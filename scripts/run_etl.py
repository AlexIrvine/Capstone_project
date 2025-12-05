from src.utils.logging_utils import setup_logger
from src.extract.extract import extract_data
from src.transform.transform import transform_data
from src.load.load import save_combined_csv


# Function to call the ETL pipeline
def run_etl_pipeline():
    # Set up the logger for the ETL pipeline
    logger = setup_logger("etl_pipeline", "etl_pipeline.log")
    # Set up try expect block
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

        # Load phase
        logger.info("Beginning data load phase")
        output_file = save_combined_csv(transformed_data)

        return output_file

    except Exception as e:
        logger.error(f"ETL pipeline failed: {e}")
        raise
