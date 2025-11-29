from src.utils.logging_utils import setup_logger
from src.extract.extract import extract_data
from src.transform.transform import transform_data


def run_etl_pipeline():
    
    logger = setup_logger("etl_pipeline", "etl_pipeline.log")

    try:
        logger.info("Starting ETL pipeline.")
        
        # Extract phase
        logger.info("Beginning data extraction phase")
        extracted_data = extract_data()
        logger.info("Data extraction phase completed")

        # Transformation phase
        logger.info("Beginning data transformation phase")
        transformed_data = transform_data(extracted_data)
        logger.info("Transformation complete.")
        return transformed_data
   
    except Exception as e:
        logger.error(f"ETL pipeline failed: {e}")
        raise
