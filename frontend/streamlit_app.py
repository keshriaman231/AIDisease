import streamlit as st
import requests
import json
import os
from PIL import Image

# Load feature list
with open("../backend/model/features.json", "r") as f:
    features = json.load(f)

# Set Streamlit page config
st.set_page_config(page_title="AI Doctor", page_icon="🏥")

st.title("🏥 AI-Powered Disease Predictor")
st.markdown("Upload your health report and get a disease prediction.")

# Basic details
name = st.text_input("👤 Name")
age = st.number_input("🎂 Age", min_value=0, max_value=120, step=1)
gender = st.selectbox("⚧ Gender", ["Male", "Female", "Other"])

# File upload
uploaded_file = st.file_uploader("📄 Upload Report (PDF or Image)", type=["pdf", "png", "jpg", "jpeg"])
if uploaded_file:
    file_ext = os.path.splitext(uploaded_file.name)[1]
    if file_ext in [".png", ".jpg", ".jpeg"]:
        img = Image.open(uploaded_file)
        st.image(img, caption="Uploaded Report", use_column_width=True)
    else:
        st.success("PDF Uploaded Successfully")

st.subheader("📊 Fill Symptoms (1 if present, 0 if not):")
input_data = {}
cols = st.columns(3)
for i, feature in enumerate(features):
    with cols[i % 3]:
        input_data[feature] = st.selectbox(f"{feature.replace('_',' ').capitalize()}", [0, 1], index=0)

# Submit button
if st.button("🧬 Predict Disease"):
    if name and age and gender:
        try:
            response = requests.post("http://127.0.0.1:5000/predict", json=input_data)
            result = response.json()

            if "prediction" in result:
                st.success(f"🧠 Disease Prediction: **{result['prediction']}**")
                st.info(f"📈 Confidence: {result['confidence']}")
                st.markdown(f"🧾 **Patient:** {name}, {age} years, {gender}")
            else:
                st.error("Prediction failed. Check input or server.")
        except Exception as e:
            st.error(f"Error: {str(e)}")
    else:
        st.warning("Please enter your name, age, and gender.")
