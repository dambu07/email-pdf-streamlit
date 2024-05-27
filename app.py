import os
from dotenv import load_dotenv
import streamlit as st
import pickle
import pytesseract  # Ensure pytesseract is installed: # `pip install pytesseract` is a command used to install the pytesseract library in Python. Pytesseract is a Python wrapper for Google's Tesseract-OCR Engine, which is used for optical character recognition (OCR). This library allows you to extract text from images and PDFs, making it useful for tasks like reading text from scanned documents or images containing text.
import openai
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from pytesseract import image_to_string
from PyPDF2 import PdfReader
from PIL import Image
from io import BytesIO
import base64
import firebase_admin
from firebase_admin import credentials, auth
import spacy
import nltk
import tempfile
nltk.download('punkt')
from nltk.tokenize import word_tokenize, sent_tokenize

# Load environment variables from .env file
load_dotenv()

# Get environment variables
GOOGLE_CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET')
FIREBASE_ADMINSDK_PATH = os.getenv('FIREBASE_ADMINSDK_PATH')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Set up OpenAI API key
openai.api_key = OPENAI_API_KEY

# Set up Firebase
if not firebase_admin._apps:
    cred = credentials.Certificate(FIREBASE_ADMINSDK_PATH)
    firebase_admin.initialize_app(cred)

# Define the scopes for Gmail
SCOPES_GMAIL = ['https://www.googleapis.com/auth/gmail.readonly']

# Define the local storage directory for PDFs
LOCAL_PDF_DIR = "pdfs"

# Function to authenticate and get the Gmail service
def authenticate_gmail():
    creds = None
    if os.path.exists('token_gmail.pkl'):
        with open('token_gmail.pkl', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials_gmail.json', SCOPES_GMAIL)
            creds = flow.run_local_server(port=0)
        with open('token_gmail.pkl', 'wb') as token:
            pickle.dump(creds, token)
    try:
        return build('gmail', 'v1', credentials=creds)
    except HttpError as error:
        st.error(f'An error occurred: {error}')
        return None

# Function to authenticate users with Firebase
def firebase_authentication():
    st.write("## FileBoro Authentication")
    choice = st.selectbox("Login/Signup", ["Login", "Signup"])
    
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    
    if choice == "Signup" and st.button("Signup"):
        try:
            user = auth.create_user(
                email=email,
                password=password
            )
            st.success(f"User created successfully: {user.email}")
        except Exception as e:
            st.error(f"Error creating user: {e}")
    
    elif choice == "Login" and st.button("Login"):
        try:
            # Firebase Admin SDK does not provide direct methods to verify passwords
            # You would typically use Firebase Authentication Client SDK for user sign-in
            # This is a placeholder for actual password verification
            user = auth.get_user_by_email(email)
            # Assume a method to verify password here, which you need to implement
            # user = auth.verify_password(email, password)  # Placeholder
            st.success(f"Authenticated as {user.email}")
            st.session_state.user = user
        except Exception as e:
            st.error(f"Invalid credentials: {e}")

# Function to fetch PDFs from Gmail
def fetch_pdfs_gmail(service):
    results = service.users().messages().list(userId='me', q='has:attachment filename:pdf').execute()
    messages = results.get('messages', [])
    pdfs = []

    for message in messages:
        msg = service.users().messages().get(userId='me', id=message['id']).execute()
        for part in msg['payload']['parts']:
            if part['filename'].endswith('.pdf'):
                att_id = part['body']['attachmentId']
                att = service.users().messages().attachments().get(userId='me', messageId=message['id'], id=att_id).execute()
                file_data = base64.urlsafe_b64decode(att['data'].encode('UTF-8'))
                pdf_content = BytesIO(file_data)
                pdfs.append((part['filename'], pdf_content))
    return pdfs

# Function to extract text from PDF using OCR
def extract_pdf_from_mail(file):
    pdf = PdfReader(file)
    text = ""
    for page_num in range(len(pdf.pages)):
        page = pdf.pages[page_num]
        image = page.to_image()
        text += image_to_string(image)
    return text

def extract_text_from_pdf(file_content):
    pdf = PdfReader(file_content)
    return "".join(page.extract_text() for page in pdf.pages)

# Function to categorize PDFs
def categorize_pdfs(pdfs):
    categorized_pdfs = {}
    for filename, file_content in pdfs:
        text = extract_text_from_pdf(file_content)
        if "invoice" in text.lower():
            category = "Invoices"
        elif "report" in text.lower():
            category = "Reports"
        else:
            category = "Others"
        if category not in categorized_pdfs:
            categorized_pdfs[category] = []
        categorized_pdfs[category].append((filename, file_content))
    return categorized_pdfs

# Function to read PDFs from local storage
def read_pdfs_from_local():
    pdfs = []
    for root, dirs, files in os.walk(LOCAL_PDF_DIR):
        for file in files:
            if file.endswith(".pdf"):
                file_path = os.path.join(root, file)
                with open(file_path, "rb") as f:
                    pdf_content = BytesIO(f.read())
                    pdfs.append((file, pdf_content))
    return pdfs

# Function to chat with PDF content
def chat_with_pdf(text):
    st.write("## Chat with PDF Content")
    user_input = st.text_input("Ask a question about the PDF")
    if st.button("Send"):
        response = openai.Completion.create(
            engine="davinci",
            prompt=f"User: {user_input}\nPDF Content: {text}\nAssistant:",
            max_tokens=150
        )
        st.write(response.choices[0].text.strip())

# Main application
def main():
    st.title("Email Attatchment Organizer")

    # Authenticate with Firebase
    firebase_authentication()
    # authenticate_gmail()

    if "user" in st.session_state:
        # Homepage
        st.header("Choose an option")
        option = st.selectbox("How would you like to view PDF files?", ("", "View PDF files from local storage", "Authenticate with Gmail"))

        if option == "View PDF files from local storage":
            # View PDFs from local storage
            st.header("Local PDF Files")
            if pdfs := read_pdfs_from_local():
                categorized_pdfs = categorize_pdfs(pdfs)
                display_categorized_pdfs(categorized_pdfs)
            else:
                st.write("No PDF files found in the specified directory.")

        elif option == "Authenticate with Gmail":
            # Google authentication
            st.header("Gmail Authentication")
            service = authenticate_gmail()
            if not service:
                st.error("Failed to authenticate with Google.")
                return

            # Fetch PDFs from Gmail
            st.header("Fetched PDFs from Gmail")
            if pdfs := fetch_pdfs_gmail(service):
                categorized_pdfs = categorize_pdfs(pdfs)
                display_categorized_pdfs(categorized_pdfs)
            else:
                st.write("No PDF files found in Gmail.")

# Function to display categorized PDFs
def display_categorized_pdfs(categorized_pdfs):
    for category, pdf_files in categorized_pdfs.items():
        st.subheader(category)
        for filename, file_content in pdf_files:
            st.write(filename)
            # Save the PDF file to a temporary location to view it
            with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
                tmp_file.write(file_content.getbuffer())
                tmp_file_path = tmp_file.name
            with st.expander("View PDF"):
                # Display the PDF file using an iframe
                st.components.v1.iframe(tmp_file_path, height=600)
            # Button to start a chat with the PDF content
            if st.button(f"Chat with {filename}"):
                text = extract_text_from_pdf(file_content)
                chat_with_pdf(text)

    # Search functionality
    st.header("Search PDFs")
    query = st.text_input("Search")
    if st.button("Search"):
        results = []
        for category, pdf_files in categorized_pdfs.items():
            for filename, file_content in pdf_files:
                text = extract_text_from_pdf(file_content)
                if query.lower() in text.lower():
                    results.append((filename, file_content))
        if results:
            st.write("Search Results:")
            for filename, file_content in results:
                st.write(filename)
                # Save the PDF file to a temporary location to view it
                with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
                    tmp_file.write(file_content.getbuffer())
                    tmp_file_path = tmp_file.name
                with st.expander("View PDF"):
                    # Display the PDF file using an iframe
                    st.components.v1.iframe(tmp_file_path, height=600)
                # Button to start a chat with the PDF content
                if st.button(f"Chat with {filename} (Search Result)"):
                    text = extract_text_from_pdf(file_content)
                    chat_with_pdf(text)
        else:
            st.write("No results found")

if __name__ == "__main__":
    main()