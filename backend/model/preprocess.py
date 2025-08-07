import json
import numpy as np
import pandas as pd
import joblib
import os

# Load features list
FEATURES_PATH = os.path.join(os.path.dirname(__file__), 'features.json')
with open(FEATURES_PATH, 'r') as f:
    FEATURES = json.load(f)

# Load pre-fitted scaler
SCALER_PATH = os.path.join(os.path.dirname(__file__), 'scaler.pkl')
scaler = joblib.load(SCALER_PATH)

def preprocess_input(input_data):
    """
    Preprocess user input data.
    
    Parameters:
        input_data (dict): Blood test biomarkers.

    Returns:
        numpy.ndarray: Scaled and ordered feature array.
    """
    # Convert input dictionary to dataframe
    df = pd.DataFrame([input_data])

    # Align dataframe columns as per FEATURES order
    df = df.reindex(columns=FEATURES)

    # Fill any missing values
    df.fillna(0, inplace=True)

    # Scale the data
    scaled_data = scaler.transform(df)

    return scaled_data
