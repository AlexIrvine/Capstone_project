import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from src.streamlit.app import load_data

st.set_page_config(layout="wide")

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
    <div class="olympic-title">🎞️ Animated map of whale movement</div>
    <p class="olympic-subtitle">
        Pick a species, then a whale, press play and watch its path.
    </p>
</div>
""", unsafe_allow_html=True)

whale_df = load_data()

# Select the species
species_list = (
    whale_df["individual_taxon_canonical_name"]
    .dropna()
    .unique()
    .tolist()
)

default_species = "Humpback whale"
default_species_index = (
    species_list.index(default_species)
    if default_species in species_list
    else 0
)

selected_species = st.selectbox(
    "Species",
    species_list,
    index=default_species_index
)

whale_df = whale_df[
    whale_df["individual_taxon_canonical_name"] == selected_species
]

# Select the whale (study_tag_id)
whale_ids = (
    whale_df["study_tag_id"]
    .dropna()
    .unique()
    .tolist()
)

default_whale = "Humpback whale and climate change_245950"
default_whale_index = (
    whale_ids.index(default_whale)
    if default_whale in whale_ids
    else 0
)

selected_whale = st.selectbox(
    "study_tag_id",
    whale_ids,
    index=default_whale_index
)

whale_df = whale_df[
    whale_df["study_tag_id"] == selected_whale
]

# Stops it breaking at the start by adding a message
if whale_df.empty:
    st.info("Please select a species and study_tag_id to show the animation.")
    st.stop()

# Center on the first location point
center_lat = whale_df.iloc[0]["location_lat"]
center_lon = whale_df.iloc[0]["location_lon"]

# Make the plot
fig = px.scatter_map(
    whale_df,
    lat="location_lat",
    lon="location_lon",
    hover_name="individual_local_identifier",
    hover_data=["individual_taxon_canonical_name", "study_name"],
    center=dict(lat=center_lat, lon=center_lon),
    zoom=2,
    # Animating section
    animation_frame="timestamp",
    animation_group="study_tag_id",
    height=700,
    color_discrete_sequence=["red"]
)

# Make the whale dot bigger
for trace in fig.data:
    if trace.mode == "markers":
        trace.marker.size = 10

# Add the trace to show the path
fig.add_trace(
    go.Scattermap(
        lat=whale_df["location_lat"],
        lon=whale_df["location_lon"],
        mode="lines",
        line=dict(color="green", width=2),
        name="Trail"
    )
)

# Speed up the movement
fig.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 40
fig.layout.updatemenus[0].buttons[0].args[1]["transition"]["duration"] = 5

# Start the plot
st.plotly_chart(fig, width="stretch")
