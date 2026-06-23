import sys

import pandas as pd

from src.Heart.constants import FEATURE_NAMES
from src.Heart.exception import customexception
from src.Heart.logger import logging
from src.Heart.utils.explainability import get_feature_importance
from src.Heart.utils.paths import artifact_path
from src.Heart.utils.recommendations import (
    categorize_risk,
    get_recommendations,
    get_risk_badge_class,
)
from src.Heart.utils.utils import load_json_artifact, load_object


class PredictPipeline:
    def __init__(self):
        self.preprocessor = None
        self.model = None
        self.model_name = "Unknown"

    def _load_artifacts(self):
        if self.preprocessor is None:
            self.preprocessor = load_object(artifact_path("Preprocessor.pkl"))
        if self.model is None:
            self.model = load_object(artifact_path("Model.pkl"))
        metadata = load_json_artifact("model_metadata.json", default={})
        self.model_name = metadata.get("best_model", "Unknown")

    def predict(self, features):
        result = self.predict_with_details(features)
        return [result["prediction"]]

    def predict_with_details(self, features, patient: dict | None = None) -> dict:
        try:
            self._load_artifacts()
            scaled_data = self.preprocessor.transform(features)
            prediction = int(self.model.predict(scaled_data)[0])

            if hasattr(self.model, "predict_proba"):
                risk_percent = float(self.model.predict_proba(scaled_data)[0][1] * 100)
            else:
                risk_percent = float(prediction * 100)

            risk_category = categorize_risk(risk_percent)
            recommendations = get_recommendations(risk_percent)
            feature_importance = get_feature_importance(self.model, scaled_data)

            patient_data = patient or features.iloc[0].to_dict()

            return {
                "prediction": prediction,
                "risk_percent": round(risk_percent, 1),
                "risk_category": risk_category,
                "risk_badge": get_risk_badge_class(risk_percent),
                "recommendations": recommendations,
                "feature_importance": feature_importance,
                "model_name": self.model_name,
                "patient": {k: patient_data.get(k) for k in FEATURE_NAMES},
                "outcome_text": "Heart Disease Detected" if prediction == 1 else "No Heart Disease Detected",
            }
        except Exception as e:
            raise customexception(e, sys)


class CustomData:
    def __init__(
        self,
        age: int,
        sex: int,
        cp: int,
        trestbps: int,
        chol: int,
        fbs: int,
        restecg: int,
        thalach: int,
        exang: int,
        oldpeak: float,
        slope: int,
        ca: int,
        thal: int,
    ):
        self.age = age
        self.sex = sex
        self.cp = cp
        self.trestbps = trestbps
        self.chol = chol
        self.fbs = fbs
        self.restecg = restecg
        self.thalach = thalach
        self.exang = exang
        self.oldpeak = oldpeak
        self.slope = slope
        self.ca = ca
        self.thal = thal

    def get_data_as_dataframe(self):
        try:
            custom_data_input_dict = {
                "age": [self.age],
                "sex": [self.sex],
                "cp": [self.cp],
                "trestbps": [self.trestbps],
                "chol": [self.chol],
                "fbs": [self.fbs],
                "restecg": [self.restecg],
                "thalach": [self.thalach],
                "exang": [self.exang],
                "oldpeak": [self.oldpeak],
                "slope": [self.slope],
                "ca": [self.ca],
                "thal": [self.thal],
            }
            df = pd.DataFrame(custom_data_input_dict)
            logging.info("Dataframe Gathered")
            return df
        except Exception as e:
            logging.info("Exception Occured in prediction pipeline")
            raise customexception(e, sys)

    def to_dict(self) -> dict:
        return {
            "age": self.age,
            "sex": self.sex,
            "cp": self.cp,
            "trestbps": self.trestbps,
            "chol": self.chol,
            "fbs": self.fbs,
            "restecg": self.restecg,
            "thalach": self.thalach,
            "exang": self.exang,
            "oldpeak": self.oldpeak,
            "slope": self.slope,
            "ca": self.ca,
            "thal": self.thal,
        }
