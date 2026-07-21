import streamlit as st
import numpy as np
import cv2
import os
import gdown
from tensorflow.keras.models import load_model
from PIL import Image

st.set_page_config(page_title="Alzheimer's Disease Predictor", page_icon="🧠", layout="centered")

# Must match the label order used in train.py's `categories` list
CLASS_NAMES = ["AD (Alzheimer's Disease)", "CN (Cognitively Normal)",
               "EMCI (Early Mild Cognitive Impairment)",
               "LMCI (Late Mild Cognitive Impairment)",
               "MCI (Mild Cognitive Impairment)"]

MODEL_PATH = "alzheimer_model.h5"

@st.cache_resource
def get_model():
    if not os.path.exists(MODEL_PATH):
        with st.spinner("Downloading model... Please wait."):
            file_id = "1kdllxj4fEKt1ysGaOzNFFZspnudhQ72O"
            url = f"https://drive.google.com/uc?id={file_id}"
            gdown.download(url, MODEL_PATH, quiet=False)

    return load_model(MODEL_PATH)

model = get_model()

st.title("🧠 Alzheimer's Disease Predictor")
st.write("Upload a brain MRI scan (JPEG) to classify its cognitive stage.")

uploaded_file = st.file_uploader("Choose an image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Read the uploaded file into an OpenCV-compatible array
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    img_bgr = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

    st.image(cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB), caption="Uploaded Scan", use_column_width=True)

    # --- Preprocessing must exactly mirror train.py ---
    gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
    gray = gray / 255.0
    gray = cv2.resize(gray, (240, 240))
    input_array = gray.reshape(1, 240, 240, 1)

    with st.spinner("Analyzing scan..."):
        prediction = model.predict(input_array)

    predicted_idx = int(np.argmax(prediction))
    confidence = float(np.max(prediction)) * 100

    st.subheader(f"Prediction: {CLASS_NAMES[predicted_idx]}")
    st.write(f"Confidence: {confidence:.2f}%")

    st.bar_chart({name: float(prob) for name, prob in zip(CLASS_NAMES, prediction[0])})

    st.caption("⚠️ This is a research/educational tool, not a medical diagnosis.")
else:
    st.info("Please upload an image to get a prediction.")