#!/usr/bin/env python

"""
A streamlit app
"""
import streamlit as st
from streamlit_folium import folium_static
from data import Data
from mapping import create_map
from mapping import create_hex_map


#borough selection
def toggle_borough():
    """
    container = st.beta_container()
    all = st.checkbox("Select all")

    if all:
        selected_options = container.multiselect("Select one or more boroughs:",
            ['MANHATTAN', 'BROOKLYN', 'QUEENS', 'BRONX', 'STATEN ISLAND'],['MANHATTAN', 'BROOKLYN', 'QUEENS', 'BRONX', 'STATEN ISLAND'])
    else:
        selected_options =  container.multiselect("Select one or more boroughs:",
            ['MANHATTAN', 'BROOKLYN', 'QUEENS', 'BRONX', 'STATEN ISLAND'])
    """


def build_header():
    """
    Writes the header and shows data table
    """
    #Laying out top section of the APP
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
    st.write("Please select the dataset and borough that you wish to visualize in the sidebar")


def build_data_view(data):
    "show the dataframe header"
    with st.beta_expander('Expand'):
        st.dataframe(data.reset_index().head(25), height=200)


def build_maps(data, year1, year2):
    "builds a map showing X"
    fmap = create_map(data, year1, year2)
    folium_static(fmap)


def hex_map(data):
    create_hex_map(DATA_1)




if __name__ == "__main__":

    # draw the webapp header
    build_header()    

    # display an example while full data loads
    # ...



    borough_selection = st.sidebar.selectbox("Please choose a borough", ('MANHATTAN', 'BROOKLYN', 'QUEENS', 'BRONX', 'STATEN ISLAND',))
    dataset_selection = st.sidebar.selectbox("Please choose a dataset", ('Water', 'Electricity'))


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
    #build_data_view(DATA.tds_by_year)

    # build several maps
    #build_maps(DATA, 2020, 2015)

    # build toggle to show different maps given options...
    # ...
    time = list(DATA.data.revenue_month.unique())
    time.sort()
    #time_selection = st.select_slider("Year-Month",time)
    
    #with st.spinner(text='Loading data'):
        #DATA_1 = DATA.data[DATA.data["revenue_month"] == time_selection]
        #st.success('App is ready')
    
    toggled_map = st.radio('Please select a map view', ('Mean consumption change between years', 
                                'Visual consumption over month', 'Consumption by borough'))
    
    if toggled_map == 'Mean consumption change between years':
        build_data_view(DATA.tds_by_year)
        #need unique years as list of options then offer using st slider

        build_maps(DATA, 2020, 2015)
        st.write(
            """
            The map above shows the change in consumption* between the years selected. 
            Red circles indicate a decrease, whilst green circles indicate an increase.

            *consumption is the average consumption for that place in a year
            """
            )
    
    elif toggled_map == 'Visual consumption over month':
        time_selection = st.select_slider("Year-Month",time)
        #with st.spinner(text='Loading data'):
        DATA_1 = DATA.data[DATA.data["revenue_month"] == time_selection]
            #st.success('App is ready')
        #st.write(DATA_1)
        #time_selection = st.select_slider("Year-Month",time)
        hex_map(DATA_1)
    
    
    


  