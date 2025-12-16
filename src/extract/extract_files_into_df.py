import logging
import pandas as pd
from src.utils.logging_utils import setup_logger

# Set up the logger with module name and captures every message
logger = setup_logger(__name__, "File_conversion.log", level=logging.DEBUG)


def extract_files_to_df(file_paths) -> dict:
    """
    Load all CSVs listed by create_file_list() into DataFrames.
    Returns a dictionary {df_name: DataFrame}.
    """
    # Set up data dictionary to store file names and dataframes
    data_dict = {}
    logger.info("Starting CSV extraction into DataFrames.")

    # Loop through every path in file path folder and convert it to a dataframe
    for path in file_paths:
        # Set up try expect block
        try:
            # Convert to dataframe
            df = pd.read_csv(path)
            # Pull out the csv name
            df_name = path.name.split(".", 1)[0]
            # Save the df under the file name
            data_dict[df_name] = df
            # Display the name, path and length
            logger.info(
                f"Loaded {df_name} from {path.name} with {len(df)} rows."
            )
        # Raise an exception with an error.
        except Exception as e:
            logger.error(f"Failed to load {path.name}: {e}")
            raise
    # Log the number of files used.
    logger.info(f"Extraction complete. Loaded {len(data_dict)} DataFrames.")
    return data_dict
