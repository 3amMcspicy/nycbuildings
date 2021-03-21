import streamlit as st
import pydeck as pdk
import pandas as pd
import numpy as np 

#Task 1: Loading the Datasets 

# Line 6 to 29 is loading the dataset from NYC Open Data.
# Each function returns the dataset in pandas dataframe format.
 
#Fetching water consumption data
def water_consumption_data():
    URL = "https://data.cityofnewyork.us/resource/66be-66yr.json"
    raw_water = pd.read_json(URL)
    return raw_water


#Fetching electricity consumption data
def electricity_consumption_data():
    URL_2 = "https://data.cityofnewyork.us/resource/jr24-e7cr.json"
    raw_electricity = pd.read_json(URL_2)
    return raw_electricity

#Fetching geo-coordinate data
def coordinate_data():
    URL_3 = "https://data.cityofnewyork.us/resource/3ub5-4ph8.json"
    raw_coordinate = pd.read_json(URL_3)
    return raw_coordinate


#Task 2: Formatting Data - incomplete

# This section is to remove columns that are unnecessary for mapping the data,
# to save space and computation power. Tables will be merged with TDS # and 
# any inconsistent data will be removed. Note that the column names in the dataframe
# is formatted differently than the names in the comments.

# The TDS # in the processed dataframe is not a string but saved as an int.


#Processing water consumption data

# The columns kept from this dataset are:
# Development Name, Borough, Account Name, Location, TDS #, EDP, Revenue Month,
# Service Start Date, Service End Date, Current Charges, Consumption (HCF)

# TODO: Consider adding null entries back for TDS if basic maps work. This will require
#       more work to convert street address to GPS coordinates. I.e. edge cases.
# TODO: Consider adding entries with location that does not start with BLD back as points
# TODO: Consider entires that could not merge with GPS dataset



def water_clean():
    data = water_consumption_data()

    #selecting columns
    data_formatted = data[['development_name', 'borough', 'account_name',
                            'location', 'tds', 'edp', 'revenue_month',
                            'service_start_date', 'service_end_date',
                            'current_charges', 'consumption_hcf']]
    
    #removes NaN or null values in TDS column
    data_formatted = data_formatted.loc[(pd.notna(data_formatted['tds'])) & (data_formatted['tds'] != '#N/A')]
    
    #casting TDS to int
    data_formatted['tds'] = pd.to_numeric(data_formatted['tds'])
    
    #For location, selecting only those with BLD and extracting the number
    data_formatted = data_formatted[data_formatted.location.str.contains('BLD', na =False)]
    data_formatted['location'] = data_formatted['location'].str.replace(r'\D', '').astype(int)

    return data_formatted



#Processing electricity consumption data

# The columns kept from this dataset are:
# Development Name, Borough, Account Name, Location, TDS #, EDP, Revenue Month,
# Service Start Date, Service End Date, Current Charges, Consumption (KWH)

# TODO: Consider adding null entries back for TDS if basic maps work. This will require
#       more work to convert street address to GPS coordinates. I.e. edge cases.
# TODO: Consider adding entries with location that does not start with BLD back as points
# TODO: Consider entires that could not merge with GPS dataset


def electricity_clean():
    data = electricity_consumption_data()

    #selecting columns
    data_formatted = data[['development_name', 'borough', 'account_name',
                            'location', 'tds', 'edp', 'revenue_month',
                            'service_start_date', 'service_end_date',
                            'current_charges', 'consumption_kwh']]
    
    #removes NaN or null values in TDS column
    data_formatted = data_formatted.loc[pd.notna(data_formatted['tds'])]

    #For location, selecting only those with BLD and extracting the number
    data_formatted = data_formatted[data_formatted.location.str.contains('BLD', na =False)]
    data_formatted['location'] = data_formatted['location'].str.replace(r'\D', '').astype(int)

    return data_formatted



#Processing coordinates data

# The columns kept from this dataset are:
# DEVELOPMENT, TDS #, BUILDING #, BOROUGH, HOUSE #, STREET, ADDRESS, CITY, LATITUDE,
# LONGTITUDE

# This dataset does not have NaN values in TDS, no processing needed.

def coordinate_clean():
    data = coordinate_data()

    #selecting columns
    data_formatted = data[['development', 'tds', 'building',
                            'borough', 'house', 'street','address','city',
                            'latitude','longitude']]
    
    return data_formatted



#Merging formatted datasets with the coordinates dataset. 

# This section is to merge the coordinates dataset with the other two dataset individually.
# If all 3 were merged together, it is likely to lose more entry points.
# The website displays electricity or water consumption, not both at the same time.


#Water + GPS

# Merging dataset based on TDS and building number

# There's only 104 entries. 
# The data processing to fit to the GPS data removed many potential water consumption data

def merge_water_gps():
    a1 = coordinate_clean()
    a2 = water_clean()
    a3 = a1.merge(a2, left_on = ['tds', 'building'], right_on = ['tds', 'location'])

    return a3


#Electricity + GPS
# """
# Merging electricity dataset with Coordinates based on TDS and building number.

# There's only 379 columns
# """
def merge_electricty_gps():
    a1 = coordinate_clean()
    a2 = electricity_clean()
    a3 = a1.merge(a2, left_on = ['tds', 'building'], right_on = ['tds', 'location'])

    return a3




#Building the map
# This section of the code is to build the map for the users



#Laying out top section of the APP
row_1, row_2 = st.beta_columns((2,3))

with row_1:
    st.title("NYCHA electricy and water consumption data")

with row_2:
    st.write(
    """
    ##
    Examing how water consumption and electricity consumption in NYCHA developments. 
    The slider provides changes in consumption over time for some buildings.
    """    
    )

#test with water data
data = merge_water_gps()


#Plotting map coordinates
# Map functions 
def map(data, lat, lon, zoom):
    st.write(pdk.Deck(
        map_style="mapbox://styles/mapbox/dark-v10",
        initial_view_state={
            "latitude": lat,
            "longitude": lon,
            "zoom": zoom,
            "pitch": 50,
        },
        layers=[
            pdk.Layer(
                "HexagonLayer",
                data=data,
                get_position=["lon", "lat"],
                radius=100,
                elevation_scale=4,
                elevation_range=[0, 1000],
                pickable=True,
                extruded=True,
            ),
        ]
    ))

#Setting the midpoint of our map location
midpoint = (np.average(data["latitude"]), np.average(data["longitude"]))

map(data,midpoint[0], midpoint[1], 11)
# Filtering data by year/month selected
# Filtering data by electricity/water

