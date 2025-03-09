import streamlit as st
import cv2
import numpy as np
import zipfile
import os
from io import BytesIO

# Function to upscale an image using bicubic interpolation
def upscale_image(image, scale_factor):
    height, width = image.shape[:2]
    new_width = int(width * scale_factor)
    new_height = int(height * scale_factor)
    upscaled_image = cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_CUBIC)
    return upscaled_image

# Streamlit UI
st.title("Image Upscaler using Bicubic Interpolation")

st.write("Upload images, set the scaling factor, and download the upscaled images.")

# File uploader
uploaded_files = st.file_uploader("Upload Images", type=["png", "jpg", "jpeg"], accept_multiple_files=True)

# Scale factor input
scale_factor = st.number_input("Enter upscale factor (e.g., 2 for 2x, 3 for 3x, etc.)", min_value=1, value=2, step=1)

if uploaded_files and scale_factor:
    upscaled_images = []
    zip_buffer = BytesIO()

    with zipfile.ZipFile(zip_buffer, "w") as zip_file:
        for uploaded_file in uploaded_files:
            # Convert uploaded file to OpenCV format
            file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
            image = cv2.imdecode(file_bytes, cv2.IMREAD_UNCHANGED)
            
            # Upscale the image
            upscaled_image = upscale_image(image, scale_factor)
            
            # Convert back to byte format
            _, img_encoded = cv2.imencode(".png", upscaled_image)
            img_bytes = img_encoded.tobytes()
            
            # Save to zip
            zip_file.writestr(f"upscaled_{uploaded_file.name}", img_bytes)

    # Prepare download button
    zip_buffer.seek(0)
    st.download_button("Download Upscaled Images", zip_buffer, "upscaled_images.zip", "application/zip")
