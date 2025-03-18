import streamlit as st
from PIL import Image
import numpy as np
import io

def encode_message_in_image(image, message):
    img_array = np.array(image)
    message_bytes = message.encode('utf-8') + b'END'
    flat_img = img_array.flatten()
    
    if len(message_bytes) * 8 > len(flat_img):
        st.error("Message is too long for the selected image.")
        return None
    
    for i in range(len(message_bytes)):
        for bit in range(8):
            flat_img[i * 8 + bit] = (flat_img[i * 8 + bit] & ~1) | ((message_bytes[i] >> bit) & 1)
    
    encoded_img = flat_img.reshape(img_array.shape)
    return Image.fromarray(encoded_img)

def decode_message_from_image(image):
    img_array = np.array(image)
    flat_img = img_array.flatten()
    message_bytes = bytearray()
    
    for i in range(0, len(flat_img), 8):
        byte = sum((flat_img[i + bit] & 1) << bit for bit in range(8))
        message_bytes.append(byte)
        if message_bytes[-3:] == b'END':
            return message_bytes[:-3].decode('utf-8')
    
    return "No hidden message found."

def encrypt_message():
    st.subheader("🔐 Encrypt a Message in an Image")
    st.markdown("**Upload an image and enter a secret message to hide it within the image.**")
    
    uploaded_image = st.file_uploader("Upload An Image", type=["png", "jpg", "jpeg"])
    message = st.text_area("Enter Your Secret Message. (Press Ctrl+Enter To Submit)")
    
    if uploaded_image and message:
        image = Image.open(uploaded_image).convert("RGB")
        encoded_image = encode_message_in_image(image, message)
        
        if encoded_image:
            img_byte_arr = io.BytesIO()
            encoded_image.save(img_byte_arr, format='PNG')
            img_byte_arr.seek(0)
            
            st.success("✅ Message encoded successfully!")
            st.download_button("📥 Download Encoded Image", 
                               img_byte_arr.getvalue(), 
                               "encoded_image.png", 
                               "image/png")

def decrypt_message():
    st.subheader("🔓 Decrypt a Message from an Image")
    st.markdown("**Upload an encoded image to extract the hidden message.**")
    
    uploaded_image = st.file_uploader("Upload an encoded image", type=["png"])
    
    if uploaded_image:
        image = Image.open(uploaded_image).convert("RGB")
        decoded_message = decode_message_from_image(image)
        
        if decoded_message:
            st.success("✅ Decoded Message:")
            st.text(decoded_message)
        else:
            st.error("⚠️ No hidden message found or image is corrupted.")

def main():
    st.set_page_config(page_title="InvisiByte - Steganography", page_icon="🛡️", layout="wide")
    
    st.markdown("""
        <style>
            /* Base Styles */
            .main {
                padding: 2rem;
                background-color: #f8f9fa;
                color: #212529;
            }
            body {
                font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            }
            
            /* Typography */
            h1 {
                font-size: 2.2rem;
                font-weight: 700;
                color: #1a3b6e;
                margin-bottom: 0.5rem;
            }
            h2, h3, h4 {
                color: #1a3b6e;
                font-weight: 600;
            }
            p, li {
                color: #495057;
                font-size: 1rem;
                line-height: 1.5;
            }
            
            /* Tabs */
            .stTabs [data-baseweb="tab-list"] {
                gap: 0.5rem;
                background-color: transparent;
                padding: 0.75rem 0;
                border-bottom: 1px solid #dee2e6;
            }
            .stTabs [data-baseweb="tab"] {
                height: 45px;
                padding: 0 1.75rem;
                color: #495057;
                font-weight: 500;
                background-color: white;
                border: 1px solid #dee2e6;
                border-radius: 6px;
                box-shadow: 0 1px 2px rgba(0,0,0,0.05);
                transition: all 0.2s ease;
            }
            .stTabs [data-baseweb="tab"]:hover {
                color: #1a3b6e;
                border-color: #b8c4d9;
            }
            .stTabs [data-baseweb="tab"][aria-selected="true"] {
                color: white !important;
                border-color: #1a3b6e;
                background-color: #1a3b6e;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }
            /* Ensure text inside selected tab is white */
            .stTabs [data-baseweb="tab"][aria-selected="true"] * {
                color: white !important;
            }
            
            /* Cards & Containers */
            .card {
                background-color: white;
                border-radius: 8px;
                border: 1px solid #e9ecef;
                padding: 1.75rem;
                margin: 1.25rem 0;
                box-shadow: 0 2px 12px rgba(0,0,0,0.05);
                transition: box-shadow 0.3s ease;
            }
            .card:hover {
                box-shadow: 0 4px 16px rgba(0,0,0,0.08);
            }
            .info-card {
                background-color: #f8f9fa;
                border-left: 4px solid #1a3b6e;
                border-radius: 6px;
                padding: 1.5rem;
                margin: 1.25rem 0;
            }
            
            /* Buttons & Interactive Elements */
            .stButton>button, .stDownloadButton>button, [data-testid="stFileUploadButton"] {
                background-color: #1a3b6e !important;
                color: white !important;
                font-weight: 600 !important;
                padding: 0.65rem 1.5rem !important;
                border-radius: 6px !important;
                border: none !important;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1) !important;
                transition: all 0.2s ease !important;
            }
            .stButton>button:hover, .stDownloadButton>button:hover, [data-testid="stFileUploadButton"]:hover {
                background-color: #0f2952 !important;
                box-shadow: 0 4px 8px rgba(0,0,0,0.15) !important;
                transform: translateY(-1px) !important;
                color: white !important;
            }
            .stButton>button:active, .stDownloadButton>button:active, [data-testid="stFileUploadButton"]:active,
            .stButton>button:focus, .stDownloadButton>button:focus, [data-testid="stFileUploadButton"]:focus {
                background-color: #1a3b6e !important;
                color: white !important;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1) !important;
                outline: none !important;
                border: none !important;
            }
            .stButton>button:disabled, .stDownloadButton>button:disabled, [data-testid="stFileUploadButton"]:disabled {
                background-color: #e9ecef !important;
                color: white !important;
                box-shadow: none !important;
            }
            
            /* Download Button - Updated to remove dark-blue color */
            .stDownloadButton>button {
                background-color: #f8f9fa !important;
                color: #212529 !important;
                font-weight: 600 !important;
                padding: 0.65rem 1.5rem !important;
                border-radius: 6px !important;
                border: 1px solid #ced4da !important;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1) !important;
                transition: all 0.2s ease !important;
                display: block !important;
                margin: 0 auto !important;
            }
            .stDownloadButton>button:hover {
                background-color: #e9ecef !important;
                box-shadow: 0 4px 8px rgba(0,0,0,0.15) !important;
                transform: translateY(-1px) !important;
                color: #212529 !important;
            }
            .stDownloadButton>button:active {
                background-color: #dee2e6 !important;
                transform: translateY(1px) !important;
                box-shadow: 0 1px 2px rgba(0,0,0,0.1) !important;
                color: #212529 !important;
            }
            .stDownloadButton>button:disabled {
                background-color: #e9ecef !important;
                color: #212529 !important;
                box-shadow: none !important;
            }
            
            /* File Uploader - More aggressive styling */
            .stFileUploader,
            div.stFileUploader,
            [data-testid="stFileUploader"],
            div[data-testid="stFileUploader"] {
                background-color: white !important;
                border: 2px solid #ced4da !important;
                border-radius: 6px !important;
                padding: 1rem !important;
                box-shadow: none !important;
                margin-bottom: 1rem !important;
            }
            [data-testid="stFileDropzone"],
            div[data-testid="stFileDropzone"],
            .stFileUploader [data-testid="stFileDropzone"],
            .stFileUploader div[data-testid="stFileDropzone"] {
                border: 2px solid #ced4da !important;
                border-radius: 6px !important;
                background-color: white !important;
                padding: 1rem !important;
            }
            .element-container:has(.stFileUploader) .stFileUploader {
                border: 2px solid #ced4da !important;
                border-radius: 6px !important;
            }
            .stFileUploader label, 
            div.stFileUploader p, 
            .stFileUploader div p,
            .stFileUploader > div:first-child {
                background-color: #f8f9fa !important;
                color: #212529 !important;
                font-weight: 500 !important;
            }
            .stMarkdown p {
                background-color: #f8f9fa !important;
            }
            [data-testid="stFileUploader"] div,
            [data-testid="stFileUploader"] span,
            [data-testid="stFileUploader"] p,
            [data-testid="stFileDropzone"] div,
            [data-testid="stFileDropzone"] span,
            [data-testid="stFileDropzone"] p,
            .stFileUploader small,
            .stFileUploader div small,
            [data-testid="stFileUploader"] small,
            [data-testid="stFileDropzone"] small {
                color: #212529 !important;
                background-color: transparent !important;
            }
            .stFileUploader div small,
            [data-testid="stFileUploader"] small,
            [data-testid="stFileDropzone"] small,
            small[data-testid="stFileUploadDropzoneSubHeader"] {
                color: #212529 !important;
                font-weight: 400 !important;
                background-color: transparent !important;
                opacity: 1 !important;
            }
            [data-testid="stFileUploader"] button,
            .stFileUploader button,
            button[data-testid="stFileUploadButton"] {
                background-color: #1a3b6e !important;
                color: white !important;
                font-weight: 600 !important;
                padding: 0.65rem 1.5rem !important;
                border-radius: 6px !important;
                border: none !important;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1) !important;
                transition: all 0.2s ease !important;
            }
            [data-testid="stFileUploader"] button:hover,
            .stFileUploader button:hover,
            button[data-testid="stFileUploadButton"]:hover {
                background-color: #0f2952 !important;
                box-shadow: 0 4px 8px rgba(0,0,0,0.15) !important;
                transform: translateY(-1px) !important;
            }
            [data-testid="stFileUploader"] section,
            [data-testid="stFileUploader"] div,
            [data-testid="stFileUploader"] span,
            [data-testid="stFileUploader"] p,
            [data-testid="stFileUploader"] label,
            [data-testid="stFileDropzone"],
            [data-testid="stFileDropzone"] div,
            [data-testid="stFileDropzone"] span,
            [data-testid="stFileDropzone"] p {
                background-color: white !important;
                border-color: #ced4da !important;
            }
            [style*="background-color: rgb(149, 64, 255)"],
            [style*="background-color: rgb(128, 51, 255)"],
            [style*="background-color: rgb(114, 31, 255)"],
            [style*="background-color:rgb(149, 64, 255)"],
            [style*="background-color:rgb(128, 51, 255)"],
            [style*="background-color:rgb(114, 31, 255)"] {
                background-color: white !important;
            }
            div[class*="css"] {
                background-color: white !important;
            }
            .stTextArea>div>div {
                border-radius: 6px;
                border-color: #ced4da !important;
                background-color: white !important;
            }
            .stTextArea textarea {
                color: #212529;
                font-size: 1rem;
                background-color: white !important;
            }
            .stTextArea textarea:focus {
                border-color: #1a3b6e !important;
                box-shadow: 0 0 0 2px rgba(26, 59, 110, 0.25) !important;
                background-color: white !important;
            }
            .stTextArea textarea::placeholder {
                color: #212529 !important;
                opacity: 1 !important;
            }
            .stTextArea small {
                color: #000000 !important;
                opacity: 1 !important;
            }
            .stCodeBlock {
                background-color: #1a3b6e !important;
                color: white !important;
                border-radius: 6px;
                padding: 1rem;
            }
            .success-message {
                background-color: #e8f5e9;
                border: 1px solid #a5d6a7;
                border-radius: 6px;
                padding: 1rem;
                color: #2e7d32;
                margin: 1rem 0;
            }
            .info-message {
                background-color: #e3f2fd;
                border: 1px solid #90caf9;
                border-radius: 6px;
                padding: 1rem;
                color: #0d47a1;
                margin: 1rem 0;
            }
            .warning-message {
                background-color: #fff8e1;
                border: 1px solid #ffecb3;
                border-radius: 6px;
                padding: 1rem;
                color: #f57f17;
                margin: 1rem 0;
            }
            .error-message {
                background-color: #ffebee;
                border: 1px solid #ffcdd2;
                border-radius: 6px;
                padding: 1rem;
                color: #c62828;
                margin: 1rem 0;
            }
            .image-container {
                margin: 1rem 0;
                max-width: 700px !important;
                margin-left: auto !important;
                margin-right: auto !important;
            }
            .image-container img {
                border-radius: 6px;
                box-shadow: 0 2px 8px rgba(0,0,0,0.1);
                max-width: 700px !important;
                width: 700px !important;
            }
            .image-caption {
                text-align: center;
                color: #6c757d;
                font-size: 0.9rem;
                margin-top: 0.5rem;
            }
            [data-testid="stImage"] {
                max-width: 700px !important;
                width: 700px !important;
                margin-left: auto !important;
                margin-right: auto !important;
            }
            [data-testid="stImage"] > img {
                max-width: 700px !important;
                width: 700px !important;
            }
            ::-webkit-scrollbar {
                width: 8px;
                height: 8px;
            }
            ::-webkit-scrollbar-track {
                background: #f1f1f1;
                border-radius: 4px;
            }
            ::-webkit-scrollbar-thumb {
                background: #c1c9d6;
                border-radius: 4px;
            }
            ::-webkit-scrollbar-thumb:hover {
                background: #a3b1c6;
            }
        </style>
    """, unsafe_allow_html=True)
    
    st.title("🛡️ InvisiByte")
    st.markdown("**A secure way to hide and extract messages using steganography.**")
    
    tab1, tab2 = st.tabs(["🔐 Encrypt", "🔓 Decrypt"])
    
    with tab1:
        encrypt_message()
    
    with tab2:
        decrypt_message()

if __name__ == "__main__":
    main()
