
from src.transform.clean_data import clean_data
from src.utils.logging_utils import setup_logger

logger = setup_logger("transform_data", "transform_data.log")

    
def transform_data(data_dict: dict):
    """
    Transforms the data in the provided dictionary of DataFrames.
    """
    try:
        logger.info("Starting data transformation process")
        # Clean transaction data
        logger.info("Cleaning data...")
        cleaned_data = clean_data(data_dict)
        logger.info("Data cleaned successfully.")
        # Get the first DataFrame
    
        return cleaned_data
    except Exception as e:
        logger.error(f"Data transformation failed: {str(e)}")
        raise