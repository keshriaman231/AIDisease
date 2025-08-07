# database/db.py

'''# backend/database/
from backend.config import MONGO_URI, DB_NAME, COLLECTION_NAME


# database/db.py

from pymongo import MongoClient
import os

# Load from environment or config
MONGO_URI = os.getenv('MONGO_URI', "mongodb+srv://admin:admin123@ai-disease-cluster.vvxegv0.mongodb.net/?retryWrites=true&w=majority&appName=ai-disease-cluster")
DB_NAME = os.getenv('DB_NAME', "ai-disease-cluster")
COLLECTION_NAME = os.getenv('COLLECTION_NAME', "user_reports")

# Initialize MongoDB client
try:
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    collection = db[COLLECTION_NAME]
except Exception as e:
    print(f"Error connecting to MongoDB: {e}")
    collection = None

def save_user_report(user_details, biomarkers, prediction):
    """
    Save the user's report to MongoDB.
    
    Parameters:
        user_details (dict): {name, age, gender}
        biomarkers (dict): Blood test biomarkers
        prediction (str): Predicted disease name
        
    Returns:
        str: MongoDB inserted ID
    """
    if collection is None:
        raise Exception("Database connection not established.")

    document = {
        "user_details": user_details,
        "biomarkers": biomarkers,
        "predicted_disease": prediction
    }
    result = collection.insert_one(document)
    return str(result.inserted_id)'''


'''# backend/database/db.py

from pymongo import MongoClient
# from backend.config import Config
from config import Config

# Load config values
MONGO_URI = Config.MONGO_URI
DB_NAME = Config.DB_NAME
COLLECTION_NAME = Config.COLLECTION_NAME

# Initialize MongoDB client
try:
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    collection = db[COLLECTION_NAME]
    print("✅ MongoDB connection established in db.py")
except Exception as e:
    print(f"❌ Error connecting to MongoDB in db.py: {e}")
    collection = None

def save_user_report(user_details, biomarkers, prediction):
    """
    Save the user's report to MongoDB.
    
    Parameters:
        user_details (dict): {name, age, gender}
        biomarkers (dict): Blood test biomarkers
        prediction (str): Predicted disease name
        
    Returns:
        str: MongoDB inserted ID
    """
    if collection is None:
        raise Exception("Database connection not established.")

    document = {
        "user_details": user_details,
        "biomarkers": biomarkers,
        "predicted_disease": prediction
    }
    result = collection.insert_one(document)
    return str(result.inserted_id)'''

#database/db.py

import os
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, OperationFailure
from datetime import datetime

# --- 1. DATABASE CONFIGURATION ---
# To keep things simple, we'll define the configuration directly here.
# IMPORTANT: Replace the placeholder with your actual MongoDB Atlas connection string.
MONGO_URI = os.getenv('MONGO_URI', "YOUR_MONGODB_ATLAS_CONNECTION_STRING")
DATABASE_NAME = "disease_predictor_db"
COLLECTION_NAME = "prediction_reports"

# --- 2. DATABASE CONNECTION ---
# This improved logic attempts to connect and handles failures gracefully.
try:
    print("Attempting to connect to MongoDB Atlas...")
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
    # The ismaster command is cheap and does not require auth, used to check connection.
    client.admin.command('ismaster')
    db = client[DATABASE_NAME]
    collection = db[COLLECTION_NAME]
    print("✅ MongoDB connection successful.")
except ConnectionFailure as e:
    print(f"❌ FATAL ERROR: Could not connect to MongoDB. Please check your MONGO_URI.")
    print(f"Details: {e}")
    collection = None # Set collection to None if connection fails
except Exception as e:
    print(f"❌ An unexpected error occurred during MongoDB connection: {e}")
    collection = None

# --- 3. SAVE REPORT FUNCTION ---
def save_prediction_report(report_data):
    """
    Saves a complete prediction report document to the MongoDB collection.

    This function is designed to be safe and will not crash the app if the
    database connection is unavailable.

    Args:
        report_data (dict): A dictionary containing all information to be saved,
                            including patient details, symptoms, and the prediction.
    
    Returns:
        bool: True if the report was saved successfully, False otherwise.
    """
    # First, check if the database connection was established successfully at startup.
    if collection is None:
        print("❌ Could not save report: Database connection is not available.")
        return False
        
    try:
        # Add a timestamp to the report for tracking when it was created.
        report_data["createdAt"] = datetime.utcnow()
        
        # Insert the complete document into the collection.
        result = collection.insert_one(report_data)
        print(f"✅ Report saved successfully to MongoDB with ID: {result.inserted_id}")
        return True
    except OperationFailure as e:
        # This handles errors during the database write operation (e.g., permissions).
        print(f"❌ Could not save report: A database operation error occurred.")
        print(f"Details: {e}")
        return False
    except Exception as e:
        # Catch any other unexpected errors.
        print(f"❌ An unexpected error occurred while saving the report: {e}")
        return False

