"""Flask application for Heart Disease Prediction."""

import logging
import os
import sys

from flask import Flask, flash, redirect, render_template, request, send_file, url_for
from io import BytesIO

from src.Heart.constants import FEATURE_LABELS, MEDICAL_DISCLAIMER
from src.Heart.database.db import get_all_predictions, get_prediction, init_db, save_prediction
from src.Heart.pipeline.Prediction_pipeline import CustomData, PredictPipeline
from src.Heart.utils.paths import artifact_path
from src.Heart.utils.report_generator import generate_pdf_report
from src.Heart.utils.utils import load_json_artifact
from src.Heart.utils.validators import ValidationError, validate_patient_input

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s %(name)s - %(message)s",
    stream=sys.stdout,
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "heart-disease-portfolio-dev-key")

init_db()


def _verify_artifacts() -> None:
    required = ["Model.pkl", "Preprocessor.pkl", "model_metadata.json"]
    missing = [name for name in required if not os.path.exists(artifact_path(name))]
    if missing:
        logger.error("Missing deployment artifacts: %s", ", ".join(missing))
    else:
        logger.info("Deployment artifacts verified.")


_verify_artifacts()


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        try:
            logger.info("Prediction request received.")
            patient = validate_patient_input(request.form)
            data = CustomData(**patient)
            result = PredictPipeline().predict_with_details(
                data.get_data_as_dataframe(), patient=patient
            )
            record_id = save_prediction(result)
            result["record_id"] = record_id
            result["disclaimer"] = MEDICAL_DISCLAIMER
            logger.info("Prediction saved with record_id=%s", record_id)
            return render_template("result.html", result=result)

        except ValidationError as exc:
            for message in exc.errors.values():
                flash(message, "danger")
            return render_template("index.html", form_data=request.form, errors=exc.errors)

        except Exception as exc:
            logger.exception("Prediction failed")
            flash(f"Prediction failed: {exc}", "danger")
            return render_template("index.html", form_data=request.form, errors={})

    return render_template("index.html", form_data={}, errors={})


@app.route("/dashboard")
def dashboard():
    metrics = load_json_artifact("metrics.json", default={})
    comparison = load_json_artifact("model_comparison.json", default={})
    return render_template(
        "dashboard.html",
        metrics=metrics,
        comparison=comparison.get("models", {}),
        best_model=comparison.get("best_model", metrics.get("best_model", "N/A")),
    )


@app.route("/history")
def history():
    records = get_all_predictions()
    return render_template("history.html", records=records)


@app.route("/download-report/<int:record_id>")
def download_report(record_id: int):
    record = get_prediction(record_id)
    if record is None:
        flash("Report not found.", "warning")
        return redirect(url_for("history"))

    pdf_bytes = generate_pdf_report(record)
    return send_file(
        BytesIO(pdf_bytes),
        mimetype="application/pdf",
        as_attachment=True,
        download_name=f"heart_risk_report_{record_id}.pdf",
    )


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port, debug=os.environ.get("FLASK_DEBUG", "0") == "1")
