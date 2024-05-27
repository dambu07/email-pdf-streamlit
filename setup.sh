#!/bin/bash

# Create and activate a new conda environment
conda create -n myenv python=3.9 -y
conda activate myenv

# Install Python packages
pip install spacy nltk openai streamlit pytesseract google-auth-oauthlib

# Download spacy language model
python -m spacy download en_core_web_sm

# Install JavaScript packages
npm install firebase @tensorflow/tfjs @tensorflow-models/universal-sentence-encoder @tensorflow-models/posenet tesseract.js

chmod +x setup.sh
./setup.sh

streamlit run app.py