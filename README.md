🧠 AI Disease Prediction Web App ->

>>A full-stack AI-powered medical diagnosis system using blood biomarkers and symptoms to predict diseases using a deep learning model. Built with TensorFlow, Flask, and Streamlit.

📁 Project Structure ->

AI-Disease-Prediction/
├── backend/
│   ├── app.py
│   └── model/
│       ├── disease_model.h5
│       ├── scaler.pkl
│       ├── label_encoder.pkl
│       └── features.json
├── frontend/
│   └── streamlit_app.py
├── dataset/
│   ├── Training.csv
│   └── Testing.csv
├── requirements.txt
├── README.md
└── .gitignore
--------------------------------------------------------------------------------------------------------------------------


⚙️ Setup Instructions (Run Locally) ->

🐍 1. Create & Activate Virtual Environment
>>python -m venv venv
# Activate:
# Windows:
>>venv\Scripts\activate
# macOS/Linux:
>>source venv/bin/activate

⚠️ Why It’s Important:
Reason	Explanation
>>🧼 Isolates dependencies	Avoids version conflicts with globally installed Python packages
>>💥 Prevents crashes	Different TensorFlow, scikit-learn, etc., versions won’t break other projects
>>📦 Clean install	Guarantees that only the dependencies in requirements.txt are used
>>💻 Works cross-platform	Ensures consistent behavior on Windows/Linux/Mac

💡 *Note: Creating a virtual environment is optional but strongly recommended to avoid dependency issues.*



📦 2. Install Dependencies 
>>pip install -r requirements.txt


🚀 Running the Application ->
🔁 Backend (Flask API)

>>cd backend
>>python app.py

>>Runs at: http://127.0.0.1:5000


🎨 Frontend (Streamlit UI) ->

>>cd frontend
>>streamlit run streamlit_app.py

>>Opens at: http://localhost:8501


🧪 Sample Inputs for Testing ->

@✅ Diabetes

{
  "irregular_sugar_level": 1,
  "constipation": 1,
  "fatigue": 1,
  "weight_loss": 1,
  "increased_appetite": 1
}

@✅ Jaundice

{
  "yellowish_skin": 1,
  "dark_urine": 1,
  "abdominal_pain": 1,
  "fatigue": 1
}


🚧 Future Enhancements

    ✅ Blood Report Upload Support
    Allow users to upload PDF/CSV/Image reports. These will be automatically scanned to extract biomarker features using OCR and AI.

    ✅ Automated Feature Extraction
    Convert scanned reports into structured symptom/biomarker inputs using NLP + Vision (Tesseract, OpenCV, Pandas).

    ✅ Prediction with Accuracy Scores
    Enhance the frontend to show predicted disease with confidence percentage for greater transparency.

    ✅ Explainable AI (XAI) Integration
    Use SHAP or LIME to visually explain which biomarkers/symptoms led to the prediction.

    ✅ Authentication & Dashboard
    Add user login, health history, and downloadable report results for doctors and patients.

