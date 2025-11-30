from src.extract.create_file_list import create_file_list
from src.extract.extract_files_into_df import extract_files_to_df
from src.utils.logging_utils import setup_logger

logger = setup_logger("extract_data", "extract_data.log")


def extract_data() -> dict:
    try:
        logger.info("Starting data extraction process")

        # Create a list of files
        file_list = create_file_list()
        # Convert the files into a dictionary of file name and dataframe
        data_dict = extract_files_to_df(file_list)

        logger.info(
            f"Extraction completed successfully."
            f"Number of files {len(data_dict)}"
                    )
        return data_dict

    except Exception as e:
        logger.error(f"Error during extraction: {e}")
        raise
