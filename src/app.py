#!/usr/bin/env python

"""
A streamlit app
"""
import pandas as pd
import streamlit as st
from PIL import Image
from streamlit_folium import folium_static
from data import Data
from mapping import create_map
from mapping import create_hex_map

# Header for the streamlit app
def build_header():
    """
    Writes the header and shows data table
    """
    # Laying out top section of the APP
    row_1, row_2 = st.beta_columns((2, 3))

    with row_1:
        st.title("NYCHA Consumption Data")

    with row_2:
        st.write(
            """
        ##
        Examing how water and electricity consumption has changed over 
        time in NYCHA developments.
        """
        )
    st.write(
        "Please select the dataset and borough that you wish to visualize in the sidebar"
    )


# Dataframe header for the folium map view
def build_data_view(data):
    "show the dataframe header"
    with st.beta_expander("Expand"):
        st.dataframe(data.reset_index().head(25), height=200)


# Function to create a folium map
def build_maps(data, year1, year2):
    "builds a map showing X"
    fmap = create_map(data, year1, year2)
    folium_static(fmap)


# Function to create hexagonal map view
def hex_map(data):
    create_hex_map(data)


# Function that displays an example of what kind of maps the app can deploy
def display_example():

    # Loading the images from other directory
    hexagon_image = Image.open("../map/hexagon_layer.jpg")
    folium_image = Image.open("../map/folium_layer.jpg")

    # Displaying the images
    col1, col2 = st.beta_columns(2)
    with col1:
        st.image(
            hexagon_image,
            caption="An example of visualizing consumption over the months",
        )
    with col2:
        st.image(
            folium_image,
            caption="An example of visualizing mean consumption over the years",
        )


if __name__ == "__main__":

    # draw the webapp header
    build_header()

    # Display an example while full data loads below the header
    display_example()

    # Dataset and borough selection
    borough_selection = st.sidebar.selectbox(
        "Please choose a borough",
        (
            "MANHATTAN",
            "BROOKLYN",
            "QUEENS",
            "BRONX",
            "STATEN ISLAND",
        ),
    )
    dataset_selection = st.sidebar.selectbox(
        "Please choose a dataset", ("Water", "Electricity")
    )

    # for testing: subset data with kwargs
    # Including option for borough
    KWARGS = {
        "borough": borough_selection,
    }

    # load the data once
    with st.spinner(text="Loading data"):
        DATA = Data(dataset_selection, **KWARGS)
        st.success("App is ready")

    # Toggles to choose between the 2 map views
    toggled_map = st.radio(
        "Please select a map view",
        ("Mean consumption change between years", "Visual consumption over month"),
    )

    # First folium map view that displays the change in mean consumption between years
    if toggled_map == "Mean consumption change between years":

        # draw the data matrix header
        build_data_view(DATA.tds_by_year)

        # Date input by user to compare between years
        second_date = st.number_input(
            "Please enter the earlier year to compare",
            min_value=2013,
            max_value=2020,
            value=2015,
        )
        first_date = st.number_input(
            "Please enter the later year to compare",
            min_value=2014,
            max_value=2021,
            value=2020,
        )

        # A Go button so that the computational heavy calculations come after the date inputs are confirmed
        if st.button("Go"):

            build_maps(DATA, first_date, second_date)
            st.write(
                """
                The map above shows the change in consumption* between the years selected. 
                Red circles indicate a decrease, whilst green circles indicate an increase.

                *consumption is the average consumption for that place in a year
                """
            )

    # The hexagonal map view
    elif toggled_map == "Visual consumption over month":
        # To build the time slider by returning the unique Year-Month values and sorting it in order
        time = list(DATA.data.revenue_month.unique())
        time.sort()

        # Streamlit timeslider function
        time_selection = st.select_slider("Year-Month", time)

        # Selecting a subset of the data based on the Year-Month selection and displays the hexagonal map view
        DATA_1 = DATA.data[DATA.data["revenue_month"] == time_selection]
        hex_map(DATA_1)
