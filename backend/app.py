from flask import Flask, request, jsonify
import numpy as np
import joblib
import json
import tensorflow as tf
import os

app = Flask(__name__)

# Load model and preprocessors
model = tf.keras.models.load_model("model/disease_model.h5")
scaler = joblib.load("model/scaler.pkl")
label_encoder = joblib.load("model/label_encoder.pkl")

with open("model/features.json", "r") as f:
    features = json.load(f)

@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()
        input_data = [data.get(f, 0) for f in features]

        # Preprocess input
        input_array = np.array(input_data).reshape(1, -1)
        input_scaled = scaler.transform(input_array)

        # Predict
        prediction_probs = model.predict(input_scaled)[0]
        predicted_index = np.argmax(prediction_probs)
        predicted_disease = label_encoder.inverse_transform([predicted_index])[0]
        confidence = float(prediction_probs[predicted_index]) * 100

        return jsonify({
            "prediction": predicted_disease,
            "confidence": f"{confidence:.2f}%"
        })

    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(debug=True)
