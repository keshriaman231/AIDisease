# backend/__init__.py

from flask import Flask
import os

# Initialize Flask app
app = Flask(__name__)

# Optional: Load configurations from a config.py file if needed
app.config.from_object('backend.config.Config')

# Initialize extensions, such as CORS, DB, etc.
# from flask_cors import CORS
# CORS(app)

# Register blueprints here if you have modular components
# from backend.some_module import some_blueprint
# app.register_blueprint(some_blueprint)
