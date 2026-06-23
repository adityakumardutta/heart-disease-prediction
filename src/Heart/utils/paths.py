"""Centralized path helpers so artifacts resolve from any working directory."""

import os


def get_repo_root() -> str:
    return os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "..", "..")
    )


def artifact_path(*parts: str) -> str:
    return os.path.join(get_repo_root(), "Artifacts", *parts)


def static_chart_path(*parts: str) -> str:
    return os.path.join(get_repo_root(), "static", "charts", *parts)


def database_path() -> str:
    db_dir = os.path.join(get_repo_root(), "database")
    os.makedirs(db_dir, exist_ok=True)
    return os.path.join(db_dir, "predictions.db")
