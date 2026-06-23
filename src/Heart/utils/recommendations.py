"""Personalized lifestyle recommendations based on predicted risk level."""

from src.Heart.constants import MEDICAL_DISCLAIMER


LOW_RISK = [
    "Maintain a balanced diet rich in fruits, vegetables, and whole grains.",
    "Exercise at least 150 minutes per week with moderate activity.",
    "Schedule routine health check-ups every 12 months.",
    "Limit processed foods, salt, and added sugars.",
    "Stay hydrated and manage stress through mindfulness or hobbies.",
]

MODERATE_RISK = [
    "Consult your physician for a comprehensive cardiovascular screening.",
    "Reduce sodium intake and monitor blood pressure weekly.",
    "Increase aerobic exercise gradually under medical guidance.",
    "Track cholesterol levels and discuss lipid management options.",
    "Avoid smoking and limit alcohol consumption.",
    "Maintain a heart-healthy diet such as DASH or Mediterranean style.",
]

HIGH_RISK = [
    "Seek immediate consultation with a cardiologist or healthcare provider.",
    "Follow prescribed medications and treatment plans strictly.",
    "Monitor blood pressure, heart rate, and symptoms daily.",
    "Adopt a low-sodium, low-saturated-fat diet immediately.",
    "Avoid strenuous activity until cleared by a medical professional.",
    "Ensure emergency contacts and care plans are in place.",
]


def categorize_risk(risk_percent: float) -> str:
    if risk_percent <= 30:
        return "Low Risk"
    if risk_percent <= 70:
        return "Moderate Risk"
    return "High Risk"


def get_recommendations(risk_percent: float) -> list[str]:
    category = categorize_risk(risk_percent)
    if category == "Low Risk":
        return LOW_RISK
    if category == "Moderate Risk":
        return MODERATE_RISK
    return HIGH_RISK


def get_risk_badge_class(risk_percent: float) -> str:
    category = categorize_risk(risk_percent)
    return {
        "Low Risk": "success",
        "Moderate Risk": "warning",
        "High Risk": "danger",
    }[category]


def get_disclaimer() -> str:
    return MEDICAL_DISCLAIMER
