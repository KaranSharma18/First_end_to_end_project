import dill
import os
import sys

from src.exception import CustomerException
from src.logger import logging


def save_object(obj, file_path):
    """
    Save an object to a file using dill.

    :param obj: The object to be saved.
    :param file_path: The file path where the object should be saved.
    """
    try:
        # Ensure the directory exists
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        # Open the file and save the object
        with open(file_path, "wb") as file:
            dill.dump(obj, file)

    except Exception as e:
        raise CustomerException(e, sys)
