import streamlit as st
from PIL import Image
import numpy as np
import cv2
from pyzbar.pyzbar import decode, ZBarSymbol

st.set_page_config(page_title="Barcode & QR Scanner", layout="centered")
st.title("📷 Barcode/QR Code Scanner")

st.markdown("""
Capture a clear image of a barcode or QR code using your webcam. This app will attempt to decode the content automatically.
""")

img_file = st.camera_input("Step 1: Capture a barcode or QR code")

if img_file is not None:
    # Load image and convert to OpenCV grayscale
    img = Image.open(img_file)
    img_np = np.array(img)
    img_gray = cv2.cvtColor(img_np, cv2.COLOR_RGB2GRAY)

    # Decode with pyzbar (supports QR, Code128, EAN-13, etc.)
    decoded_objs = decode(img_gray, symbols=[ZBarSymbol.QRCODE, ZBarSymbol.CODE128, ZBarSymbol.EAN13])

    if decoded_objs:
        st.success(f"✅ Detected {len(decoded_objs)} code(s):")
        for obj in decoded_objs:
            code_type = obj.type
            data = obj.data.decode("utf-8")
            st.subheader(f"{code_type} detected")
            st.code(data, language="text")
        st.image(img, caption="Captured Image")
    else:
        # Try OpenCV QR detector as a fallback
        qr_detector = cv2.QRCodeDetector()
        data, bbox, _ = qr_detector.detectAndDecode(img_gray)

        if data:
            st.success("✅ QR Code detected with OpenCV:")
            st.code(data, language="text")
            st.image(img, caption="Captured Image")
        else:
            st.error("❌ No barcode or QR code could be detected.")
