import logging
import os
from pathlib import Path
from src.utils.logging_utils import setup_logger

logger = setup_logger(__name__, "File_path_retrieval.log", level=logging.DEBUG)

# Set the root directory for raw data
root_directory = Path(__file__).resolve().parents[2]
data_directory = root_directory / "data" / "raw"


def create_file_list() -> list:
    """
    Extract the file path of all csvs found in the raw data folder.

    Returns:
        List of file paths

    Raises:
        Exception if no file found
    """
    try:
        # Create file list to store paths
        file_list = []
        logger.info(f"Creating file list from {data_directory}")
        # Error if file path not found
        if not data_directory.exists():
            logger.error(f"Data directory does not exist: {data_directory}")
            raise FileNotFoundError(
                f"Data directory does not exist: {data_directory}"
            )

        # For every file name found in the directory
        for file_name in os.listdir(data_directory):
            # If it is a csv file
            if file_name.endswith(".csv"):
                # Add it it path
                file_path = data_directory / file_name
                file_list.append(file_path)

        logger.info(
            f"File list creation complete. "
            f"Total files found: {len(file_list)}"
        )
        return file_list

    except Exception as e:
        logger.error(f"Error creating file list: {e}")
        raise
