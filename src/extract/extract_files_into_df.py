import logging
import pandas as pd
from src.utils.logging_utils import setup_logger

logger = setup_logger(__name__, "File_conversion.log", level=logging.DEBUG)


def extract_files_to_df(file_paths) -> dict:
    """
    Load all CSVs listed by create_file_list() into DataFrames.
    Returns a dictionary {df_name: DataFrame}.
    """
    data_dict = {}
    counter = 1

    logger.info("Starting CSV extraction into DataFrames.")

    for path in file_paths:
        try:
            df = pd.read_csv(path)
            df_name = path.name.rsplit(".", 1)[0]
            
            data_dict[df_name] = df

            logger.info(
                f"Loaded {df_name} from {path.name} with {len(df)} rows."
                )
            counter += 1

        except Exception as e:
            logger.error(f"Failed to load {path.name}: {e}")
            raise

    logger.info(f"Extraction complete. Loaded {len(data_dict)} DataFrames.")
    return data_dict
