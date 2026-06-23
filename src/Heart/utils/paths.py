"""Centralized path helpers so artifacts resolve from any working directory."""

import logging
import os

logger = logging.getLogger(__name__)


def get_repo_root() -> str:
    env_root = os.environ.get("REPO_ROOT")
    if env_root:
        return os.path.abspath(env_root)

    start = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
    candidates = [start, os.getcwd()]
    for candidate in candidates:
        if os.path.isfile(os.path.join(candidate, "app.py")) and os.path.isdir(
            os.path.join(candidate, "Artifacts")
        ):
            return candidate

    logger.warning("Could not locate repo root from app.py; falling back to %s", start)
    return start


def artifact_path(*parts: str) -> str:
    path = os.path.join(get_repo_root(), "Artifacts", *parts)
    logger.debug("Resolved artifact path: %s", path)
    return path


def static_chart_path(*parts: str) -> str:
    return os.path.join(get_repo_root(), "static", "charts", *parts)


def database_path() -> str:
    db_dir = os.path.join(get_repo_root(), "database")
    os.makedirs(db_dir, exist_ok=True)
    return os.path.join(db_dir, "predictions.db")
