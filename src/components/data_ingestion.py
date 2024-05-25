import os
import sys

# Ensure the src directory is in the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
from src.logger import logging
from src.exception import CustomerException
from dataclasses import dataclass
from sklearn.model_selection import train_test_split
from src.components.data_transformation import DataTransformation
import pandas as pd


@dataclass
class DataIngestionConfig:
    train_data_path: str = os.path.join("artifacts", "train.csv")
    test_data_path: str = os.path.join("artifacts", "test.csv")
    raw_data_path: str = os.path.join("artifacts", "data.csv")


class DataIngestion:
    def __init__(self):
        self.ingestion_config = DataIngestionConfig()

    def inititate_data_ingestion(self):
        logging.info("Entered Data Ingestion method")

        try:
            logging.info("Data Ingestion initiated")

            df = pd.read_csv("notebook\data\stud.csv")

            os.makedirs(
                os.path.dirname(self.ingestion_config.raw_data_path), exist_ok=True
            )
            df.to_csv(self.ingestion_config.raw_data_path, index=False, header=True)

            logging.info("Train test split initiated")
            train_data, test_data = train_test_split(df, test_size=0.2, random_state=42)

            train_data.to_csv(
                self.ingestion_config.train_data_path, index=False, header=True
            )
            test_data.to_csv(
                self.ingestion_config.test_data_path, index=False, header=True
            )

            logging.info("Ingestion of the data Completed")
            return (
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path,
            )

        except Exception as e:
            raise CustomerException(e, sys)


if __name__ == "__main__":
    obj = DataIngestion()
    train_data, text_data = obj.inititate_data_ingestion()

    data_traformation = DataTransformation()
    train_arr, test_arr, path = data_traformation.inititate_data_transformation(
        train_data, text_data
    )
