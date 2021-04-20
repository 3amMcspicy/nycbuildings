#!/usr/bin/env python

"""
Fetch data from REST API
"""

import requests
import pandas as pd

# URL for water dataset
WATER = "https://data.cityofnewyork.us/resource/66be-66yr.json"
COLUMNS = [
    # "development_name",
    "borough",
    "location",
    "tds",
    "revenue_month",
    "consumption_hcf",
]


class Water:
    """
    Request data from the REST API
    """

    def __init__(self):
        self.params = {
            "$offset": 0,
            "$limit": int(1e9),  # arbitrarily large to get all data
        }

    def get_all_data(self):
        """
        Get all 34.6K records and return as a dataframe.
        """
        # make request and get response object
        response = requests.get(
            url=WATER,
            params=self.params,
        )

        # check for errors
        response.raise_for_status()

        # return as dataframe at selected columns
        return pd.json_normalize(response.json())[COLUMNS]

    def get_data_with_kwargs(self, **kwargs):
        """
        Get data for only the specified month
        """
        # make request and get response object
        response = requests.get(
            url=WATER,
            params={**self.params, **kwargs},
        )

        # check for errors
        response.raise_for_status()

        # return as dataframe
        data = pd.json_normalize(response.json())

        # subset to columns of interest
        return data[COLUMNS]

    def get_data(self, **kwargs):
        """
        Get data for only the specified month
        """
        # make request and get response object
        response = requests.get(
            url=WATER,
            params={**self.params, **kwargs},
        )

        # check for errors
        response.raise_for_status()

        # return as dataframe w/ subset columns
        data = pd.json_normalize(response.json())
        return data[COLUMNS]


if __name__ == "__main__":

    # simple test for fetching Water data.
    TEST = Water()
    KWARGS = {
        "borough": "MANHATTAN",
        "revenue_month": "2020-01",
    }
    DATA = TEST.get_data(**KWARGS)
    print(DATA.head())
