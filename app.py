import streamlit as st
import base64
from io import BytesIO
from PIL import Image
from openai import OpenAI

# 1. UI SETUP (The "Hacker" Look)
st.set_page_config(page_title="KIROSHI-RICK SCANNER", page_icon="🧪")

st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #00f3ff; font-family: 'Courier New', monospace; }
    h1 { color: #ff003c; text-shadow: 2px 2px #000; text-align: center; }
    .scan-box { border: 2px solid #00f3ff; padding: 15px; background: black; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🔋 KIROSHI v.C137")

# 2. SECURE API CONNECTION
# This line looks for the "OPENAI_API_KEY" you saved in your Streamlit Cloud Settings
try:
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
except Exception:
    st.error("Rick: 'Morty! The API Key is missing from the Secrets settings! Fix it!'")
    st.stop()

# 3. IMAGE CONVERSION FUNCTION
def process_image(img):
    buffered = BytesIO()
    img = img.convert("RGB") # Ensure it's not a PNG with transparency
    img.save(buffered, format="JPEG")
    return base64.b64encode(buffered.getvalue()).decode('utf-8')

# 4. CAMERA & INPUT
st.subheader("SCANNER READY")
# We provide two ways to scan in case one fails on mobile
tab1, tab2 = st.tabs(["LIVE CAMERA", "FILE UPLOAD"])

with tab1:
    picture = st.camera_input("POINT AND SNAP")
with tab2:
    uploaded = st.file_uploader("CHOOSE IMAGE", type=['jpg', 'jpeg', 'png'])

final_img = picture or uploaded

# 5. THE AI ANALYSIS
if final_img:
    img_pil = Image.open(final_img)
    st.image(img_pil, caption="TARGET LOCKED")
    
    if st.button("RUN DEEP SCAN"):
        with st.spinner("💾 CONNECTING TO THE CITADEL..."):
            try:
                base64_data = process_image(img_pil)
                
                response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {
                            "role": "system",
                            "content": (
                                "You are a Cyberpunk 2077 scanner with a glitched AI that sounds like Rick Sanchez. "
                                "Format your response exactly like this: "
                                "ID: [Name] | CLASS: [Type] \n"
                                "THREAT: [0-100%] | VALUE: [Eddies] \n"
                                "COMMENT: [Sarcastic Rick-style insult about the object.]"
                            )
                        },
                        {
                            "role": "user",
                            "content": [
                                {"type": "text", "text": "Scan this target."},
                                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_data}"}}
                            ],
                        }
                    ],
                    max_tokens=200
                )
                
                # Output
                result = response.choices[0].message.content
                st.markdown(f'<div class="scan-box">{result}</div>', unsafe_allow_html=True)
                
            except Exception as e:
                st.error(f"SCANNER GLITCH: {str(e)}")
