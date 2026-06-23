"""Visualization helpers for model dashboard charts."""

import json
import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

from src.Heart.utils.paths import static_chart_path


def _ensure_chart_dir() -> str:
    chart_dir = static_chart_path()
    os.makedirs(chart_dir, exist_ok=True)
    return chart_dir


def save_confusion_matrix_chart(matrix: list[list[int]], labels: list[str] | None = None) -> str:
    chart_dir = _ensure_chart_dir()
    labels = labels or ["No Disease", "Disease"]
    arr = np.array(matrix)
    plt.figure(figsize=(5, 4))
    sns.heatmap(arr, annot=True, fmt="d", cmap="Blues", xticklabels=labels, yticklabels=labels)
    plt.xlabel("Predicted")
    plt.ylabel("Actual")
    plt.title("Confusion Matrix")
    plt.tight_layout()
    out = os.path.join(chart_dir, "confusion_matrix.png")
    plt.savefig(out, dpi=120)
    plt.close()
    return "charts/confusion_matrix.png"


def save_model_comparison_chart(comparison: dict) -> str:
    chart_dir = _ensure_chart_dir()
    names = list(comparison.keys())
    scores = [comparison[name]["accuracy"] * 100 for name in names]
    plt.figure(figsize=(8, 4))
    bars = plt.bar(names, scores, color=sns.color_palette("viridis", len(names)))
    plt.xticks(rotation=25, ha="right")
    plt.ylim(0, 100)
    plt.ylabel("Accuracy (%)")
    plt.title("Model Comparison")
    for bar, score in zip(bars, scores):
        plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 1, f"{score:.1f}%", ha="center", fontsize=9)
    plt.tight_layout()
    out = os.path.join(chart_dir, "model_comparison.png")
    plt.savefig(out, dpi=120)
    plt.close()
    return "charts/model_comparison.png"


def save_roc_curve_chart(fpr: list, tpr: list, auc_score: float) -> str:
    chart_dir = _ensure_chart_dir()
    plt.figure(figsize=(5, 4))
    plt.plot(fpr, tpr, label=f"ROC (AUC = {auc_score:.3f})")
    plt.plot([0, 1], [0, 1], linestyle="--", color="gray")
    plt.xlabel("False Positive Rate")
    plt.ylabel("True Positive Rate")
    plt.title("ROC Curve")
    plt.legend(loc="lower right")
    plt.tight_layout()
    out = os.path.join(chart_dir, "roc_curve.png")
    plt.savefig(out, dpi=120)
    plt.close()
    return "charts/roc_curve.png"


def save_feature_importance_chart(importance: list[dict]) -> str:
    chart_dir = _ensure_chart_dir()
    labels = [item["label"] for item in importance[:8]][::-1]
    values = [item["importance"] for item in importance[:8]][::-1]
    plt.figure(figsize=(7, 4))
    plt.barh(labels, values, color=sns.color_palette("rocket", len(labels)))
    plt.xlabel("Importance (%)")
    plt.title("Top Feature Importance")
    plt.tight_layout()
    out = os.path.join(chart_dir, "feature_importance.png")
    plt.savefig(out, dpi=120)
    plt.close()
    return "charts/feature_importance.png"


def save_metrics_json(path: str, payload: dict) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)
