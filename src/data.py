#!/usr/bin/env python

"""
Loading datasets.
"""
from water import Water
from electricity import Electricity
from coords import Coords


class Data:
    def __init__(self, *args, **kwargs):
        self.power = ""
        # get data and merge on 'tds'
        if  "Electricity" in args:
            self.power = "Electricity"
            self.data = Electricity().get_data(**kwargs)
        else: 
            self.power = "Water"
            self.data = Water().get_data(**kwargs)
        self.coords = Coords().get_all_data()

        # cleanup the data
        self.merge_coords()
        self.add_year_column()
        self.set_dtypes()

        # compute df of mean consumption by (tds x year)
        self.tds_by_year = None
        self.get_by_year_data()

        # add other pre-computed dataframes here 
        # ...


    def merge_coords(self):
        """
        Merge the coords into (lat,long) into the data
        """
        self.data = self.data.merge(self.coords, on='tds')


    def set_dtypes(self):
        """
        Set the datatypes to intended types
        """
        self.data.latitude = self.data.latitude.astype(float)
        self.data.longitude = self.data.longitude.astype(float)
        self.data.year = self.data.year.astype(int)     
        if self.power == "Electricity": 
            self.data.consumption_kwh = self.data.consumption_kwh.astype(float)
        else:
           self.data.consumption_hcf = self.data.consumption_hcf.astype(float)


    def add_year_column(self):
        """
        Create a new column with the year from revenue_month
        """
        years = self.data['revenue_month'].apply(lambda x: int(x.split("-")[0]))
        self.data['year'] = years
     

    def get_by_year_data(self):
        """
        Get difference in the mean consumption between years.
        """
        if self.power == "Electricity":
            self.tds_by_year = (
                self.data.groupby(["tds", "year"])
                .consumption_kwh.mean()
            )
        else:
            self.tds_by_year = (
                self.data.groupby(["tds", "year"])
                .consumption_hcf.mean()
            )
