import streamlit as st
from PIL import Image
import numpy as np
import cv2
from pyzbar.pyzbar import decode, ZBarSymbol

st.set_page_config(page_title="Barcode & QR Scanner", layout="centered")
st.title("📷 Barcode/QR Code Scanner")

st.markdown("""
Capture a **clear image** of a barcode or QR code using your webcam. This app will try everything it can to decode it—even if it’s tiny, tilted, or tricky!
""")

img_file = st.camera_input("Step 1: Snap a barcode or QR code")

if img_file is not None:
    # Convert to OpenCV grayscale image
    img = Image.open(img_file)
    img_np = np.array(img)
    img_gray = cv2.cvtColor(img_np, cv2.COLOR_RGB2GRAY)

    # Resize image to help with small codes
    scale_percent = 250  # Increase resolution
    width = int(img_gray.shape[1] * scale_percent / 100)
    height = int(img_gray.shape[0] * scale_percent / 100)
    img_resized = cv2.resize(img_gray, (width, height), interpolation=cv2.INTER_LINEAR)

    # Enhance contrast using CLAHE
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    img_enhanced = clahe.apply(img_resized)

    # Apply adaptive thresholding
    img_thresh = cv2.adaptiveThreshold(
        img_enhanced, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY, 11, 2
    )

    found = False

    # Try rotating the image in 4 orientations
    for angle in [0, 90, 180, 270]:
        rotated = np.rot90(img_thresh, k=angle // 90)
        decoded_objs = decode(rotated, symbols=[ZBarSymbol.QRCODE, ZBarSymbol.CODE128, ZBarSymbol.EAN13])
        if decoded_objs:
            st.success(f"✅ Detected {len(decoded_objs)} code(s):")
            for obj in decoded_objs:
                st.subheader(f"{obj.type} detected")
                st.code(obj.data.decode('utf-8'))
            found = True
            break

    # Fallback: OpenCV QR multi-detector
    if not found:
        qr_detector = cv2.QRCodeDetector()
        retval, decoded_info, points, _ = qr_detector.detectAndDecodeMulti(img_thresh)
        if retval:
            st.success(f"✅ Detected {len(decoded_info)} QR code(s) with OpenCV:")
            for i, data in enumerate(decoded_info):
                if data:
                    st.subheader(f"QR Code {i+1}")
                    st.code(data)
            found = True

    if not found:
        st.error("❌ No barcode or QR code could be detected. Try again with better lighting or zoom in a bit.")

    st.image(img, caption="Captured Image")
