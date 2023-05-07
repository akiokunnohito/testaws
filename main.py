import streamlit as st
import requests
from PIL import Image
import io
import base64

def send_image_to_lambda(base64_image):
    response = requests.post(api_gateway_url, json={"base64_input_image": base64_image})
    return response.json()

def resize_image(image, size=(256, 256)):
    return image.resize(size, Image.LANCZOS)

def image_to_base64(image):
    buffered = io.BytesIO()
    image.save(buffered, format="JPEG")
    return base64.b64encode(buffered.getvalue()).decode()

def base64_to_image(base64_str):
    img_data = base64.b64decode(base64_str)
    return Image.open(io.BytesIO(img_data))

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

    # Add this code after st.text(base64_resized_image)
    decoded_image = base64_to_image(base64_resized_image)
    st.write("Decoded Image:")
    st.image(decoded_image)

    lambda_response = send_image_to_lambda(base64_resized_image)
    st.write("Lambda Response:")
    st.write(lambda_response)

    if "base64_result_image" in lambda_response:
        received_base64_image = lambda_response["base64_result_image"]
        received_image = base64_to_image(received_base64_image)
        st.write("Received Image from Lambda:")
        st.image(received_image)
else:
    st.write("No image file has been uploaded.")
