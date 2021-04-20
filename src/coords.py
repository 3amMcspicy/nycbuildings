#!/usr/env/bin python

"""
Coordinate projection of data.

In order to run an analysis by building, you can use a 
combination of TDS and building number which gives a unique 
identifier for each building
"""

import requests
import pandas as pd


COORDS = "https://data.cityofnewyork.us/resource/3ub5-4ph8.json"
COLUMNS = [
    "tds",
    "building",
    "latitude",
    "longitude",
]


class Coords:
    def __init__(self):
        self.params = {"$limit": int(1e9), "$offset": 0}

    def get_all_data(self):
        """
        Get all records and return as a dataframe.
        """
        # make request and get response object
        response = requests.get(
            url=COORDS,
            params=self.params,
        )

        # check for errors
        response.raise_for_status()

        # return as dataframe at selected columns
        data = pd.json_normalize(response.json())[COLUMNS]

        # convert lat,long to floats
        data[["latitude", "longitude"]] = data[["latitude", "longitude"]].astype(float)
        return data


if __name__ == "__main__":

    DATA = Coords().get_all_data()
    print(DATA.shape)
    print(DATA.columns)
    print(DATA.head())
