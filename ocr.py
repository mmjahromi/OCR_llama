import streamlit as st
import ollama
from PIL import Image

# Page configuration
st.set_page_config(
    page_title="Llama OCR",
    page_icon="🦙",
    layout="wide",
    initial_sidebar_state="expanded",
)

# App title and description
st.title("🦙 Llama OCR")
st.markdown('<p style="margin-top: -20px;">Extract structured text from images using Llama 3.2 Vision!</p>',
    unsafe_allow_html=True,
)
st.markdown("---")

# Add a custom health endpoint
if st.query_params.get("health"):
    st.write("OK")
else:
    # Your Streamlit app logic here
    st.title("🦙 Llama OCR")
    st.write("Welcome to the OCR app!")

# Model is not available, try downloading it first
try:
    # Attempt to process the image again
    response = ollama.chat(
        model="llama3.2-vision",
        messages=[
            {
                "role": "user",
                "content": (
                    "Analyze the text in the provided image. Extract all readable content "
                    "and present it in a structured Markdown format that is clear, concise, "
                    "and well-organized. Ensure proper formatting (e.g., headings, lists, or "
                    "code blocks) as necessary to represent the content effectively."
                )
            }
        ],
    )
except Exception as e:
    st.error(f"Error downloading model: {e}")

# Sidebar: Upload Image
with st.sidebar:
    st.header("Upload Image")
    uploaded_file = st.file_uploader("Choose an image...", type=["png", "jpg", "jpeg"])
    
    if uploaded_file:
        # Display the uploaded image
        try:
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded Image", width=300)
        except Exception as e:
            st.error(f"Error opening image: {e}")

        if st.button("Extract Text 🔍"):
            with st.spinner("Processing image..."):
                try:
                    response = ollama.chat(
                        model="llama3.2-vision",
                        messages=[
                            {
                                "role": "user",
                                "content": (
                                    "Analyze the text in the provided image. Extract all readable content "
                                    "and present it in a structured Markdown format that is clear, concise, "
                                    "and well-organized. Ensure proper formatting (e.g., headings, lists, or "
                                    "code blocks) as necessary to represent the content effectively."
                                ),
                                "images": [uploaded_file.getvalue()],
                            }
                        ],
                    )
                    st.session_state["ocr_result"] = response.message.content
                except Exception as e:
                    st.error(f"Error processing image: {e}")

# Clear button in main content area
col1, col2 = st.columns([6, 1])
with col2:
    if st.button("Clear 🗑️"):
        try:
            st.session_state.pop("ocr_result", None)
            st.rerun()
        except Exception as e:
            st.error(f"Error clearing session state: {e}")

# Display OCR result
if "ocr_result" in st.session_state and st.session_state["ocr_result"]:
    st.markdown(st.session_state["ocr_result"])
else:
    st.info("Upload an image and click 'Extract Text' to see the results here.")