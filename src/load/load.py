import logging
from pathlib import Path
from src.utils.logging_utils import setup_logger

# Get the root directory
logger = setup_logger(__name__, "Load_data.log", level=logging.DEBUG)

root_directory = Path(__file__).resolve().parents[2]
# Create output directory and file
output_dir = root_directory / "data" / "processed"
output_dir.mkdir(parents=True, exist_ok=True)


# Save the data to the output folder
def save_combined_csv(combined_data):
    output_path = output_dir / "combined_cleaned_data.csv"
    combined_data.to_csv(output_path, index=False)
    logger.info("Dataset loaded")
    return output_path
# Future work get the folder right
