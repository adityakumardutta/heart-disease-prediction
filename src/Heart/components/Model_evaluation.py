import os
import sys

import numpy as np
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
    roc_curve,
)

from src.Heart.utils.explainability import get_feature_importance
from src.Heart.utils.paths import artifact_path
from src.Heart.utils.utils import load_object, save_json_artifact
from src.Heart.utils.visualization import (
    save_confusion_matrix_chart,
    save_feature_importance_chart,
    save_roc_curve_chart,
)

try:
    import mlflow
    import mlflow.sklearn
    from urllib.parse import urlparse

    _HAS_MLFLOW = True
except Exception:
    _HAS_MLFLOW = False


class ModelEvaluation:
    def eval_metrics(self, actual, pred, proba=None):
        accuracy = accuracy_score(actual, pred)
        precision = precision_score(actual, pred, zero_division=0)
        recall = recall_score(actual, pred, zero_division=0)
        f1 = f1_score(actual, pred, zero_division=0)
        roc_auc = None
        if proba is not None and len(np.unique(actual)) > 1:
            roc_auc = roc_auc_score(actual, proba)
        return accuracy, precision, recall, f1, roc_auc

    def initate_model_evaluation(self, train_array, test_array, best_model_name=None):
        try:
            X_test, y_test = test_array[:, :-1], test_array[:, -1]
            model_path = artifact_path("Model.pkl")
            model = load_object(model_path)

            predicted = model.predict(X_test)
            proba = model.predict_proba(X_test)[:, 1] if hasattr(model, "predict_proba") else None
            accuracy, precision, recall, f1, roc_auc = self.eval_metrics(
                y_test, predicted, proba
            )

            cm = confusion_matrix(y_test, predicted).tolist()
            fpr, tpr, _ = roc_curve(y_test, proba) if proba is not None else ([], [])
            importance = get_feature_importance(model, X_test)

            metrics_payload = {
                "best_model": best_model_name or "Unknown",
                "accuracy": round(float(accuracy), 4),
                "precision": round(float(precision), 4),
                "recall": round(float(recall), 4),
                "f1": round(float(f1), 4),
                "roc_auc": round(float(roc_auc), 4) if roc_auc is not None else None,
                "confusion_matrix": cm,
                "charts": {
                    "confusion_matrix": save_confusion_matrix_chart(cm),
                    "roc_curve": save_roc_curve_chart(fpr.tolist(), tpr.tolist(), roc_auc or 0)
                    if proba is not None
                    else None,
                    "feature_importance": save_feature_importance_chart(importance),
                    "model_comparison": "charts/model_comparison.png",
                },
            }
            save_json_artifact("metrics.json", metrics_payload)

            print(
                f"Accuracy: {accuracy}, Precision: {precision}, Recall: {recall}, "
                f"F1: {f1}, ROC-AUC: {roc_auc}"
            )

            if _HAS_MLFLOW:
                try:
                    mlflow.set_registry_uri(
                        "https://dagshub.com/HemaKalyan45/Heart-Disease-Prediction.mlflow"
                    )
                    tracking_url_type_store = urlparse(mlflow.get_tracking_uri()).scheme
                    with mlflow.start_run():
                        mlflow.log_metric("Testing Accuracy", accuracy)
                        mlflow.log_metric("Precision Score", precision)
                        mlflow.log_metric("Recall Score", recall)
                        mlflow.log_metric("F1 Score", f1)
                        if roc_auc is not None:
                            mlflow.log_metric("ROC AUC", roc_auc)
                        if tracking_url_type_store != "file":
                            mlflow.sklearn.log_model(model, "Model", registered_model_name="ml_model")
                        else:
                            mlflow.sklearn.log_model(model, "Model")
                except Exception as e:
                    print("mlflow logging skipped -", e)

            return metrics_payload

        except Exception as e:
            raise e
