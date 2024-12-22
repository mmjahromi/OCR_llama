import streamlit as st
import ollama
from PIL import Image
import io
import time
from pdf2image import convert_from_path
from pdf2image import convert_from_bytes
import filetype
import mimetypes


# Page configuration
st.set_page_config(
    page_title="Extract Text from Images with AI Solutions",
    page_icon="🖼️",
    layout="wide",
    initial_sidebar_state="expanded",
)


# File validation function
def validate_file(uploaded_file):
    mime_type, _ = mimetypes.guess_type(uploaded_file.name)
    supported_mime_types = {
        "image/jpeg": "jpeg",
        "image/png": "png",
        "image/gif": "gif",
        "image/tiff": "tiff",
        "application/pdf": "pdf",
    }
    if mime_type in supported_mime_types:
        return supported_mime_types[mime_type]
    return None

# Enhanced Debugging Function
def log_timing(step_name, start_time):
    elapsed_time = time.time() - start_time
    st.write(f"⏱️ {step_name} took {elapsed_time:.2f} seconds")

# Clear data on file upload
def clear_results():
    st.session_state["ocr_result"] = None

# Supported file formats
SUPPORTED_FORMATS = ["jpg", "jpeg", "png", "gif", "jfif", "heic", "pdf", "tiff"]

# File validation function
def validate_file(file):
    kind = filetype.guess(file)
    if kind is not None and kind.extension in SUPPORTED_FORMATS:
        return kind.extension
    return None

# Process uploaded file
def process_uploaded_file(uploaded_file, file_extension):
    uploaded_file.seek(0)  # Reset the file pointer
    if file_extension in ["jpg", "jpeg", "png", "gif", "jfif", "heic", "tiff"]:
        return Image.open(uploaded_file)
    elif file_extension == "pdf":
        try:
            pdf_bytes = uploaded_file.read()
            images = convert_from_bytes(pdf_bytes, dpi=300)
            return images[0]  # Process the first page only
        except Exception as e:
            raise ValueError(f"Failed to process PDF file. Error: {e}")
    else:
        raise ValueError("Unsupported file format")


# Custom CSS Styling
st.markdown(
    """
    <style>
    body {
        background-color: #f8f9fa;
        font-family: 'Arial', sans-serif;
        color: #212529;
    }
    h1 {
        color: #007bff;
        text-align: center;
        font-size: 3em;
        margin-bottom: 0.5em;
    }
    .description {
        text-align: center;
        font-size: 1.2em;
        color: #6c757d;
        margin-bottom: 2em;
    }
    .stButton button {
        background-color: #007bff;
        color: white;
        border: none;
        padding: 0.7em 1.5em;
        font-size: 1.1em;
        border-radius: 5px;
        cursor: pointer;
    }
    .stButton button:hover {
        background-color: #0056b3;
    }
    .sidebar-header {
        font-size: 1.5em;
        color: #007bff;
        margin-bottom: 1em;
    }
    .ad-container {
        border: 1px solid #ccc;
        padding: 20px;
        text-align: center;
        background-color: #ffffff;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-top: 2em;
    }
    .ad-container h3 {
        color: #333;
        font-size: 1.3em;
        margin-bottom: 0.5em;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# App title and description
start_time = time.time()
st.markdown(
    """
    <h1>Extract Text from Images Using AI Solutions</h1>
    <p class="description">Experience the power of AI to extract text seamlessly and efficiently.</p>
    """,
    unsafe_allow_html=True,
)
log_timing("Page Setup", start_time)

# Sidebar for uploading files
with st.sidebar:
    st.markdown("<div class='sidebar-header'>Upload Your File</div>", unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Choose a file...", type=SUPPORTED_FORMATS, on_change=clear_results)
    log_timing("Sidebar Rendering", start_time)

    if uploaded_file:
        try:
            # Determine file extension
            file_extension = validate_file(uploaded_file)
            if not file_extension:
                st.error("Unsupported file format. Please upload a valid file.")
                st.stop()

            # Process file into an image
            image = process_uploaded_file(uploaded_file, file_extension)
            st.image(image, caption="Uploaded File Preview", width=300)

            if st.button("Extract Text 🔍"):
                with st.spinner("Processing your file..."):
                    try:
                        # Convert image to bytes in a valid format for the API
                        img_bytes = io.BytesIO()
                        image.save(img_bytes, format="PNG")  # Ensure the image is encoded as PNG
                        img_bytes.seek(0)  # Reset the pointer for reading

                        # Extract text from the image
                        response = ollama.chat(
                            model="llama3.2-vision",
                            messages=[
                                {
                                    "role": "user",
                                    "content": (
                                        "Analyze the text in the provided image. Extract all readable content "
                                        "and present it in a structured Markdown format."
                                    ),
                                    "images": [img_bytes.read()],  # Pass valid image bytes for processing
                                }
                            ],
                        )
                        st.session_state["ocr_result"] = response.message.content
                    except Exception as e:
                        st.error(f"Error extracting text: {e}")
        except Exception as e:
            st.error(f"Error processing file: {e}")


# Display OCR result and download option
if "ocr_result" in st.session_state and st.session_state["ocr_result"]:
    st.markdown(st.session_state["ocr_result"])
    result_bytes = io.BytesIO(st.session_state["ocr_result"].encode("utf-8"))
    st.download_button(
        label="Download Results as .txt",
        data=result_bytes,
        file_name="ocr_result.txt",
        mime="text/plain",
    )
else:
    st.info("Upload a file and click 'Extract Text' to see results.")

# Advertisement Section
st.markdown("---")
st.markdown(
    """
    <div class="ad-container">
        <h3>Sponsored Ads</h3>
        <p>Promote your brand here! Contact us for more details.</p>
    </div>
    """,
    unsafe_allow_html=True,
)
