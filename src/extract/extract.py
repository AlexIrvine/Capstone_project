import pandas as pd
import os
import pathlib
from src.utils.logging_utils import setup_logger

# Set up logger 
logger = setup_logger(name="extract", log_file="extract.log")

# Project root
root_directory = pathlib.Path(__file__).resolve().parents[2]
data_directory = root_directory / "data" / "raw"


def create_file_list():
    file_list = []
    logger.info(f"Creating file list from {data_directory}.")

    if not data_directory.exists():
        logger.error(f"Data directory does not exist: {data_directory}")
        raise FileNotFoundError(f"Data directory does not exist: {data_directory}")
      
    for file_name in os.listdir(data_directory):
        if file_name.endswith('.csv'):
            file_path = data_directory / file_name
            file_list.append(file_path)

    logger.info(f"File list creation complete. Total files found: {len(file_list)}")
    return file_list


def extract_data() -> dict:
    """
    Load all CSVs listed by create_file_list() into DataFrames.
    Returns a dictionary {filename: DataFrame}.
    """

    file_paths = create_file_list()
    data_dict = {}
    counter = 1 
    
    logger.info("Starting CSV extraction into DataFrames.")
    for path in file_paths: 
        try: 
            df = pd.read_csv(path)
            df_name = f"df{counter}"
            
            df["source_file"] = path.name  # Add source file column
            data_dict[df_name] = df
            
            logger.info(f"Loaded {df_name} from {path.name} with {len(df)} rows.")
            
            counter += 1
        except Exception as e:
            logger.error(f"Failed to load {path.name}: {e}")
            raise
    logger.info(f"Extraction complete. Loaded {len(data_dict)} DataFrames.")
    return data_dict