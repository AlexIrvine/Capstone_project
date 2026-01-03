import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if not (ROOT / "src").exists():
    ROOT = Path(__file__).resolve().parents[1]

sys.path.insert(0, str(ROOT))

import streamlit as st
import pandas as pd
from src.streamlit.app import load_data

st.set_page_config(layout="wide")

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

# Title at the top of the page
st.markdown("""
<div class="highlight-box">
    <div class="olympic-title">🐋 Cetacean Olympics</div>
    <p class="olympic-subtitle">
        Daily distance and speed rankings for whales
        with at least five days of tracking.
    </p>
</div>
""", unsafe_allow_html=True)

# Load in the data set
whale_df = load_data()

# Force timestamp to have mixed format
whale_df["timestamp"] = pd.to_datetime(
    whale_df["timestamp"], format="mixed", errors="coerce"
)

whale_df["obs_date"] = whale_df["timestamp"].dt.date

# Group by individual whale
individual_stats = (
    whale_df.groupby("individual_local_identifier", as_index=False)
    .agg(
        total_distance_m=("distance_from_prev_m", "sum"),
        days_observed=("obs_date", "nunique"),
        avg_speed_mps=("speed_mps", "mean"),
        species=("individual_taxon_canonical_name", "first")
    )
)

# Only include individuals with at least 5 days of data
individual_stats = individual_stats[
    individual_stats["days_observed"] >= 5
].copy()

# Calculate daily km
individual_stats["daily_km"] = (
    individual_stats["total_distance_m"] / 1000
) / individual_stats["days_observed"]

# Aggregate to species level
species_stats = (
    individual_stats.groupby("species", as_index=False)
    .agg(
        mean_daily_km=("daily_km", "mean"),
        mean_speed=("avg_speed_mps", "mean"),
        No=("individual_local_identifier", "count")
    )
)

# Top and bottom selections
top8_dist = species_stats.sort_values(
    "mean_daily_km", ascending=False
).head(8)

bot8_dist = species_stats.sort_values(
    "mean_daily_km", ascending=True
).head(8)

top8_speed = species_stats.sort_values(
    "mean_speed", ascending=False
).head(8)

bot8_speed = species_stats.sort_values(
    "mean_speed", ascending=True
).head(8)

# Distance tables
st.subheader("Top & Bottom Species by Daily Distance (km/day)")
dist_col1, dist_col2 = st.columns(2)

with dist_col1:
    st.container(border=True).subheader("Top 8 by Daily Distance")
    show = top8_dist[["species", "mean_daily_km", "No"]].rename(
        columns={
            "species": "Species",
            "mean_daily_km": "Mean daily distance (km)",
            "No": "#"
        }
    )
    show["Mean daily distance (km)"] = show[
        "Mean daily distance (km)"
    ].round(2)
    st.dataframe(show, hide_index=True, use_container_width=True)

with dist_col2:
    st.container(border=True).subheader("Bottom 8 by Daily Distance")
    show = bot8_dist[["species", "mean_daily_km", "No"]].rename(
        columns={
            "species": "Species",
            "mean_daily_km": "Mean daily distance (km)",
            "No": "#"
        }
    )
    show["Mean daily distance (km)"] = show[
        "Mean daily distance (km)"
    ].round(2)
    st.dataframe(show, hide_index=True, use_container_width=True)

# Speed tables
st.subheader("Top & Bottom Species by Average Speed (m/s)")
spd_col1, spd_col2 = st.columns(2)

with spd_col1:
    st.container(border=True).subheader("Top 8 by Speed")
    show = top8_speed[["species", "mean_speed", "No"]].rename(
        columns={
            "species": "Species",
            "mean_speed": "Mean speed (m/s)",
            "No": "#"
        }
    )
    show["Mean speed (m/s)"] = show[
        "Mean speed (m/s)"
    ].round(2)
    st.dataframe(show, hide_index=True, use_container_width=True)

with spd_col2:
    st.container(border=True).subheader("Bottom 8 by Speed")
    show = bot8_speed[["species", "mean_speed", "No"]].rename(
        columns={
            "species": "Species",
            "mean_speed": "Mean speed (m/s)",
            "No": "#"
        }
    )
    show["Mean speed (m/s)"] = show[
        "Mean speed (m/s)"
    ].round(2)
    st.dataframe(show, hide_index=True, use_container_width=True)
