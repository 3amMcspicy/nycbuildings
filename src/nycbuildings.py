import streamlit as st
import requests
import pandas as pd
import numpy as np 

#Loading the Datasets 
"""
Line 6 to 29 is loading the dataset from NYC Open Data.
Each function returns the dataset in JSON format.
""" 
#Fetching water consumption data
def water_consumption_data():
    URL = "https://data.cityofnewyork.us/resource/66be-66yr.json"
    response = requests.get(url=URL)
    return response.json()

water_consumption_data()

#Fetching electricity consumption data
def electricity_consumption_data():
    URL_2 = "https://data.cityofnewyork.us/resource/jr24-e7cr.json"
    response = requests.get(url=URL_2)
    return response.json()

#Fetching geo-coordinate data
def coordinate_data():
    URL_3 = "https://data.cityofnewyork.us/resource/3ub5-4ph8.json"
    response = requests.get(url = URL_3)
    return response.json()


#Formatting Data - not done yet


#Plotting map coordinates
# Map functions 
# Filtering data by year/month selected
# Filtering data by electricity/water

