import streamlit as st
from PIL import Image
import numpy as np
import cv2
import pytesseract
import pandas as pd

st.set_page_config(page_title="Text Extractor", layout="centered")
st.title("📷 Image Text Extractor (Serial & PIP No)")

st.markdown("""
Take **two photos** containing text like serial numbers and PIP numbers.
The app will extract the text and display it in a table format.
""")

# Capture the first image
img1_file = st.camera_input("Step 1: Capture First Image (Serial No)")

# Capture the second image
img2_file = st.camera_input("Step 2: Capture Second Image (PIP No)")

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

        with st.expander("📸 Show Captured Images"):
            st.image(img1, caption="First Image (Serial No)", use_column_width=True)
            st.image(img2, caption="Second Image (PIP No)", use_column_width=True)

elif img1_file or img2_file:
    st.info("📸 Please capture **both** images to proceed.")

