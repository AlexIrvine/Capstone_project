from src.utils.logging_utils import setup_logger
logger = setup_logger(name="transform", log_file="transform.log")

def transform_data(data_dict):
    logger.info("Starting data transformation.")
    
    for df_name, df in data_dict.items():
        print(df.head())    