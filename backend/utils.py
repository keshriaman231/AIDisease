# backend/utils.py

import os
import pandas as pd
import numpy as np

# Example: A utility function for reading a CSV file
def read_csv(file_path):
    try:
        data = pd.read_csv(file_path)
        return data
    except Exception as e:
        print(f"Error reading CSV: {e}")
        return None

# Example: A utility function for saving a model
def save_model(model, model_path):
    try:
        model.save(model_path)
        print(f"Model saved at {model_path}")
    except Exception as e:
        print(f"Error saving model: {e}")

# Example: A utility function to normalize data
def normalize_data(data):
    try:
        return (data - data.mean()) / data.std()
    except Exception as e:
        print(f"Error normalizing data: {e}")
        return None

# Example: A function to validate input data (e.g., checking required columns)
def validate_data(data, required_columns):
    missing_columns = [col for col in required_columns if col not in data.columns]
    if missing_columns:
        print(f"Missing columns: {', '.join(missing_columns)}")
        return False
    return True
