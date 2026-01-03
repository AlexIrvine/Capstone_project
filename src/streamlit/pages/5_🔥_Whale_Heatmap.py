import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if not (ROOT / "src").exists():
    ROOT = Path(__file__).resolve().parents[1]

sys.path.insert(0, str(ROOT))

import streamlit as st
import leafmap.foliumap as leafmap
from src.streamlit.app import load_data


# Make it look good
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
    <div class="olympic-title">🔥 Heatmap of whale activity</div>
    <p class="olympic-subtitle">
        View all or select a species.
    </p>
</div>
""", unsafe_allow_html=True)

st.set_page_config(layout="wide")

# Load the data
whale_df = load_data()

# Add heatmap value column
whale_df["value"] = 1

# Add a species filter
species_list = whale_df["individual_taxon_canonical_name"].unique().tolist()

selected_species = st.sidebar.multiselect(
    "Select Species",
    species_list
)

if selected_species:
    whale_df = whale_df[whale_df["individual_taxon_canonical_name"].isin(selected_species)]


# Center the map on the average
center = dict(
    lat=whale_df["location_lat"].mean(),
    lon=whale_df["location_lon"].mean()
)

# Separate the columns
col1, col2 = st.columns([4, 1])

# Get the available leafmaps
options = list(leafmap.basemaps.keys())
index = options.index("OpenTopoMap")

with col2:
    basemap = st.selectbox("Select a basemap:", options, index)

with col1:

    m = leafmap.Map(
        center=[whale_df["location_lat"].mean(),
                whale_df["location_lon"].mean()],
        zoom=2
    )

    m.add_basemap(basemap)
    # Add the info to the map
    m.add_heatmap(
        data=whale_df,
        latitude="location_lat",
        longitude="location_lon",
        value="value",
        name="Whale Heatmap",
        radius=10,
    )
    # Plot the map
    m.to_streamlit(height=600)
