#!/usr/bin/env python

"""
Fetch data from REST API
"""

import requests
import pandas as pd


ELECTRICITY = "https://data.cityofnewyork.us/resource/jr24-e7cr.json"
COLUMNS = [
    # "development_name",
    "borough",
    "location",
    "tds",
    "revenue_month",
    "consumption_kwh",
]


class Electricity:
    """
    Request data from the REST API
    """

    def __init__(self):
        self.params = {
            "$offset": 0,
            "$limit": int(1e9),  # arbitrarily large to get all data
        }

    def get_data(self, **kwargs):
        """
        Get data for only the specified month
        """
        # make request and get response object
        response = requests.get(
            url=ELECTRICITY,
            params={**self.params, **kwargs},
        )

        # check for errors
        response.raise_for_status()

        # return as dataframe w/ subset columns
        data = pd.json_normalize(response.json())
        return data[COLUMNS]


if __name__ == "__main__":

    # simple test for fetching Electricity data.
    TEST = Electricity()
    KWARGS = {
        "borough": "MANHATTAN",
        "revenue_month": "2020-01",
    }
    DATA = TEST.get_data(**KWARGS)
    print(DATA.head())
