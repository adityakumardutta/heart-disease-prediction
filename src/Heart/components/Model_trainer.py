import os
import sys

import numpy as np
from dataclasses import dataclass
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC

from src.Heart.exception import customexception
from src.Heart.logger import logging
from src.Heart.utils.explainability import get_feature_importance
from src.Heart.utils.paths import artifact_path
from src.Heart.utils.utils import evaluate_models_full, save_json_artifact, save_object
from src.Heart.utils.visualization import save_model_comparison_chart

try:
    from xgboost import XGBClassifier

    _HAS_XGBOOST = True
except Exception:
    _HAS_XGBOOST = False


@dataclass
class ModelTrainerConfig:
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
    trained_model_file_path = os.path.join(repo_root, "Artifacts", "Model.pkl")


class ModelTrainer:
    def __init__(self):
        self.model_trainer_config = ModelTrainerConfig()

    def _get_comparison_models(self):
        models = {
            "Logistic Regression": LogisticRegression(max_iter=1000, random_state=42),
            "Random Forest": RandomForestClassifier(
                n_estimators=100, random_state=42, max_depth=8
            ),
            "Support Vector Machine": SVC(kernel="rbf", C=2, probability=True, random_state=42),
        }
        if _HAS_XGBOOST:
            models["XGBoost"] = XGBClassifier(
                learning_rate=0.05,
                n_estimators=100,
                max_depth=6,
                random_state=42,
                eval_metric="logloss",
            )
        return models

    def initate_model_training(self, train_array, test_array):
        try:
            logging.info("Splitting Dependent and Independent variables from train and test data")
            X_train, y_train, X_test, y_test = (
                train_array[:, :-1],
                train_array[:, -1],
                test_array[:, :-1],
                test_array[:, -1],
            )

            models = self._get_comparison_models()
            model_report = evaluate_models_full(X_train, y_train, X_test, y_test, models)
            print(model_report)
            logging.info(f"Model Report: {model_report}")

            best_model_name = max(
                model_report,
                key=lambda name: (
                    model_report[name]["roc_auc"] or 0,
                    model_report[name]["f1"],
                    model_report[name]["accuracy"],
                ),
            )
            best_model = models[best_model_name]
            best_model.fit(X_train, y_train)

            print(
                f"Best Model Found: {best_model_name} | "
                f"Accuracy: {model_report[best_model_name]['accuracy']:.3f}"
            )
            logging.info(f"Best Model Found: {best_model_name}")

            save_object(self.model_trainer_config.trained_model_file_path, best_model)

            importance = get_feature_importance(best_model, X_test)
            save_json_artifact(
                "model_comparison.json",
                {
                    "models": model_report,
                    "best_model": best_model_name,
                },
            )
            save_json_artifact(
                "model_metadata.json",
                {
                    "best_model": best_model_name,
                    "feature_importance": importance,
                },
            )
            save_model_comparison_chart(model_report)

            return best_model_name, model_report, X_test, y_test, best_model

        except Exception as e:
            logging.info("Exception occured at Model Training")
            raise customexception(e, sys)
