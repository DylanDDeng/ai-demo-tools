import streamlit as st
import base64
import os
from mistralai import Mistral
from io import BytesIO
from PIL import Image

# Page config
st.set_page_config(
    page_title="Mistral Image Chatbot",
    page_icon="🤖",
    layout="wide"
)

# Add CSS styling
st.markdown("""
    <style>
    .stApp {
        max-width: 1200px;
        margin: 0 auto;
    }
    .stTextInput > label {
        font-size: 20px;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🤖 Mistral Image Chatbot")
st.markdown("Upload an image and chat with Mistral AI about it")

# Sidebar for configuration and image upload
with st.sidebar:
    st.title("🔑 API Configuration")
    api_key = st.text_input("Mistral API Key", type="password")
    model_option = st.selectbox(
        "Select Mistral Model",
        ["mistral-small-latest"],
        index=0
    )
    
    if api_key:
        os.environ["MISTRAL_API_KEY"] = api_key
        st.success("API key configured!")
    
    st.markdown("---")
    
    # Image uploader (moved to sidebar)
    st.subheader("📷 Upload Images")
    uploaded_files = st.file_uploader("Upload images to analyze", type=["jpg", "jpeg", "png"], accept_multiple_files=True)
    
    # Clear images button
    if st.button("Clear All Images"):
        st.session_state.uploaded_images = []
        st.session_state.image_names = []
        st.rerun()
    
    # Process uploaded files
    if uploaded_files:
        # Clear previous images if new ones are uploaded
        if len(uploaded_files) != len(st.session_state.uploaded_images):
            st.session_state.uploaded_images = []
            st.session_state.image_names = []
            
            for uploaded_file in uploaded_files:
                # Display the uploaded image
                image = Image.open(uploaded_file)
                
                # Convert the image to bytes for base64 encoding
                img_byte_arr = BytesIO()
                
                # Convert RGBA to RGB if needed (JPEG doesn't support alpha channel)
                if image.mode == 'RGBA':
                    image = image.convert('RGB')
                    
                image.save(img_byte_arr, format=image.format if image.format else "JPEG")
                img_bytes = img_byte_arr.getvalue()
                
                # Add to session state
                st.session_state.uploaded_images.append(image)
                st.session_state.image_names.append(uploaded_file.name)
        
        # Display number of uploaded images
        st.success(f"{len(st.session_state.uploaded_images)} images uploaded")
        
        # Display thumbnails of uploaded images
        if st.session_state.uploaded_images:
            for i, img in enumerate(st.session_state.uploaded_images):
                st.image(img, caption=st.session_state.image_names[i], width=150)
    
    st.markdown("---")
    
    # About this app (moved to sidebar)
    with st.expander("ℹ️ About this app"):
        st.markdown("""
        This app uses Mistral AI's multimodal capabilities to analyze images and respond to questions about them.
        
        **Features:**
        - Upload images for analysis
        - Ask questions about the uploaded image
        - Maintain conversation context
        - Choose between different Mistral models
        
        **Note:** You need a valid Mistral API key to use this application.
        """)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "uploaded_images" not in st.session_state:
    st.session_state.uploaded_images = []  # List to store multiple images

if "image_names" not in st.session_state:
    st.session_state.image_names = []  # List to store image names

# Function to encode image to base64
def encode_image(image_bytes):
    """Encode the image bytes to base64."""
    try:
        return base64.b64encode(image_bytes).decode('utf-8')
    except Exception as e:
        st.error(f"Error encoding image: {e}")
        return None

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if message["role"] == "user" and "image_names" in message:
            # Display text and image filenames for user messages with images
            image_list = ", ".join(message['image_names'])
            st.markdown(f"{message['content']} [Images: {image_list}]")
        else:
            # Display text only for other messages
            st.markdown(message["content"])

# Main chat area

# Chat input
if prompt := st.chat_input("Ask something about the image..."):
    # Check if API key is provided
    if not api_key:
        st.error("Please enter your Mistral API key in the sidebar first!")
    # Check if images are uploaded
    elif not st.session_state.uploaded_images:
        st.error("Please upload at least one image first!")
    else:
        # Encode all uploaded images
        base64_images = []
        for img in st.session_state.uploaded_images:
            img_byte_arr = BytesIO()
            
            # Convert RGBA to RGB if needed (JPEG doesn't support alpha channel)
            img_to_save = img
            if img_to_save.mode == 'RGBA':
                img_to_save = img_to_save.convert('RGB')
                
            img_to_save.save(img_byte_arr, format="JPEG")
            img_bytes = img_byte_arr.getvalue()
            base64_images.append(encode_image(img_bytes))
        
        # Add user message to chat history
        st.session_state.messages.append({
            "role": "user", 
            "content": prompt,
            "image_names": st.session_state.image_names  # Store image filenames
        })
        
        # Display user message
        with st.chat_message("user"):
            image_list = ", ".join(st.session_state.image_names)
            st.markdown(f"{prompt} [Images: {image_list}]")
        
        # Initialize Mistral client
        client = Mistral(api_key=api_key)
        
        # Prepare the message for Mistral API
        mistral_messages = []
        
        # Add previous conversation context (text only)
        for msg in st.session_state.messages[:-1]:  # Exclude the last message which we'll handle specially
            if msg["role"] == "user":
                mistral_messages.append({
                    "role": "user",
                    "content": msg["content"]
                })
            else:
                mistral_messages.append({
                    "role": "assistant",
                    "content": msg["content"]
                })
        
        # Add the current message with multiple images
        content_list = [
            {
                "type": "text",
                "text": prompt
            }
        ]
        
        # Add all images to the content list
        for base64_img in base64_images:
            content_list.append({
                "type": "image_url",
                "image_url": f"data:image/jpeg;base64,{base64_img}"
            })
        
        mistral_messages.append({
            "role": "user",
            "content": content_list
        })
        
        # Display a spinner while waiting for the response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    # Get response from Mistral
                    chat_response = client.chat.complete(
                        model=model_option,
                        messages=mistral_messages
                    )
                    
                    # Extract the response content
                    response_content = chat_response.choices[0].message.content
                    
                    # Display the response
                    st.markdown(response_content)
                    
                    # Add assistant response to chat history
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": response_content
                    })
                except Exception as e:
                    st.error(f"Error getting response from Mistral: {str(e)}")

# Add a button to clear the conversation
if st.button("Clear Conversation"):
    st.session_state.messages = []
    st.rerun()
