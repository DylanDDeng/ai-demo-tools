import streamlit as st
from phi.agent import Agent
from phi.model.google import Gemini
from phi.tools.duckduckgo import DuckDuckGo
import replicate
import os
from PIL import Image
import requests
from io import BytesIO
import base64

# page config
st.set_page_config(
    page_title="AI Image & Video Generator",
    page_icon="🎨",
    layout="wide"
)

# add css style
st.markdown("""
    <style>
    .stTextInput > label {
        font-size: 20px;
        font-weight: bold;
    }
    .main {
        padding: 2rem;
    }
    </style>
""", unsafe_allow_html=True)

# sidebar api config
with st.sidebar:
    st.title("🔑 API Configuration")
    gemini_key = st.text_input("Gemini API Key", type="password")
    replicate_key = st.text_input("Replicate API Key", type="password")
    
    if gemini_key and replicate_key:
        os.environ["GOOGLE_API_KEY"] = gemini_key
        os.environ["REPLICATE_API_TOKEN"] = replicate_key
        st.success("API keys configured successfully!")

# main interface
st.title("🎨 AI Image & Video Generator")
st.markdown("Generate unique images and videos from your text descriptions")

# init session_state
if 'generated_images' not in st.session_state:
    st.session_state.generated_images = []  # store all generated images
if 'image_data_list' not in st.session_state:
    st.session_state.image_data_list = []   # store all image data
if 'prompts' not in st.session_state:
    st.session_state.prompts = []           # store all generated prompts
if 'generated_videos' not in st.session_state:
    st.session_state.generated_videos = []   # store all generated videos

# user input
user_input = st.text_area("Enter your description:", height=100)

# create two columns for generating buttons
col1, col2 = st.columns(2)

# generate image button
with col1:
    generate_image_button = st.button("🎨 Generate Image", type="primary")

# generate video button
with col2:
    generate_video_button = st.button("🎬 Generate Video", type="primary")

def extract_model_content(response):
    if hasattr(response, 'messages'):
        for message in response.messages:
            if message.role == 'model' and message.content and not message.tool_calls:
                return message.content
    return None

def extract_content(response):
    if hasattr(response, 'content'):
        return response.content.strip()
    return None

def generate_prompt(user_input):
    """generate optimized prompt using Gemini and DuckDuckGo"""
    try:
        agent = Agent(
            model=Gemini(id="gemini-2.0-flash-exp"),
            tools=[DuckDuckGo(search=True)],
            instructions=[
                "Please according to the search results, give back only one prompt for AI image generation;",
                "Just give me the prompt, no other words",
                "Make the prompt detailed and optimized for image generation"
            ],
            show_tool_calls=True,
            markdown=True,
        )
        
        response = agent.run(user_input)
        return extract_model_content(response) or extract_content(response)
    except Exception as e:
        st.error(f"Error generating prompt: {str(e)}")
        return None

def generate_image(prompt):
    """generate image using Replicate API"""
    try:
        output = replicate.run(
            "black-forest-labs/flux-1.1-pro-ultra",
            input={
                "prompt": prompt,
                "aspect_ratio": "3:2"
            }
        )
        return output
    except Exception as e:
        st.error(f"Error generating image: {str(e)}")
        return None

def generate_video(prompt):
    """generate video using Replicate API"""
    try:
        output = replicate.run(
            "minimax/video-01",
            input={"prompt": prompt}
        )
        return output
    except Exception as e:
        st.error(f"Error generating video: {str(e)}")
        return None

def get_video_html(video_data):
    """generate video html tag"""
    b64 = base64.b64encode(video_data).decode()
    return f"""
        <video width="100%" controls>
            <source src="data:video/mp4;base64,{b64}" type="video/mp4">
            Your browser does not support the video tag.
        </video>
    """

# generate image logic
if generate_image_button:
    if not (gemini_key and replicate_key):
        st.error("Please configure both API keys in the sidebar first!")
    elif not user_input:
        st.warning("Please enter a description first!")
    else:
        # step 1: generate optimized prompt
        with st.spinner("Step 1/2: Generating optimized prompt using Gemini..."):
            prompt = generate_prompt(user_input)
            
            if prompt:
                st.success("✅ Prompt generated successfully!")
                
                # display generated prompt using expander
                with st.expander("Show generated prompt", expanded=True):
                    st.info(f"Generated prompt: {prompt}")
                
                # step 2: generate image using prompt
                with st.spinner("Step 2/2: Generating image using Replicate..."):
                    image_url = generate_image(prompt)
                    
                    if image_url:
                        try:
                            # 获取图像
                            response = requests.get(image_url, timeout=30)
                            img = Image.open(BytesIO(response.content))
                            
                            # prepare image data
                            buf = BytesIO()
                            img.save(buf, format="JPEG")
                            img_data = buf.getvalue()
                            
                            # add new image and prompt to the list
                            st.session_state.generated_images.insert(0, img)
                            st.session_state.image_data_list.insert(0, img_data)
                            st.session_state.prompts.insert(0, prompt)  # save prompt
                            
                            st.success("✅ Image generated successfully!")
                            
                            # reload page to display new image
                            st.rerun()
                                
                        except Exception as e:
                            st.error(f"Error downloading image: {str(e)}")
            else:
                st.error("Failed to generate prompt. Please try again.")

# generate video logic
if generate_video_button:
    if not (gemini_key and replicate_key):
        st.error("Please configure both API keys in the sidebar first!")
    elif not user_input:
        st.warning("Please enter a description first!")
    else:
        # step 1: generate optimized prompt
        with st.spinner("Step 1/2: Generating optimized prompt using Gemini..."):
            prompt = generate_prompt(user_input)
            
            if prompt:
                st.success("✅ Prompt generated successfully!")
                with st.expander("Show generated prompt", expanded=True):
                    st.info(f"Generated prompt: {prompt}")
                
                # step 2: generate video
                with st.spinner("Step 2/2: Generating video..."):
                    video_data = generate_video(prompt)
                    if video_data:
                        # save video data and prompt
                        video_bytes = video_data.read()
                        st.session_state.generated_videos.insert(0, {
                            'video_data': video_bytes,
                            'prompt': prompt
                        })
                        st.success("✅ Video generated successfully!")
                        st.rerun()

# display all generated content
for idx, (img, img_data, prompt) in enumerate(zip(
    st.session_state.get('generated_images', []),
    st.session_state.get('image_data_list', []),
    st.session_state.get('prompts', [])
)):
    with st.expander(f"Generated Image {len(st.session_state.generated_images) - idx}", expanded=(idx == 0)):
        st.image(img, caption=f"Generated Image {len(st.session_state.generated_images) - idx}", 
                use_column_width=True)
        st.info(f"Generated prompt: {prompt}")
        
        # download image button
        st.download_button(
            label="⬇️ Download Image",
            data=img_data,
            file_name=f"generated_image_{len(st.session_state.generated_images) - idx}.jpg",
            mime="image/jpeg",
            key=f"download_button_{len(st.session_state.generated_images) - idx}"
        )

# display all generated videos
for idx, video_item in enumerate(st.session_state.get('generated_videos', [])):
    with st.expander(f"Generated Video {len(st.session_state.generated_videos) - idx}", expanded=(idx == 0)):
        st.info(f"Generated prompt: {video_item['prompt']}")
        
        # display video
        st.markdown(get_video_html(video_item['video_data']), unsafe_allow_html=True)
        
        # download video button
        st.download_button(
            label="⬇️ Download Video",
            data=video_item['video_data'],
            file_name=f"generated_video_{len(st.session_state.generated_videos) - idx}.mp4",
            mime="video/mp4",
            key=f"download_video_{len(st.session_state.generated_videos) - idx}"
        )

# add footer
st.markdown("---")
st.markdown("Made with ❤️ using Streamlit")