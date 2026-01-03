import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if not (ROOT / "src").exists():
    ROOT = Path(__file__).resolve().parents[1]

sys.path.insert(0, str(ROOT))

import pandas as pd
import os
import streamlit as st
from scripts.run_etl import run_etl_pipeline
from src.utils.logging_utils import setup_logger


def main():
    logger = setup_logger("app_pipeline", "app_pipeline.log")
    filepath = None  # ← REQUIRED

    try:
        logger.info("Starting app pipeline")
        filepath = run_etl_pipeline()
        print(filepath)
    except Exception as e:
        logger.error(f"An error occurred in the app pipeline : {e}")

    if filepath is None:
        filepath = "data/processed/combined_cleaned_data.csv"

    return filepath


@st.cache_data(show_spinner="Loading whale data...")
def load_data():
    root_directory = Path(__file__).resolve().parents[2]
    data_directory = root_directory / "data" / "processed"

    for file_name in os.listdir(data_directory):
        if file_name.endswith(".csv"):
            file_path = data_directory / file_name

    return pd.read_csv(file_path)


# Style the page to look good
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

# Title + overview
st.markdown("""
<div class="highlight-box">
    <div class="olympic-title">🐋 Whale GPS Movement Analytics Platform</div>
    <p class="olympic-subtitle">
        An interactive exploration of global whale movement data built using an end-to-end ETL pipeline.
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
### About this project

This application processes open-source whale tracking data from the **Movebank** platform.
The data is cleaned, validated, and enriched through a custom ETL pipeline before being
visualised in a set of interactive maps.

The goal is to demonstrate **robust data engineering practices** while presenting complex
ecological movement data in an accessible and engaging way.
""")

st.markdown("""
### What each page shows

**🌍 Global Whale View**  
View all recorded GPS locations across all studies.  
Filter by species, study, or individual whale to explore movement patterns at different scales.

**🌍 Global Whale View (Reduced)**  
A lighter-weight version of the global map, displaying a random subset of points to improve
performance while still showing global distribution.

**🎞️ Animated Path**  
Select an individual whale and watch its movement over time.  
This page animates GPS tracks to show migration paths and movement behaviour.

**🔥 Whale Heatmap**  
Visualise areas of high whale activity using a spatial heatmap.  
Filter by species to identify hotspots and regions of frequent use.
""")

st.markdown("""
### How the data is generated

When this app starts, it automatically runs the ETL pipeline:
- Extracts raw CSV files
- Cleans and validates GPS and timestamp data
- Calculates distance, time deltas, and movement speed
- Removes implausible outliers
- Produces a single processed dataset used by all pages

This ensures the visualisations always reflect the latest cleaned data.
""")

st.markdown("""
---

Thank you for exploring the project.  
Feel free to navigate between pages using the sidebar, and ask any questions.
""")


if __name__ == "__main__":
    main()

