import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
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
    <div class="olympic-title">🎞️ Animated map of whale movement</div>
    <p class="olympic-subtitle">
        Pick a whale, press play and watch its path.
    </p>
</div>
""", unsafe_allow_html=True)

st.set_page_config(layout="wide")

whale_df = load_data()

# Select the species
species_list = whale_df["study_tag_id"].unique().tolist()
selected_whale = st.multiselect("study_tag_id", species_list)

whale_df = whale_df[whale_df["study_tag_id"].isin(selected_whale)]

# Stops it breaking at the start by adding a message, could add whale
if whale_df.empty:
    st.info("Please select at least one study_tag_id to show the animation.")
    st.stop()

# Center on the fist location point
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
    height=600,
    color_discrete_sequence=["red"]
)

# Create a trace to show the path
for trace in fig.data:
    if "marker" in trace:
        trace.marker.size = 10
# Add the trace to the map
fig.add_trace(
    go.Scattermap(
        lat=whale_df["location_lat"],
        lon=whale_df["location_lon"],
        mode="lines",
        line=dict(color="green", width=3),
        name="Trail"
    )
)

# Speed up the movement
fig.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 40
fig.layout.updatemenus[0].buttons[0].args[1]["transition"]["duration"] = 5

# Start the plot
st.plotly_chart(fig)
