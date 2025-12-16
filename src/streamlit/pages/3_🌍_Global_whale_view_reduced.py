import streamlit as st
import leafmap.foliumap as leafmap
from random import randint
from src.streamlit.app import load_data

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
    <div class="olympic-title">🌍 Map of 3000 random GPS points</div>
    <p class="olympic-subtitle">
        Limited to 3000 points to save computation.
    </p>
</div>
""", unsafe_allow_html=True)


st.markdown("**Change the map to change view!**")

# Load the data
whale_df = load_data()

# Create a value column for the marker value
whale_df["value"] = 1

# Center on the longitude and latitude column
center = dict(
    lat=whale_df["location_lat"].mean(),
    lon=whale_df["location_lon"].mean()
)

# Create two layout columns
col1, col2 = st.columns([4, 1])

# Get available leafemap basemaps
options = list(leafmap.basemaps.keys())
index = options.index("OpenTopoMap")

with col2:
    basemap = st.selectbox("Select a basemap:", options, index)

with col1:

    m = leafmap.Map(center=[whale_df["location_lat"].mean(), whale_df["location_lon"].mean()], zoom=2)
    m.add_basemap(basemap)

    # Random 3000 as it is too intensive
    x = randint(1, len(whale_df) - 3000)
    subset_df = whale_df.iloc[x: x + 3000].copy()

    m.add_markers_from_xy(
        data=subset_df,
        x="location_lon",
        y="location_lat",
        popup=None
    )

    m.to_streamlit(height=700)
