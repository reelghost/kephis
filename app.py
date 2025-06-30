import streamlit as st
from PIL import Image
import numpy as np
from pyzbar.pyzbar import decode


st.title("Barcode/QR Code Scanner")

st.write("""
This app uses your webcam to capture an image, then scans for barcodes or QR codes and displays the decoded contents.
""")

img_file = st.camera_input("Capture a barcode or QR code")

if img_file is not None:
    img = Image.open(img_file)
    img_np = np.array(img)
    decoded_objs = decode(img_np)
    if decoded_objs:
        st.success(f"Found {len(decoded_objs)} code(s):")
        for obj in decoded_objs:
            code_type = obj.type.upper()
            if code_type == "QRCODE":
                st.subheader("QR Code detected:")
            else:
                st.subheader(f"Barcode detected: {code_type}")
            st.write(f"**Data:** {obj.data.decode('utf-8')}")
        st.image(img, caption="Captured Image")
    else:
        st.error("No barcode or QR code detected in the image.")
