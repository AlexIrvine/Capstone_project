from src.extract.extract import extract_data
from src.utils.logging_utils import setup_logger
from src.transform.transform import transform_data

logger = setup_logger(name="run_etl", log_file="run_etl.log")


def run_etl_pipline():
    logger.info("Starting ETL pipeline.")
    try:
        extracted_data = extract_data()
        logger.info("Extraction complete and data returned.")
    
    except Exception as e:
        logger.error(f"An error occurred during data extraction: {e}")
        raise
    
    try: 
        logger.info("Starting data transformation.")
        transformed_data = transform_data(extracted_data)
        logger.info("Data transformation complete and data returned.")
    except Exception as e:
        logger.error(f"An error occurred during data transformation: {e}")
        raise
    