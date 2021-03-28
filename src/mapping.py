#!/usr/bin/env python

"""
Create folium maps
"""

import pandas as pd
import folium
import branca.colormap as cm


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
        colors=['blue', 'red'], 
        vmin=-50000,
        vmax=50000,
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
                    text=f"tds={tds}, delta-consumption={diff.loc[tds]:.0f} KWH",
                )
            )
            fmap.add_child(marker)

    # show map
    return fmap
