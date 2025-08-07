# test_mongo.py

from pymongo import MongoClient
from config import Config

client = MongoClient(Config.MONGO_URI)

try:
    db = client[Config.DB_NAME]
    collection = db[Config.COLLECTION_NAME]
    # Try to insert dummy data
    collection.insert_one({"test": "connection successful"})
    print("✅ MongoDB connection successful. Test document inserted.")
except Exception as e:
    print("❌ MongoDB connection failed:", e)
