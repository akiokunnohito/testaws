import streamlit as st
import requests
from PIL import Image
import base64
import io

def resize_image(image, size=(256, 256)):
    return image.resize(size, Image.LANCZOS)

def image_to_base64(image):
    buffered = io.BytesIO()
    image.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    return img_str

# Replace the URL below with the Invoke URL from your API Gateway
api_gateway_url = "https://tf10zezfri.execute-api.ap-southeast-2.amazonaws.com/test/processimage"

def send_image_data_to_lambda(base64_image):
    response = requests.post(api_gateway_url, json={"image_data": base64_image})
    return response.json()

st.title("Image Upload and Resize Test Application")

uploaded_file = st.file_uploader("Upload an image file", type=["jpg", "png"])

if uploaded_file is not None:
    input_image = Image.open(uploaded_file)
    st.write("Original Image:")
    st.image(input_image)

    resized_image = resize_image(input_image)
    st.write("Resized Image (256px x 256px):")
    st.image(resized_image)

    base64_resized_image = image_to_base64(resized_image)
    st.write("Base64 Encoded Resized Image:")
    st.text(base64_resized_image)

    # Send the serialized image data to the Lambda function
    lambda_response = send_image_data_to_lambda(base64_resized_image)
    st.write("Lambda Response:")
    st.write(lambda_response)
else:
    st.write("No image file has been uploaded.")
