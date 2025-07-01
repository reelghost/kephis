import streamlit as st
from PIL import Image
import numpy as np
import pytesseract
import pandas as pd
import cv2
import base64
from io import BytesIO

st.set_page_config(page_title="Text Extractor", layout="centered")
st.title("📷 Image Text Extractor (Serial & PIP No)")

st.markdown("""
Take **two photos** containing text like serial numbers and PIP numbers.  
Use your **rear camera** if available (mobile supported).
""")

def capture_image(label):
    uploaded = st.file_uploader(label, type=['jpg', 'jpeg', 'png'], accept_multiple_files=False, key=label)
    return uploaded

img1_file = capture_image("Step 1: Upload First Image (Serial No)")
img2_file = capture_image("Step 2: Upload Second Image (PIP No)")

def extract_text(img_file):
    if img_file is not None:
        img = Image.open(img_file)
        img_np = np.array(img)
        img_gray = cv2.cvtColor(img_np, cv2.COLOR_RGB2GRAY)

        # Enhance image
        img_resized = cv2.resize(img_gray, None, fx=2, fy=2, interpolation=cv2.INTER_LINEAR)
        img_blur = cv2.medianBlur(img_resized, 3)
        _, img_thresh = cv2.threshold(img_blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        # OCR
        custom_config = r'--oem 3 --psm 6'
        text = pytesseract.image_to_string(img_thresh, config=custom_config)
        return text.strip(), img
    return "", None

if img1_file and img2_file:
    with st.spinner("🔍 Extracting text from images..."):
        serial_text, img1 = extract_text(img1_file)
        pip_text, img2 = extract_text(img2_file)

        # Format into table
        data = {
            "Serial No": [serial_text],
            "PIP No": [pip_text]
        }
        df = pd.DataFrame(data)

        st.success("✅ Text extraction complete!")
        st.subheader("📋 Extracted Data:")
        st.table(df)

        with st.expander("📸 Show Uploaded Images"):
            st.image(img1, caption="First Image (Serial No)", use_column_width=True)
            st.image(img2, caption="Second Image (PIP No)", use_column_width=True)

elif img1_file or img2_file:
    st.info("📸 Please upload **both** images to proceed.")
