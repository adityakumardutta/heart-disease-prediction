import os
import sys
import numpy as np
import pandas as pd
from src.Heart.logger import logging
from src.Heart.exception import customexception
from sklearn.model_selection import train_test_split
from dataclasses import dataclass
from pathlib import Path

class DataIngestionConfig:
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
    raw_data_path:str = os.path.join(repo_root, "Artifacts","raw_data.csv")
    train_data_path:str = os.path.join(repo_root, "Artifacts","train_data.csv")
    test_data_path:str = os.path.join(repo_root, "Artifacts","test_data.csv")

class DataIngestion:
    def __init__(self):
        self.ingestion_config = DataIngestionConfig()

    @staticmethod
    def _normalize_feature_encoding(data: pd.DataFrame) -> pd.DataFrame:
        """Align UCI-style 1-based encodings with the web form (0-based)."""
        normalized = data.copy()
        if normalized["cp"].min() >= 1:
            normalized["cp"] = normalized["cp"] - 1
        if normalized["slope"].min() >= 1:
            normalized["slope"] = normalized["slope"] - 1
        return normalized

    def initiate_data_ingestion(self):
        logging.info("Data ingestion started")
        try:
            repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
            data_path = os.path.join(repo_root, "Notebook_Experiments", "Data", "heart.csv")
            fallback_path = self.ingestion_config.raw_data_path

            if os.path.exists(data_path):
                data = pd.read_csv(data_path)
                logging.info("Loaded dataset from %s", data_path)
            elif os.path.exists(fallback_path):
                data = pd.read_csv(fallback_path)
                logging.info("heart.csv missing; loaded fallback dataset from %s", fallback_path)
            else:
                raise FileNotFoundError(
                    f"Training data not found. Expected {data_path} or {fallback_path}. "
                    "Commit heart.csv or run training locally before deploy."
                )

            data = self._normalize_feature_encoding(data)

            os.makedirs(os.path.dirname(self.ingestion_config.raw_data_path), exist_ok=True)
            data.to_csv(self.ingestion_config.raw_data_path, index=False)
            logging.info("Created the raw data file")

            logging.info("Splitting the data into train and test")
            train_data, test_data = train_test_split(data, test_size=0.2, random_state=42)
            logging.info("Data Splitting is done")

            train_data.to_csv(self.ingestion_config.train_data_path, index=False)
            test_data.to_csv(self.ingestion_config.test_data_path, index=False)
            logging.info("Created the train and test data files")
            logging.info("Data ingestion completed")

            return (
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path
            )
        except Exception as e:
            logging.info("Excpetion occured while ingesting the data")
            raise customexception(e,sys)