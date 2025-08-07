'''# frontend/streamlit_app.py

import streamlit as st
import requests
import pandas as pd
from io import StringIO
import json

# Flask backend API endpoint
API_URL = "http://localhost:5000/predict"  # Change this to your Flask backend URL if hosted

def predict_disease(user_details, biomarkers):
    try:
        # Prepare the data payload
        payload = {
            'user_details': user_details,
            'biomarkers': biomarkers
        }

        # Make a POST request to the Flask API
        response = requests.post(API_URL, json=payload)
        response_data = response.json()

        # Return the predicted disease
        return response_data['prediction'] if 'prediction' in response_data else None

    except Exception as e:
        st.error(f"Error in prediction: {e}")
        return None


# Streamlit App UI
def main():
    st.title("AI-Powered Disease Prediction System")

    # User details input form
    with st.form(key="user_details_form"):
        name = st.text_input("Enter your Name")
        age = st.number_input("Enter your Age", min_value=1, max_value=120)
        gender = st.selectbox("Select Gender", ["Male", "Female", "Other"])
        submit_button = st.form_submit_button("Submit")

    # Blood test report upload form
    st.subheader("Upload Your Blood Test Report (CSV or PDF)")
    file = st.file_uploader("Choose a file", type=["csv", "pdf"])

    if submit_button and file is not None:
        # Convert the uploaded CSV into biomarkers data
        if file.type == "text/csv":
            # Read CSV data into pandas DataFrame
            df = pd.read_csv(file)
            biomarkers = df.to_dict(orient="records")  # Convert DataFrame to list of dicts
        else:
            # Placeholder for handling PDF file (e.g., using a PDF parser later)
            st.warning("PDF upload is not yet supported. Please upload a CSV file.")
            biomarkers = []

        if biomarkers:
            # Prepare user details
            user_details = {"name": name, "age": age, "gender": gender}

            # Predict disease using Flask backend
            prediction = predict_disease(user_details, biomarkers)
            if prediction:
                st.success(f"The predicted disease is: {prediction}")
            else:
                st.error("Prediction failed. Please check your inputs and try again.")
        else:
            st.error("Please upload a valid blood test report.")

if __name__ == "__main__":
    main()'''

# frontend/streamlit_app.py

import streamlit as st
import requests
import json
import os

# --- 1. CONFIGURATION ---
st.set_page_config(
    page_title="AI Disease Predictor",
    page_icon="🩺",
    layout="wide"
)

# --- 2. LOAD SYMPTOM FEATURES ---
# This function loads the list of symptoms from the features.json file
# which is expected to be in the backend/model directory.
def load_symptom_features():
    """
    Loads the list of feature names (symptoms) from the JSON file.
    """
    # This path assumes the 'frontend' and 'backend' folders are in the same root directory.
    # Adjust the path if your project structure is different.
    # Project Root -> backend -> model -> features.json
    features_path = os.path.join(os.path.dirname(__file__), '..', 'backend', 'model', 'features.json')
    
    try:
        with open(features_path, 'r') as f:
            features = json.load(f)
        print("✅ Symptom features loaded successfully.")
        return features
    except FileNotFoundError:
        st.error(f"Fatal Error: The symptom list file 'features.json' was not found.")
        st.error(f"Please ensure the file exists at: {features_path}")
        return None
    except json.JSONDecodeError:
        st.error("Fatal Error: 'features.json' is not a valid JSON file.")
        return None

# --- 3. MAIN APPLICATION UI ---
def main():
    """
    Renders the main Streamlit application UI.
    """
    st.title("🩺 AI-Powered Disease Predictor")
    st.markdown("Enter your details and select your symptoms (1 for Yes, 0 for No) to get a prediction.")
    
    # Load the list of symptoms
    symptoms_list = load_symptom_features()
    
    # Only proceed if the symptoms were loaded successfully
    if symptoms_list:
        # Use a form to group inputs and have a single submission button
        with st.form(key="prediction_form"):
            
            # --- User Details Section ---
            st.subheader("Patient Information")
            col1, col2, col3 = st.columns(3)
            with col1:
                name = st.text_input("Enter Your Name", placeholder="e.g., John Doe")
            with col2:
                age = st.number_input("Enter Your Age", min_value=1, max_value=120, step=1)
            with col3:
                gender = st.selectbox("Select Gender", ["Male", "Female", "Other"])

            st.markdown("---")
            
            # --- Symptom Selection Section ---
            st.subheader("Select Your Symptoms")
            
            symptom_inputs = {}
            # Use 4 columns for a cleaner layout
            num_columns = 4
            cols = st.columns(num_columns)
            
            # Dynamically create a select box for each symptom
            for i, symptom in enumerate(symptoms_list):
                # Format symptom name for better readability (e.g., 'skin_rash' -> 'Skin Rash')
                display_name = symptom.replace('_', ' ').title()
                symptom_inputs[symptom] = cols[i % num_columns].selectbox(
                    display_name, 
                    options=[0, 1], 
                    format_func=lambda x: "No" if x == 0 else "Yes",
                    key=symptom
                )
            
            # Form submission button
            st.markdown("---")
            submit_button = st.form_submit_button("Predict Disease")

        # --- Handle Form Submission ---
        if submit_button:
            if not name or age <= 0:
                st.warning("Please enter a valid name and age.")
            else:
                with st.spinner("Analyzing your symptoms..."):
                    # Create the list of symptom values in the correct order
                    symptom_values = [symptom_inputs[symptom] for symptom in symptoms_list]
                    
                    # Define the backend API URL
                    api_url = "http://127.0.0.1:5000/predict"
                    
                    # Prepare the JSON payload for the API
                    payload = {"symptoms": symptom_values}
                    
                    try:
                        # Send the POST request to the backend
                        response = requests.post(api_url, json=payload, timeout=10)
                        response.raise_for_status()  # Raise an error for bad status codes (4xx or 5xx)
                        
                        result = response.json()
                        
                        if "error" in result:
                            st.error(f"An error occurred: {result['error']}")
                        else:
                            prediction = result.get('prediction', 'N/A')
                            confidence = result.get('confidence', 'N/A')
                            
                            st.success(f"**Disease Prediction: {prediction}**")
                            st.info(f"**Confidence Score: {confidence}%**")
                            st.markdown(f"**Patient:** {name}, {age} years old, {gender}")
                            st.balloons()

                    except requests.exceptions.ConnectionError:
                        st.error(f"Connection Error: Could not connect to the backend API at {api_url}.")
                        st.error("Please make sure the Flask backend server is running.")
                    except requests.exceptions.RequestException as e:
                        st.error(f"An error occurred while making the request: {e}")

if __name__ == "__main__":
    main()