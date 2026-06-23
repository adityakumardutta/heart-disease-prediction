"""PDF report generation for prediction results."""

from io import BytesIO

from fpdf import FPDF

from src.Heart.constants import FEATURE_LABELS, MEDICAL_DISCLAIMER


class PredictionReport(FPDF):
    def header(self):
        self.set_font("Helvetica", "B", 16)
        self.cell(0, 10, "Heart Disease Risk Assessment Report", new_x="LMARGIN", new_y="NEXT", align="C")
        self.ln(4)


def generate_pdf_report(record: dict) -> bytes:
    pdf = PredictionReport()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Helvetica", "", 11)

    width = pdf.w - pdf.l_margin - pdf.r_margin

    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(width, 8, "Patient Inputs", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 11)
    for key, value in record["patient"].items():
        label = FEATURE_LABELS.get(key, key.replace("_", " ").title())
        pdf.cell(width, 7, f"{label}: {value}", new_x="LMARGIN", new_y="NEXT")

    pdf.ln(4)
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(width, 8, "Prediction Summary", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 11)
    outcome = "Heart Disease Detected" if record["prediction"] == 1 else "No Heart Disease Detected"
    pdf.cell(width, 7, f"Outcome: {outcome}", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(width, 7, f"Risk Score: {record['risk_percent']:.1f}%", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(width, 7, f"Risk Category: {record['risk_category']}", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(width, 7, f"Model Used: {record.get('model_name', 'N/A')}", new_x="LMARGIN", new_y="NEXT")

    pdf.ln(4)
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(width, 8, "Top Risk Factors", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 11)
    for item in record.get("feature_importance", [])[:5]:
        pdf.cell(width, 7, f"- {item['label']}: {item['importance']:.1f}%", new_x="LMARGIN", new_y="NEXT")

    pdf.ln(4)
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(width, 8, "Recommendations", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 11)
    for tip in record.get("recommendations", []):
        pdf.set_x(pdf.l_margin)
        pdf.multi_cell(width, 7, f"- {tip}")

    pdf.ln(6)
    pdf.set_font("Helvetica", "I", 9)
    pdf.set_x(pdf.l_margin)
    pdf.multi_cell(width, 5, MEDICAL_DISCLAIMER)

    buffer = BytesIO()
    pdf.output(buffer)
    return buffer.getvalue()
