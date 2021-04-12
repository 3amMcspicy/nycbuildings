#!/usr/bin/env python

"""
A streamlit app
"""
import streamlit as st
from streamlit_folium import folium_static
from data import Data
from mapping import create_map



def build_header():
    """
    Writes the header and shows data table
    """
    #Laying out top section of the APP
    row_1, row_2 = st.beta_columns((2, 3))

    with row_1:
        st.title("NYCHA electricity and water consumption data")

    with row_2:
        st.write(
        """
        ##
        Examing how water and electricity consumption has changed over 
        time in NYCHA developments. The slider can be used to change
        the selected time over which to view changes in consumption.
        """    
    )


def build_data_view(data):
    "show the dataframe header"
    with st.beta_expander('Expand'):
        st.dataframe(data.reset_index().head(25), height=200)


def build_maps(data, year1, year2):
    "builds a map showing X"
    fmap = create_map(data, year1, year2)
    folium_static(fmap)

borough_selection = st.sidebar.selectbox("Please choose a borough", ('MANHATTAN', 'BROOKLYN', 'QUEENS', 'BRONX', 'STATEN ISLAND'))
dataset_selection = st.sidebar.selectbox("Please choose a dataset", ('Water', 'Electricity'))






if __name__ == "__main__":

    # draw the webapp header
    build_header()    

    # display an example while full data loads
    # ...

    # for testing: subset data with kwargs
    # Including option for borough
    KWARGS = {
        "borough": borough_selection,
        
    }

    # load the data once
    with st.spinner(text='Loading data'):
        DATA = Data(dataset_selection, **KWARGS)
        st.success('App is ready')

    # draw the data matrix header
    build_data_view(DATA.tds_by_year)

    # build several maps
    build_maps(DATA, 2020, 2015)

    # build toggle to show different maps given options...
    # ...
    time = list(DATA.data.revenue_month.unique())
    time.reverse()
    time_selection = st.select_slider("Year-Month",time)
    DATA_1 = DATA.data[DATA.data["revenue_month"] == time_selection]
    #selected_time = {"revenue_month": time_selection}
    st.write(DATA_1)
    
    
    #with st.spinner(text='Loading data'):
    #    DATA_1 = Data(dataset_selection, selected_time)
    #    st.success('App is ready')
    
    #st.write(DATA_1.data.head(10))
    #st.write(DATA.data.head(10))
    #build_data_view(DATA_1)
    #build_maps(DATA,2020, time_selection)
    