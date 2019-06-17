#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 19 10:01:38 2018

@author: ggaregnani
"""
from . import plant as pl
import requests
import pandas as pd


class ST_plant(pl.Plant):
    """
    The class describes a solarthermal plant providing
    methods to compute different indicators. Additional parameters to
    Plant class

    :param area: Surface area of the module [m^{2}]
    """
    def __init__(self, area, **kwargs):
        """Initialize the base and height attributes."""
        self.area = area
        # TODO: acceptable list of attributes
        for k in kwargs.keys():
            self.__setattr__(k, kwargs[k])

    def compute_energy(self, irradiation):
        """Calculate the energy production on the base"""
        return irradiation * self.area * self.efficiency

    def profile(self, mean=None, token=None):
        """
        Return the dataframe with Pv profile
        >>> stplant = ST_plant(id='test', lat=34.125, long=39.814,
        ...                   area=6, efficiency=0.90)
        >>> stplant.hourlyprofile = stplant.profile()
        >>> min(stplant.hourlyprofile['output'])
        0.0
        """
        api_base = 'https://www.renewables.ninja/api/'
        s = requests.session()
        # Send token header with each request
        if token:
            s.headers = {'Authorization': 'Token ' + token}
        url = api_base + 'data/pv'
        args = {
            'lat': self.lat,
            'lon': self.long,
            'date_from': '2014-01-01',
            'date_to': '2014-12-31',
            'dataset': 'merra2',
            'capacity': 1,
            'system_loss':  100 * (1-self.efficiency),
            'tracking': 0,
            'tilt': 30,
            'azim': 180,
            'format': 'json',
            'metadata': False,
            'raw': True,
            'mean': mean,
        }
        r = s.get(url, params=args)
        # Parse JSON to get a pandas.DataFrame
        df = pd.read_json(r.text, orient='index')
        # modify the labels by deleting the year
        df['output'] = ((df['diffuse'] + df['direct']) * self.area)
        return df


if __name__ == "__main__":
    import doctest
    doctest.testmod()
