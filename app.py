import streamlit as st
from pylibdmtx.pylibdmtx import decode as dmtx_decode
from PIL import Image
import numpy as np
import cv2
import pandas as pd
from pyzbar.pyzbar import decode as pyzbar_decode, ZBarSymbol

st.set_page_config(page_title="Serial & PIP Scanner", layout="centered")
st.title("📷 Serial No (Barcode) & PIP No (QR Code) Scanner")

st.markdown("""
1. Upload an image of a **barcode** (e.g., Serial No).  
2. Upload an image of a **QR code** (e.g., PIP No).  
3. We'll scan and display them in a table.
""")

# --- QR Code Decoder ---
def decode_datamatrix(image_file):
    """
    Decodes Data Matrix codes from an image file using pylibdmtx,
    with preprocessing to improve recognition.

    Parameters:
        image_file: Uploaded file-like object

    Returns:
        list: A list of decoded Data Matrix code strings
    """
    # Load image
    img = Image.open(image_file)

    # Ensure RGB format
    if img.mode != "RGB":
        img = img.convert("RGB")

    # Convert to NumPy and enhance contrast
    img_np = np.array(img)
    gray = cv2.cvtColor(img_np, cv2.COLOR_RGB2GRAY)
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Convert back to PIL for dmtx
    preprocessed_img = Image.fromarray(thresh)

    # Decode
    results = dmtx_decode(preprocessed_img)
    return [r.data.decode("utf-8") for r in results]



# --- Barcode Decoder ---
def decode_barcode(frame):
    """
    Decodes barcodes in the given image frame.
    Returns:
        list: A list of decoded barcode data.
    """
    decoded_objects = pyzbar_decode(frame, symbols=[ZBarSymbol.CODE128, ZBarSymbol.EAN13, ZBarSymbol.CODE39])
    return [obj.data.decode('utf-8') for obj in decoded_objects]

# --- Image Processor ---
def process_image(image_file):
    img = Image.open(image_file)

    # Ensure it's in RGB mode
    if img.mode != "RGB":
        img = img.convert("RGB")

    img_np = np.array(img)
    gray = cv2.cvtColor(img_np, cv2.COLOR_RGB2GRAY)
    resized = cv2.resize(gray, None, fx=2.0, fy=2.0, interpolation=cv2.INTER_LINEAR)
    return resized, img


# --- Step 1: Barcode ---
img1 = st.file_uploader("Step 1: Upload Barcode Image (Serial No)", type=["jpg", "jpeg", "png"])

# --- Step 2: QR Code ---
img2 = st.file_uploader("Step 2: Upload QR Code Image (PIP No)", type=["jpg", "jpeg", "png"])

# --- Process both ---
if img1 and img2:
    with st.spinner("🔍 Scanning images..."):
        frame1, display1 = process_image(img1)
        frame2, display2 = process_image(img2)

        barcode_data = decode_barcode(frame1)
        qr_data = decode_datamatrix(img2)

        serial = barcode_data[0] if barcode_data else None
        pip = qr_data[0] if qr_data else None

        if serial and pip:
            st.success("✅ Codes detected successfully!")

            df = pd.DataFrame({
                "Serial No": [serial],
                "PIP No": [pip]
            })
            st.subheader("📋 Scanned Results:")
            st.table(df)

        else:
            if not serial:
                st.error("❌ Could not detect barcode (Serial No).")
            if not pip:
                st.error("❌ Could not detect QR code (PIP No).")

elif img1 or img2:
    st.info("📂 Please upload **both images** to proceed.")
