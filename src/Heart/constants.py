"""Project-wide constants for features, validation, and risk thresholds."""

FEATURE_NAMES = [
    "age", "sex", "cp", "trestbps", "chol", "fbs", "restecg",
    "thalach", "exang", "oldpeak", "slope", "ca", "thal",
]

FEATURE_LABELS = {
    "age": "Age",
    "sex": "Sex",
    "cp": "Chest Pain Type",
    "trestbps": "Resting Blood Pressure",
    "chol": "Serum Cholesterol",
    "fbs": "Fasting Blood Sugar",
    "restecg": "Resting ECG Results",
    "thalach": "Max Heart Rate",
    "exang": "Exercise Angina",
    "oldpeak": "ST Depression (Oldpeak)",
    "slope": "ST Slope",
    "ca": "Major Vessels (Fluoroscopy)",
    "thal": "Thalassemia",
}

# Valid input ranges aligned with the UCI Cleveland heart dataset.
VALIDATION_RULES = {
    "age": {"min": 18, "max": 100, "type": int},
    "sex": {"min": 0, "max": 1, "type": int},
    "cp": {"min": 0, "max": 3, "type": int},
    "trestbps": {"min": 80, "max": 220, "type": int},
    "chol": {"min": 100, "max": 600, "type": int},
    "fbs": {"min": 0, "max": 1, "type": int},
    "restecg": {"min": 0, "max": 2, "type": int},
    "thalach": {"min": 60, "max": 220, "type": int},
    "exang": {"min": 0, "max": 1, "type": int},
    "oldpeak": {"min": 0.0, "max": 10.0, "type": float},
    "slope": {"min": 0, "max": 2, "type": int},
    "ca": {"min": 0, "max": 3, "type": int},
    "thal": {"min": 3, "max": 7, "type": int, "allowed": [3, 6, 7]},
}

RISK_THRESHOLDS = {"low_max": 30, "moderate_max": 70}

MEDICAL_DISCLAIMER = (
    "This tool is for educational and research purposes only. "
    "It is not a substitute for professional medical advice, diagnosis, or treatment. "
    "Always consult a qualified healthcare provider for medical concerns."
)
