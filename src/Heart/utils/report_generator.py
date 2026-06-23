"""PDF report generation for prediction results."""

import os
from io import BytesIO

from fpdf import FPDF

from src.Heart.constants import FEATURE_LABELS, MEDICAL_DISCLAIMER


class PredictionReport(FPDF):
    def header(self):
        self.set_font("Helvetica", "B", 16)
        self.cell(0, 10, "Heart Disease Risk Assessment Report", ln=True, align="C")
        self.ln(4)


def generate_pdf_report(record: dict) -> bytes:
    pdf = PredictionReport()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Helvetica", "", 11)

    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 8, "Patient Inputs", ln=True)
    pdf.set_font("Helvetica", "", 11)
    for key, value in record["patient"].items():
        label = FEATURE_LABELS.get(key, key.replace("_", " ").title())
        pdf.cell(0, 7, f"{label}: {value}", ln=True)

    pdf.ln(4)
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 8, "Prediction Summary", ln=True)
    pdf.set_font("Helvetica", "", 11)
    outcome = "Heart Disease Detected" if record["prediction"] == 1 else "No Heart Disease Detected"
    pdf.cell(0, 7, f"Outcome: {outcome}", ln=True)
    pdf.cell(0, 7, f"Risk Score: {record['risk_percent']:.1f}%", ln=True)
    pdf.cell(0, 7, f"Risk Category: {record['risk_category']}", ln=True)
    pdf.cell(0, 7, f"Model Used: {record.get('model_name', 'N/A')}", ln=True)

    pdf.ln(4)
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 8, "Top Risk Factors", ln=True)
    pdf.set_font("Helvetica", "", 11)
    for item in record.get("feature_importance", [])[:5]:
        pdf.cell(0, 7, f"- {item['label']}: {item['importance']:.1f}%", ln=True)

    pdf.ln(4)
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 8, "Recommendations", ln=True)
    pdf.set_font("Helvetica", "", 11)
    for tip in record.get("recommendations", []):
        pdf.multi_cell(0, 7, f"- {tip}")

    pdf.ln(6)
    pdf.set_font("Helvetica", "I", 9)
    pdf.multi_cell(0, 5, MEDICAL_DISCLAIMER)

    buffer = BytesIO()
    pdf.output(buffer)
    return buffer.getvalue()
