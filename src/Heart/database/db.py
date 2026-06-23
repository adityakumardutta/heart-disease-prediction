"""SQLite persistence for prediction history."""

import json
import sqlite3
from datetime import datetime

from src.Heart.utils.paths import database_path


def _connect():
    conn = sqlite3.connect(database_path())
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    with _connect() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS predictions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                created_at TEXT NOT NULL,
                age INTEGER,
                sex INTEGER,
                cp INTEGER,
                trestbps INTEGER,
                chol INTEGER,
                fbs INTEGER,
                restecg INTEGER,
                thalach INTEGER,
                exang INTEGER,
                oldpeak REAL,
                slope INTEGER,
                ca INTEGER,
                thal INTEGER,
                prediction INTEGER,
                risk_percent REAL,
                risk_category TEXT,
                model_name TEXT,
                patient_json TEXT,
                recommendations_json TEXT,
                feature_importance_json TEXT
            )
            """
        )


def save_prediction(record: dict) -> int:
    init_db()
    with _connect() as conn:
        cursor = conn.execute(
            """
            INSERT INTO predictions (
                created_at, age, sex, cp, trestbps, chol, fbs, restecg,
                thalach, exang, oldpeak, slope, ca, thal,
                prediction, risk_percent, risk_category, model_name,
                patient_json, recommendations_json, feature_importance_json
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC"),
                record["patient"]["age"],
                record["patient"]["sex"],
                record["patient"]["cp"],
                record["patient"]["trestbps"],
                record["patient"]["chol"],
                record["patient"]["fbs"],
                record["patient"]["restecg"],
                record["patient"]["thalach"],
                record["patient"]["exang"],
                record["patient"]["oldpeak"],
                record["patient"]["slope"],
                record["patient"]["ca"],
                record["patient"]["thal"],
                record["prediction"],
                record["risk_percent"],
                record["risk_category"],
                record.get("model_name", "Unknown"),
                json.dumps(record["patient"]),
                json.dumps(record["recommendations"]),
                json.dumps(record["feature_importance"]),
            ),
        )
        return int(cursor.lastrowid)


def get_prediction(record_id: int) -> dict | None:
    init_db()
    with _connect() as conn:
        row = conn.execute(
            "SELECT * FROM predictions WHERE id = ?", (record_id,)
        ).fetchone()
    if row is None:
        return None
    return _row_to_dict(row)


def get_all_predictions(limit: int = 50) -> list[dict]:
    init_db()
    with _connect() as conn:
        rows = conn.execute(
            "SELECT * FROM predictions ORDER BY id DESC LIMIT ?", (limit,)
        ).fetchall()
    return [_row_to_dict(row) for row in rows]


def _row_to_dict(row: sqlite3.Row) -> dict:
    return {
        "id": row["id"],
        "created_at": row["created_at"],
        "patient": json.loads(row["patient_json"]),
        "prediction": row["prediction"],
        "risk_percent": row["risk_percent"],
        "risk_category": row["risk_category"],
        "model_name": row["model_name"],
        "recommendations": json.loads(row["recommendations_json"]),
        "feature_importance": json.loads(row["feature_importance_json"]),
    }
