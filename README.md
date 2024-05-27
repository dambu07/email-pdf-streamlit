# Email PDF Organizer and Management System

A Streamlit application for organizing and managing PDFs from emails using Firebase and various AI models. This app allows you to authenticate with Gmail, fetch PDFs, extract text using OCR, categorize PDFs, and interact with the content using OpenAI's GPT-3.

## Features

- **Firebase Authentication**: Sign up and login using Firebase.
- **Gmail Integration**: Authenticate with Gmail and fetch PDFs from your email.
- **OCR Text Extraction**: Extract text from PDFs using Tesseract OCR.
- **Categorize PDFs**: Automatically categorize PDFs based on their content.
- **Chat with PDF Content**: Interact with the content of PDFs using OpenAI's GPT-3.

## Installation

### Prerequisites

- [Conda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html)
- [Node.js and npm](https://nodejs.org/)

### Step-by-Step Installation

1. **Clone the repository**:

   ```sh
   git clone https://github.com/dambu07/email-pdf-organizer.git
   cd email-pdf-organizer

Create and activate a new conda environment:
conda create -n myenv python=3.9 -y
conda activate myenv
Install Python dependencies:
pip install -r requirements.txt
Install JavaScript dependencies:
npm install
Download Spacy language model:
python -m spacy download en_core_web_sm
Environment Variables
Create a .env file in the root directory of your project and add the following environment variables:

GOOGLE_CLIENT_SECRET=your_google_client_secret
FIREBASE_ADMINSDK_PATH=path/to/your/firebase-adminsdk.json
OPENAI_API_KEY=your_openai_api_key
Usage
Run the Streamlit app:

streamlit run app.py
Project Structure
email-pdf-organizer/
├── app.py
├── requirements.txt
├── package.json
├── setup.sh
├── .env
└── README.md
Dependencies
Python Packages
streamlit
python-dotenv
pytesseract
openai
google-auth-oauthlib
google-api-python-client
PyPDF2
firebase-admin
spacy==3.2.0
nltk
JavaScript Packages
firebase
@tensorflow/tfjs
@tensorflow-models/universal-sentence-encoder
@tensorflow-models/posenet
tesseract.js
Contributing
Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

License
This project is licensed under the MIT License.

Acknowledgements
Streamlit
Firebase
OpenAI
Tesseract OCR
Spacy
TensorFlow.js

### Explanation

- **Project Title and Description**: Provides an overview of what the project is about.
- **Features**: Lists the key features of the application.
- **Installation**: Step-by-step instructions for setting up the project, including prerequisites and commands to install dependencies.
- **Environment Variables**: Instructions for setting up environment variables required by the application.
- **Usage**: Instructions for running the Streamlit app.
- **Project Structure**: A brief overview of the project's file structure.
- **Dependencies**: Lists the Python and JavaScript dependencies.
- **Contributing**: Guidelines for contributing to the project.
- **License**: Information about the project's license.
- **Acknowledgements**: Credits to the tools and libraries used in the project.

### Usage

1. Save the above content into a file named `README.md` in the root directory of your project.
2. Ensure the `.env` file is correctly set up with your credentials.
3. Follow the installation instructions to set up the project.
4. Run the Streamlit app using `streamlit run app.py`.

By following these steps, you should have a comprehensive README for your Streamlit application, making it easier for others to understand and contribute to your project. If you encounter any further issues or need additional information, please let me know!
