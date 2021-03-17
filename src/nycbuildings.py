import streamlit as st
import requests
import pandas as pd
import numpy as np 

#Task 1: Loading the Datasets 
"""
Line 6 to 29 is loading the dataset from NYC Open Data.
Each function returns the dataset in pandas dataframe format.
""" 
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
"""
This section is to remove columns that are unnecessary for mapping the data,
to save space and computation power. Tables will be merged with TDS # and 
any inconsistent data will be removed. Note that the column names in the dataframe
is formatted differently than the names in the comments.

The TDS # in the processed dataframe is not a string but saved as an int.
"""

#Processing water consumption data
"""
The columns kept from this dataset are:
Development Name, Borough, Account Name, Location, TDS #, EDP, Revenue Month,
Service Start Date, Service End Date, Current Charges, Consumption (HCF)

TODO: remove empty entries where TDS is Null. Might consider adding them if basic maps work first.

"""

def water_clean():
    data = water_consumption_data()

    #selecting columns
    data_formatted = data[['development_name', 'borough', 'account_name',
                            'location', 'tds', 'edp', 'revenue_month',
                            'service_start_date', 'service_end_date',
                            'current_charges', 'consumption_hcf']]
    
    #removes NaN or null values in TDS column
    data_formatted = data_formatted.loc[pd.notna(data_formatted['tds'])]
    return data_formatted



#Processing electricity consumption data
"""
The columns kept from this dataset are:
Development Name, Borough, Account Name, Location, TDS #, EDP, Revenue Month,
Service Start Date, Service End Date, Current Charges, Consumption (KWH)

TODO: remove empty entries where TDS is Null
"""
def electricity_clean():
    data = electricity_consumption_data()

    #selecting columns
    data_formatted = data[['development_name', 'borough', 'account_name',
                            'location', 'tds', 'edp', 'revenue_month',
                            'service_start_date', 'service_end_date',
                            'current_charges', 'consumption_kwh']]
    
    #removes NaN or null values in TDS column
    data_formatted = data_formatted.loc[pd.notna(data_formatted['tds'])]
    return data_formatted

#Processing coordinates data
"""
The columns kept from this dataset are:
DEVELOPMENT, TDS #, BUILDING #, BOROUGH, HOUSE #, STREET, ADDRESS, CITY, LATITUDE,
LONGTITUDE

This dataset does not have NaN values in TDS, no processing needed.
"""
def coordinate_clean():
    data = coordinate_data()

    #selecting columns
    data_formatted = data[['development', 'tds', 'building',
                            'borough', 'house', 'street','address','city',
                            'latitude','longitude']]
    
    return data_formatted



#Merging the data with coordinates. 


#Plotting map coordinates
# Map functions 
# Filtering data by year/month selected
# Filtering data by electricity/water

