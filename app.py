import streamlit as st
from PIL import Image
import requests
import io

st.title("📷 QR/Barcode Scanner (Cloud API)")

st.write("Capture a barcode or QR code. This app will send it to an API and decode the contents.")

img_file = st.camera_input("Capture Image")

if img_file is not None:
    st.image(img_file, caption="Captured Image")

    with st.spinner("Scanning..."):
        # Convert uploaded image to bytes
        image_bytes = img_file.getvalue()
        files = {'file': ("scan.png", image_bytes, "image/png")}

        # Send to QRServer API (also detects barcodes)
        response = requests.post("https://api.qrserver.com/v1/read-qr-code/", files=files)

        if response.ok:
            results = response.json()
            try:
                symbol_data = results[0]["symbol"][0]
                if symbol_data["data"]:
                    st.success("Code Detected:")
                    st.write(f"**Data:** {symbol_data['data']}")
                    st.write(f"**Type:** {symbol_data['type']}")
                else:
                    st.warning("No code found in the image.")
            except Exception:
                st.error("Error parsing response.")
        else:
            st.error("Failed to connect to the QR/barcode decoding API.")
