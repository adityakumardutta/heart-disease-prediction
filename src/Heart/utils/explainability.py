"""Explainable AI helpers: SHAP when available, model/permutation importance otherwise."""

import numpy as np

from src.Heart.constants import FEATURE_LABELS, FEATURE_NAMES

try:
    import shap

    _HAS_SHAP = True
except Exception:
    _HAS_SHAP = False


def _model_feature_importance(model, feature_names: list[str]) -> dict[str, float]:
    if hasattr(model, "feature_importances_"):
        values = model.feature_importances_
    elif hasattr(model, "coef_"):
        values = np.abs(np.ravel(model.coef_))
    else:
        return {}

    total = values.sum() or 1.0
    return {
        feature_names[i]: float(values[i] / total * 100)
        for i in range(len(feature_names))
    }


def get_feature_importance(model, X_sample, feature_names: list[str] | None = None) -> list[dict]:
    """Return top factors influencing prediction as sorted list of dicts."""
    feature_names = feature_names or FEATURE_NAMES
    importance_map: dict[str, float] = {}

    if _HAS_SHAP and X_sample is not None and len(X_sample) > 0:
        try:
            explainer = shap.Explainer(model.predict, X_sample[: min(50, len(X_sample))])
            shap_values = explainer(X_sample[:1])
            values = np.abs(np.array(shap_values.values).ravel())
            total = values.sum() or 1.0
            importance_map = {
                feature_names[i]: float(values[i] / total * 100)
                for i in range(len(feature_names))
            }
        except Exception:
            importance_map = {}

    if not importance_map:
        importance_map = _model_feature_importance(model, feature_names)

    if not importance_map:
        from src.Heart.utils.utils import load_json_artifact

        metadata = load_json_artifact("model_metadata.json", default={})
        saved = metadata.get("feature_importance", [])
        importance_map = {item["feature"]: item["importance"] for item in saved}

    ranked = sorted(importance_map.items(), key=lambda item: item[1], reverse=True)
    return [
        {
            "feature": name,
            "label": FEATURE_LABELS.get(name, name),
            "importance": round(score, 2),
        }
        for name, score in ranked[:8]
    ]
