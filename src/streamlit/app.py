from scripts.run_etl import run_etl_pipeline
from src.utils.logging_utils import setup_logger


def main():
    
    logger = setup_logger("app_pipeline", "app_pipeline.log")
    
    try:
        logger.info("Starting app pipeline")
        
        data = run_etl_pipeline()

    except Exception as e:
        logger.error(f"An error occurred in the app pipeline : {e}")
        print(f"An error occurred: {e}")       
    return data


# Test driven development to check if it can call the extract function
if __name__ == "__main__":
    main()