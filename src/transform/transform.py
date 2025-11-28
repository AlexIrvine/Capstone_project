import pandas as pd
from src.utils.logging_utils import setup_logger

logger = setup_logger(name="transform", log_file="transform.log")

first_df = None
def transform_data(data_dict: dict):
    """
    Transforms the data in the provided dictionary of DataFrames.
    """

    if data_dict is None:
        logger.error("No data provided for transformation.")
        return None

    # Get the first DataFrame
    first_df = next(iter(data_dict.values()))

    print(first_df.head())
    print(first_df.shape)

    return data_dict
