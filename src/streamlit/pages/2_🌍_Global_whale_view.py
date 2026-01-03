import streamlit as st
import plotly.express as px
from src.streamlit.app import load_data
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(ROOT))

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
    <div class="olympic-title">🌍 Map of all GPS points</div>
    <p class="olympic-subtitle">
        Feel free to filter by species, study and individual.
    </p>
</div>
""", unsafe_allow_html=True)


st.markdown("**Fun fact: Whales are found in all major oceans on Earth!**")

# Colour selector side bar
colour = st.sidebar.color_picker("Color", value="#00FFAA")

# Load the data
whale_df = load_data()

filtered = whale_df.copy()

# Species filter
species_list = whale_df["individual_taxon_canonical_name"].unique().tolist()
selected_species = st.sidebar.multiselect(
    "Select Species",
    species_list
)

if selected_species:
    filtered = filtered[filtered["individual_taxon_canonical_name"].isin(selected_species)]

# Study filter
study_list = filtered["study_name"].unique().tolist()
selected_study = st.sidebar.multiselect(
    "Select Study",
    study_list
)

if selected_study:
    filtered = filtered[filtered["study_name"].isin(selected_study)]

# Individual filter
individual_list = filtered["individual_local_identifier"].unique().tolist()
selected_individuals = st.sidebar.multiselect(
    "Select Individual Whale",
    individual_list
)

if selected_individuals:
    filtered = filtered[filtered["individual_local_identifier"].isin(selected_individuals)]

# Make the scatter map
fig = px.scatter_map(
    filtered,
    lat="location_lat",
    lon="location_lon",
    hover_name="individual_local_identifier",
    hover_data=["individual_taxon_canonical_name", "study_name"],
    color_discrete_sequence=[colour],
    zoom=1,
    height=600
)

fig.update_layout(mapbox_style="carto-darkmatter")
st.plotly_chart(fig)
