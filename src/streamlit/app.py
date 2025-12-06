import pandas as pd
import os
import streamlit as st
from pathlib import Path
from scripts.run_etl import run_etl_pipeline
from src.utils.logging_utils import setup_logger


def main():
    # Sets up the logger and the file
    logger = setup_logger("app_pipeline", "app_pipeline.log")
    # Set up a try except for the app pipeline
    try:
        # Message at the start of app pipeline
        logger.info("Starting app pipeline")
        # Call the ETL pipeline
        filepath = run_etl_pipeline()
        print(filepath)
        # Exception block if the pipeline fails
    except Exception as e:
        logger.error(f"An error occurred in the app pipeline : {e}")
        # Return the data
    return filepath


def load_data():
    root_directory = Path(__file__).resolve().parents[2]
    data_directory = root_directory / "data" / "processed"
    for file_name in os.listdir(data_directory):
        # If it is a csv file
        if file_name.endswith(".csv"):
            # Add it it path
            file_path = data_directory / file_name

    return pd.read_csv(file_path)


# Style the page to look good
st.markdown("""
<style>
.highlight-box {
    background-color: #F0F2F6;
    padding: 20px;
    border-radius: 10px;
    border-left: 5px solid #4ECDC4;
    margin-bottom: 20px;
}
.olympic-title {
    font-size: 32px;
    color: #000000;
    font-weight: 700;
    margin-bottom: 0.25rem;
}
.olympic-subtitle {
    font-size: 16px;
    color: #000000;
    margin-top: 0;
}
</style>
""", unsafe_allow_html=True)
# Title
st.markdown("""
<div class="highlight-box">
    <div class="olympic-title">Thank you for listening! </div>
    <p class="olympic-subtitle">
        Hope you had a whale of a time (I'm so sorry)
        Any questions?
    </p>
</div>
""", unsafe_allow_html=True)

if __name__ == "__main__":
    main()

