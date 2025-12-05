from src.transform.clean_data import clean_data
from src.utils.logging_utils import setup_logger
from src.transform.create_new_df import create_combined_df


def transform_data(data_dict: dict):
    """
    Transforms the data in the provided dictionary of DataFrames.
    """
    logger = setup_logger("transform_data", "transform_data.log")

    try:
        logger.info("Starting data transformation process")
        # Clean transaction data
        logger.info("Cleaning data...")
        cleaned_data = clean_data(data_dict)
        logger.info("Data cleaned successfully.")
        # Combine data in one dataframe
        logger.info("Combining into one df...")
        combined_df = create_combined_df(cleaned_data)
        logger.info("Data combined successfully.")

        return combined_df
    except Exception as e:
        logger.error(f"Data transformation failed: {str(e)}")
        raise
