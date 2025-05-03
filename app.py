import streamlit as st
from PIL import Image
from detector import load_model, detect_faces
from webcam import run_webcam

st.set_page_config(page_title="Face Mask Detection", layout="centered")
st.title("😷 Face Mask Detection using YOLOv5")

option = st.radio("Choose Input Type", ["Upload Image", "Use Webcam"])

model = load_model("models/best.pt")

if option == "Upload Image":
    uploaded_file = st.file_uploader("Upload an Image", type=["jpg", "jpeg", "png"])
    if uploaded_file:
        image = Image.open(uploaded_file).convert("RGB")
        st.image(image, caption="Uploaded Image", use_column_width=True)
        st.write("Processing...")
        result_img = detect_faces(model, image)
        st.image(result_img, caption="Detection Result", use_column_width=True)

elif option == "Use Webcam":
    st.warning("Click below to launch the webcam in a new window (Press 'Q' to quit).")
    if st.button("Start Webcam Detection"):
        run_webcam(model)