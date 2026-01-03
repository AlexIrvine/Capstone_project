import streamlit as st
import folium
from folium.plugins import HeatMap
import plotly_express as px
from streamlit_folium import st_folium
from src.streamlit.app import load_data
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(ROOT))


whale_df = load_data()

st.subheader("Whale Density Heatmap (Plotly)")

fig = px.density_mapbox(
    whale_df,
    lat="location_lat",
    lon="location_lon",
    radius=1,
    center=dict(
        lat=whale_df["location_lat"].mean(),
        lon=whale_df["location_lon"].mean()
    ),
    zoom=1,
    hover_name="individual_local_identifier",
    hover_data=["individual_taxon_canonical_name", "study_name"],
    mapbox_style="open-street-map",
    color_continuous_scale="Viridis"
)

st.plotly_chart(fig)

st.subheader("Whale Density Heatmap (Folium)")

m = folium.Map(
    location=[
        whale_df["location_lat"].mean(),
        whale_df["location_lon"].mean()
    ],
    zoom_start=3,
    control_scale=True
)

# Loop through each species
for species, df_group in whale_df.groupby("individual_taxon_canonical_name"):

    vals = df_group[["location_lat", "location_lon"]].copy()
    vals["weight"] = 1
    data = vals.values.tolist()

    fg = folium.FeatureGroup(name=species)

    HeatMap(
        data,
        min_opacity=0.05,
        max_opacity=0.9,
        radius=15
    ).add_to(fg)

    fg.add_to(m)

folium.LayerControl().add_to(m)

st_folium(m, width=1200)
