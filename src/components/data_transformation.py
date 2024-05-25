import os
import sys

import numpy as np
import pandas as pd
from src.logger import logging
from src.exception import CustomException
from src.utils import save_object
from dataclasses import dataclass

from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer


@dataclass
class DataTransformationConfig:
    preprocessor_obj_file_path = os.path.join("artifacts", "preprocessor.pkl")


class DataTransformation:
    def __init__(self):
        self.data_transformation_config = DataTransformationConfig()

    def get_data_trasformer_obj(self):
        logging.info("Entered get_data_tranformer_obj method")
        try:
            numerical_columns = ["writing_score", "reading_score"]
            categorical_columns = [
                "gender",
                "race_ethnicity",
                "parental_level_of_education",
                "lunch",
                "test_preparation_course",
            ]

            numerical_pipeline = Pipeline(
                steps=[
                    ("imputer", SimpleImputer(strategy="median")),
                    ("scaler", StandardScaler()),
                ]
            )

            categorical_pipeline = Pipeline(
                steps=[
                    ("imputer", SimpleImputer(strategy="most_frequent")),
                    ("one_hot_encoder", OneHotEncoder()),
                    ("scaler", StandardScaler(with_mean=False)),
                ]
            )

            logging.info(f"Numerical features: {numerical_columns}")
            logging.info(f"Categorical features: {categorical_columns}")

            preprocessor = ColumnTransformer(
                [
                    ("num_pipeline", numerical_pipeline, numerical_columns),
                    ("cat_pipeline", categorical_pipeline, categorical_columns),
                ]
            )

            logging.info("get_data_trasformer_obj method completed")

            return preprocessor

        except Exception as e:
            raise CustomException(e, sys)

    def inititate_data_transformation(self, train_path, test_path):
        logging.info("Entered inititate_data_transformation method")

        try:
            logging.info("Data Transformation initiated")

            train_data = pd.read_csv(train_path)
            test_data = pd.read_csv(test_path)

            target_col_name = "math_score"

            input_feature_train_df = train_data.drop(target_col_name, axis=1)
            input_feature_test_df = test_data.drop(target_col_name, axis=1)

            target_feature_train_df = train_data[target_col_name]
            target_feature_test_df = test_data[target_col_name]

            logging.info("Applying preprocessing object on train df and test df")

            preprocessing_obj = self.get_data_trasformer_obj()
            input_feature_train_arr = preprocessing_obj.fit_transform(
                input_feature_train_df
            )
            input_feature_test_arr = preprocessing_obj.transform(input_feature_test_df)

            train_arr = np.c_[
                input_feature_train_arr, np.array(target_feature_train_df)
            ]
            test_arr = np.c_[input_feature_test_arr, np.array(target_feature_test_df)]

            logging.info("Saving preprocessing object")
            save_object(
                obj=preprocessing_obj,
                file_path=self.data_transformation_config.preprocessor_obj_file_path,
            )

            logging.info("Data Transformation of the data Completed")

            return (
                train_arr,
                test_arr,
                self.data_transformation_config.preprocessor_obj_file_path,
            )

        except Exception as e:
            raise CustomException(e, sys)
