'''from flask import Flask, request, jsonify
from model.predict import predict_disease
from model.preprocess import preprocess_input
from database.db import save_user_report
import json
import os

app.config.from_object('backend.config.Config')  

# Load Features List (needed for validation)
FEATURES_PATH = os.path.join(os.path.dirname(__file__), 'model', 'features.json')
with open(FEATURES_PATH, 'r') as f:
    FEATURES = json.load(f)

app = Flask(__name__)

def validate_input(biomarkers, FEATURES):
    missing = [feature for feature in FEATURES if feature not in biomarkers]
    return missing

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        user_details = data['user_details']
        biomarkers = data['biomarkers']

        missing = validate_input(biomarkers, FEATURES)
        if missing:
            return jsonify({"error": f"Missing features: {missing}"}), 400

        processed_input = preprocess_input(biomarkers)
        prediction = predict_disease(processed_input)

        save_user_report(user_details, biomarkers, prediction)

        return jsonify({"prediction": prediction})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5001)'''

'''from flask import Flask, request, jsonify
from model.predict import predict_disease
from model.preprocess import preprocess_input
from database.db import save_user_report
import json
import os

# Initialize app first
app = Flask(__name__)
# app.config.from_object('backend.config.Config')  # ✅ Moved after app = Flask(...)
app.config.from_object('config.Config')

# Load Features List (needed for validation)
FEATURES_PATH = os.path.join(os.path.dirname(__file__), 'model', 'features.json')
with open(FEATURES_PATH, 'r') as f:
    FEATURES = json.load(f)

def validate_input(biomarkers, FEATURES):
    missing = [feature for feature in FEATURES if feature not in biomarkers]
    return missing

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        user_details = data['user_details']
        biomarkers = data['biomarkers']

        missing = validate_input(biomarkers, FEATURES)
        if missing:
            return jsonify({"error": f"Missing features: {missing}"}), 400

        processed_input = preprocess_input(biomarkers)
        prediction = predict_disease(processed_input)

        save_user_report(user_details, biomarkers, prediction)

        return jsonify({"prediction": prediction})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5001)'''

# backend/app.py

import os
import joblib
import json
import numpy as np
from flask import Flask, request, jsonify
from tensorflow.keras.models import load_model

# --- 1. INITIALIZE FLASK APP ---
app = Flask(__name__)

# --- 2. LOAD MODEL AND PREPROCESSING FILES ---
def load_all_models():
    """
    Loads the Keras model, scaler, and label encoder from the 'model' directory.
    """
    base_dir = os.path.dirname(os.path.abspath(__file__))
    model_dir = os.path.join(base_dir, 'model')
    
    model_path = os.path.join(model_dir, 'disease_model.h5')
    scaler_path = os.path.join(model_dir, 'scaler.pkl')
    label_encoder_path = os.path.join(model_dir, 'label_encoder.pkl')

    try:
        model = load_model(model_path)
        scaler = joblib.load(scaler_path)
        label_encoder = joblib.load(label_encoder_path)
        
        print("✅ Model and preprocessing objects loaded successfully!")
        return model, scaler, label_encoder

    except FileNotFoundError as e:
        print(f"❌ FATAL ERROR: A required model file was not found. Details: {e}")
        return None, None, None
    except Exception as e:
        print(f"❌ FATAL ERROR: An error occurred during model loading. Details: {e}")
        return None, None, None

keras_model, scaler, label_encoder = load_all_models()


# --- 3. DEFINE THE PREDICTION API ENDPOINT ---
@app.route('/predict', methods=['POST'])
def predict():
    """
    Handles the prediction request from the frontend.
    """
    if not all([keras_model, scaler, label_encoder]):
        return jsonify({
            "error": "Server is not ready. Model files could not be loaded. Please check server logs."
        }), 500

    data = request.get_json()
    if not data or 'symptoms' not in data:
        return jsonify({"error": "Invalid input. Request must include a 'symptoms' key."}), 400

    try:
        symptoms = data['symptoms']
        
        # --- PREDICTION LOGIC ---
        input_array = np.array(symptoms).reshape(1, -1)
        input_scaled = scaler.transform(input_array)
        prediction_probabilities = keras_model.predict(input_scaled)
        predicted_index = np.argmax(prediction_probabilities[0])
        confidence = float(np.max(prediction_probabilities[0]))
        predicted_disease = label_encoder.inverse_transform([predicted_index])[0]
        
        # --- SUCCESS RESPONSE ---
        return jsonify({
            "prediction": predicted_disease,
            "confidence": f"{confidence * 100:.2f}"
        })

    except Exception as e:
        print(f"❌ An error occurred during prediction: {e}")
        return jsonify({"error": "An internal server error occurred."}), 500


# --- 4. RUN THE FLASK APP ---
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
