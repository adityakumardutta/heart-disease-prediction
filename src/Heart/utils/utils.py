import json
import os
import pickle
import sys

import joblib
import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score

from src.Heart.exception import customexception
from src.Heart.logger import logging
from src.Heart.utils.paths import artifact_path


def save_object(file_path, obj):
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        # Use joblib for sklearn objects for better compatibility
        if hasattr(obj, '__sklearn_clone__') or 'sklearn' in str(type(obj)):
            joblib.dump(obj, file_path)
        else:
            with open(file_path, "wb") as file_obj:
                pickle.dump(obj, file_obj)
    except Exception as e:
        raise customexception(e, sys)


def load_object(file_path):
    try:
        if not os.path.exists(file_path):
            logging.error("Artifact missing: %s (cwd=%s)", file_path, os.getcwd())
            raise FileNotFoundError(f"Artifact not found: {file_path}")
        logging.info("Loading artifact: %s", file_path)
        # Try joblib first for sklearn objects, fallback to pickle
        try:
            return joblib.load(file_path)
        except:
            with open(file_path, "rb") as file_obj:
                return pickle.load(file_obj)
    except Exception as e:
        logging.exception("Failed to load artifact at %s", file_path)
        raise customexception(e, sys)


def evaluate_model(X_train, y_train, X_test, y_test, models):
    """Backward-compatible accuracy-only evaluation."""
    try:
        report = {}
        for model_name, model in models.items():
            model.fit(X_train, y_train)
            y_test_pred = model.predict(X_test)
            report[model_name] = accuracy_score(y_test, y_test_pred)
        return report
    except Exception as e:
        logging.info("Exception occurred during model training")
        raise customexception(e, sys)


def evaluate_models_full(X_train, y_train, X_test, y_test, models):
    """Evaluate models with accuracy, precision, recall, F1, and ROC-AUC."""
    from sklearn.metrics import (
        accuracy_score,
        f1_score,
        precision_score,
        recall_score,
        roc_auc_score,
    )

    report = {}
    for model_name, model in models.items():
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        y_proba = None
        if hasattr(model, "predict_proba"):
            y_proba = model.predict_proba(X_test)[:, 1]

        metrics = {
            "accuracy": float(accuracy_score(y_test, y_pred)),
            "precision": float(precision_score(y_test, y_pred, zero_division=0)),
            "recall": float(recall_score(y_test, y_pred, zero_division=0)),
            "f1": float(f1_score(y_test, y_pred, zero_division=0)),
        }
        if y_proba is not None and len(np.unique(y_test)) > 1:
            metrics["roc_auc"] = float(roc_auc_score(y_test, y_proba))
        else:
            metrics["roc_auc"] = None

        report[model_name] = metrics
    return report


def save_json_artifact(filename: str, payload: dict) -> str:
    path = artifact_path(filename)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)
    return path


def load_json_artifact(filename: str, default=None):
    path = artifact_path(filename)
    if not os.path.exists(path):
        return default
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)
