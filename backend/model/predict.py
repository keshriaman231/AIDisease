# predict.py

import os
import joblib
import numpy as np
import tensorflow as tf

# Load trained model
MODEL_PATH = os.path.join(os.path.dirname(__file__), 'disease_model.h5')
model = tf.keras.models.load_model(MODEL_PATH)

# Load label encoder
LABEL_ENCODER_PATH = os.path.join(os.path.dirname(__file__), 'label_encoder.pkl')
label_encoder = joblib.load(LABEL_ENCODER_PATH)

def predict_disease(processed_input):
    """
    Predict disease from processed input.
    
    Args:
        processed_input (numpy array): Preprocessed input biomarkers.

    Returns:
        str: Predicted disease name.
    """
    preds = model.predict(processed_input)
    pred_class = np.argmax(preds, axis=1)
    disease_name = label_encoder.inverse_transform(pred_class)[0]
    return disease_name
