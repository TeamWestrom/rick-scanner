import streamlit as st
from PIL import Image
from openai import OpenAI

# 1. Personality Setup
st.set_page_config(page_title="Kiroshi-Rick Scanner", page_icon="🧪")
st.title("🔋 KIROSHI OPTICS v.C137")

# Enter your OpenAI API Key here
client = OpenAI(api_key="YOUR_OPENAI_API_KEY")

# 2. The Scanner UI
img_file_buffer = st.camera_input("SCAN TARGET")

if img_file_buffer is not None:
    # Read the image
    img = Image.open(img_file_buffer)
    st.image(img, caption="Target Locked.")

    # 3. The "Rick" Brain
    with st.spinner("Analyzing... don't be a Jerry..."):
        # We send the image to the AI
        # (Note: This requires a GPT-4o or Vision-enabled API key)
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": "You are a Cyberpunk scanner mixed with Rick Sanchez. Give a short 3-line scan: 1. Object name, 2. Threat Level/Value, 3. Sarcastic Rick-style insult."
                },
                {
                    "role": "user",
                    "content": "What is in this image?"
                }
            ]
        )
        
        # 4. Show the result
        st.success(response.choices[0].message.content)