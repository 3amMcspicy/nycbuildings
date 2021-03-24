import streamlit as st
import pydeck as pdk
import pandas as pd
import numpy as np 

#Task 1: Loading the Datasets 

# Line 6 to 29 is loading the dataset from NYC Open Data.
# Each function returns the dataset in pandas dataframe format.
 
#Fetching water consumption data
def water_consumption_data():
    """
    This function fetches water consumption data from NYC Open Data. Returns a pandas dataframe.
    """
    URL = "https://data.cityofnewyork.us/resource/66be-66yr.json?$limit=50000"
    raw_water = pd.read_json(URL)
    return raw_water


#Fetching electricity consumption data
#TODO: Electricity data has 315k entries, the current URL only takes 50k
def electricity_consumption_data():
    """
    This function fetches electricty consumption data from NYC Open Data. Returns a pandas dataframe.
    """
    URL_2 = "https://data.cityofnewyork.us/resource/jr24-e7cr.json?$limit=50000"
    raw_electricity = pd.read_json(URL_2)
    return raw_electricity

#Fetching geo-coordinate data
def coordinate_data():
    """
    this function fetches coordinate data from NYC Open Data. Returns a pandas dataframe. 
    Alice note: this only returns 1000 rows of data, which is part of why there were so few rows at the end.
    """
    URL_3 = "https://data.cityofnewyork.us/resource/3ub5-4ph8.json?$limit=50000"
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
    """
    This function processes the water consumption data from NYC Open Data by removing irrelevant columns, removing rows with null tds values, 
    removing rows with null building number values, and converting the building number data to integer format.
    """
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
    data_formatted['location'] = data_formatted['location'].str.replace(r'\D', '').astype(str)

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
    """
    This function processes the electricity consumption data from NYC Open Data by removing irrelevant columns, removing rows with null tds values, 
    removing rows with null location values, and converting the location data to integer format.
    """
    data=electricity_consumption_data()
    #selecting columns
    data_formatted = data[['development_name', 'borough', 'account_name',
                            'location', 'tds', 'edp', 'revenue_month',
                            'service_start_date', 'service_end_date',
                            'current_charges', 'consumption_kwh']]
    
    #removes NaN or null values in TDS and location columns
    data_formatted = data_formatted.loc[pd.notna(data_formatted['tds'])]
    data_formatted = data_formatted.loc[pd.notna(data_formatted['location'])]

    #For location, selecting only those with BLD and extracting the number: this is causing errors. I havent investigated the data to see what is in the location column, but might need more/different cleaning. 
    data_formatted = data_formatted[data_formatted.location.str.contains('BLD', na =False)]
    data_formatted["location"]= data_formatted['location'].str.replace(r'\D','').astype(str)

    return data_formatted


#Processing coordinates data

# The columns kept from this dataset are:
# DEVELOPMENT, TDS #, BUILDING #, BOROUGH, HOUSE #, STREET, ADDRESS, CITY, LATITUDE,
# LONGTITUDE

# This dataset does not have NaN values in TDS, no processing needed.

def coordinate_clean():
    """
    this function selects only the columns of the coordinate data that are necessary for the analysis.
    Alice note: I realized one of the reasons you were getting so few rows of data at the end is that the url for the data above has only 1000 rows, compared to the data in your data folder. I have pointed
    this function at the csv data instead, as the coordinate data is unlikely to be frequently updated like the water and electricity data I assume. 
    """
    #data=coordinate_data() <<as noted above, this data set only has 1000 rows so I switched to using your csv as a data source until we can figure out what's going on with the json data.
    #I renamed the columns of the csv data below to the names from the json data you were getting from the city so that subsequent code does not need to be changed again (hopefully) if you go back to using the json data
    #instead of the csv data.
   #data = pd.read_csv('./nycbuildings/dataset/NYCHA_Residential_Addresses.csv').rename(columns={"DEVELOPMENT" : "development", "TDS #" : "tds", "BUILDING #" : "building", 
    #                    "BOROUGH" : "borough", "HOUSE #" : "house", "STREET" : "street", "ADDRESS" : "address", "CITY" : "city", "LATITUDE" : "latitude", "LONGITUDE" : "longitude"})

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
    """
    This function combines the dataframe of coordinate data with the dataframe of water use data by tds number and building/location.
    """

    a1 = coordinate_clean()
    a2 = water_clean()
    a3 = a1.merge(a2, left_on = ['tds', 'building'], right_on = ['tds', 'location']) 
    
    return a3



#Electricity + GPS
# """
# Merging electricity dataset with Coordinates based on TDS and building number.

# There's only 379 columns
# """
def merge_electricity_gps():
    """
    This function combines the dataframe of coordinate data with the dataframe of electricity use data by tds number and building/location.
    """
    
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

#test
waterdata = merge_water_gps()
#elecdata=merge_electricity_gps()
#print water data onto app (temporary, just for ease of troubleshooting/seeing how many records there are)
st.write(waterdata)

#Plotting map coordinates
# Map functions 
def map(data, lat, lon, zoom):
    """
    this function plots water consumption as bars using latitude and longitude.
    """
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
                get_position=["longitude", "latitude"],
                radius=100,
                elevation_scale=1,
                elevation_range=[0, 1000],
                pickable=True,
                extruded=True,
            ),
        ]
    ))

#Setting the midpoint of our map location
midpoint = (np.average(waterdata["latitude"]), np.average(waterdata["longitude"]))

map(waterdata,midpoint[0], midpoint[1], 11)
#map(elecdata, midpoint[0], midpoint[1], 11)
# Filtering data by year/month selected
# Filtering data by electricity/water

