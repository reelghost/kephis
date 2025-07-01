import streamlit as st
from PIL import Image
import numpy as np
import cv2
import pandas as pd
from pyzbar.pyzbar import decode, ZBarSymbol

st.set_page_config(page_title="Serial & PIP Scanner", layout="centered")
st.title("📷 Serial No (Barcode) & PIP No (QR Code) Scanner")

st.markdown("""
1. Capture an image of a **barcode** (e.g., Serial No).  
2. Capture an image of a **QR code** (e.g., PIP No).  
3. We'll scan and display them in a table.
""")

# --- Helper function to decode image ---
def decode_code(image_file, symbols):
    img = Image.open(image_file)
    img_np = np.array(img)
    gray = cv2.cvtColor(img_np, cv2.COLOR_RGB2GRAY)

    # Resize to improve recognition
    resized = cv2.resize(gray, None, fx=2.0, fy=2.0, interpolation=cv2.INTER_LINEAR)

    # Try decoding with pyzbar
    decoded = decode(resized, symbols=symbols)
    for obj in decoded:
        return obj.data.decode('utf-8'), img
    return None, img

# --- Step 1: Barcode ---
img1 = st.camera_input("Step 1: Capture Barcode (Serial No)")

# --- Step 2: QR Code ---
img2 = st.camera_input("Step 2: Capture QR Code (PIP No)")

# --- Process both ---
if img1 and img2:
    with st.spinner("🔍 Scanning images..."):
        serial, img1_display = decode_code(img1, [ZBarSymbol.CODE128, ZBarSymbol.EAN13, ZBarSymbol.CODE39])
        pip, img2_display = decode_code(img2, [ZBarSymbol.QRCODE])

        if serial and pip:
            st.success("✅ Codes detected successfully!")

            df = pd.DataFrame({
                "Serial No": [serial],
                "PIP No": [pip]
            })
            st.subheader("📋 Scanned Results:")
            st.table(df)

            with st.expander("📸 View Captured Images"):
                st.image(img1_display, caption="Barcode Image", use_column_width=True)
                st.image(img2_display, caption="QR Code Image", use_column_width=True)
        else:
            if not serial:
                st.error("❌ Could not detect barcode (Serial No).")
            if not pip:
                st.error("❌ Could not detect QR code (PIP No).")

elif img1 or img2:
    st.info("📷 Please capture **both images** to proceed.")
