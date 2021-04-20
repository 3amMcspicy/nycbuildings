#!/usr/bin/env python

"""
Create folium maps
"""
import numpy as np
import pandas as pd
import folium
import branca.colormap as cm
import pydeck as pdk
import streamlit as st


def create_map(data, year1, year2):
    """
    Takes a Data class instance as input
    """
    # create map
    fmap = folium.Map(
        tiles="Stamen Toner",
        location=[40.75, -73.9],
        zoom_start=11,
    )

    # use colorscale normalized by all years values
    colormap = cm.LinearColormap(
        colors=["green", "red"],
    )

    # get the difference in consumption between two years
    diff = data.tds_by_year.loc[:, year1] - data.tds_by_year.loc[:, year2]

    # create markers colored by the difference in consumption
    for tds in diff.index:

        if not pd.isna(diff.loc[tds]):

            # get lat,long of this tds
            lat = data.coords[data.coords.tds == tds].latitude.values[0]
            lon = data.coords[data.coords.tds == tds].longitude.values[0]

            # add marker to this year
            marker = folium.Circle(
                location=[lat, lon],
                radius=150,
                color=colormap(diff.loc[tds]),
                fill=True,
                tooltip=folium.Tooltip(
                    text=f"tds={tds}, delta-consumption={diff.loc[tds]:.0f}",
                ),
            )
            fmap.add_child(marker)

    # show map
    return fmap


# Creating hexagonal map view built with pydeck
def create_hex_map(data):

    # Checks the dataset selection to differentiate between consumption_kwh and consumption_hcf
    if "consumption_kwh" in data.columns:
        data = data[["latitude", "longitude", "consumption_kwh"]]

    else:
        data = data[["latitude", "longitude", "consumption_hcf"]]

    # Calculation for midpoint of the GPS coordinates to zoom to
    midpoint = (np.average(data["latitude"]), np.average(data["longitude"]))

    # st.write(data)
    st.write(
        pdk.Deck(
            map_style="mapbox://styles/mapbox/dark-v10",
            initial_view_state={
                "latitude": midpoint[0],
                "longitude": midpoint[1],
                "zoom": 11,
                "pitch": 50,
            },
            layers=[
                pdk.Layer(
                    "HexagonLayer",
                    data=data,
                    get_position=["longitude", "latitude"],
                    radius=100,
                    elevation_scale=3,
                    elevation_range=[0, 3000],
                    pickable=True,
                    extruded=True,
                ),
            ],
        )
    )


# No tooltip included for hexmap because the difference in lowest and highest consumption is too large to display without scaling them
