# Mistral Image Chatbot 🤖

A Streamlit-based chatbot that uses Mistral AI's multimodal capabilities to analyze images and respond to questions about them.

## Features

- Upload images for analysis
- Ask questions about the uploaded image
- Maintain conversation context
- Choose between different Mistral models (small, medium, large)

## Installation

1. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

2. Get a Mistral API key from [Mistral AI](https://mistral.ai/)

## Usage

1. Run the Streamlit app:
   ```
   streamlit run mistral_image_chatbot.py
   ```

2. Enter your Mistral API key in the sidebar
3. Upload an image
4. Ask questions about the image in the chat

## Files

- `mistral_image_chatbot.py` - Main Streamlit application
- `test_mistral_small.py` - Simple test script for Mistral API
- `requirements.txt` - Required Python packages

## Requirements

- Python 3.8+
- Mistral API key
- Internet connection for API access