#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 19 10:01:38 2018

@author: ggaregnani
"""
from . import plant as pl
import requests
import pandas as pd


class PV_plant(pl.Plant):
    """
        The class describes a photovoltaic plant providing
        methods to compute different indicators. Additional parameters to
        Plant classs
    """
    def __init__(self, k_pv, **kwargs):
        """Initialize the base and height attributes.

        :param k_pv: Module efficiency at Standard Test Conditions [kW m^{-2}]
        """
        self.k_pv = k_pv
        # TODO: acceptable list of attributes
        for k in kwargs.keys():
            self.__setattr__(k, kwargs[k])

    def area(self):
        """Calculate and return the area of the pv system."""
        return self.peak_power / self.k_pv

    def compute_energy(self, irradiation):
        """Calculate the energy production on the base
           of the mean irradiation
        :param irradiation: mean irradiation [kWh/m2 year]
        :return: the energy produced by the pv panels [kWh/year]

        >>> pvplant = PV_plant(id='test',k_pv=0.15, efficiency=0.75,
        ...                    peak_power=3)
        >>> pvplant.compute_energy(1350)
        3037.5
        """
        return irradiation * self.peak_power * self.efficiency

    def profile(self, raw=False, mean=None, token=None):
        """
        Return the dataframe with Pv profile
        >>> pvplant = PV_plant(id='test', lat=34.125, long=39.814,
        ...                   k_pv=0.15, efficiency=0.75,
        ...                   peak_power=3)
        >>> pvplant.hourlyprofile = pvplant.profile()
        >>> min(pvplant.hourlyprofile['output'])
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
            'capacity': self.peak_power,
            'system_loss':  100 * (1-self.efficiency),
            'tracking': 0,
            'tilt': 30,
            'azim': 180,
            'format': 'json',
            'metadata': False,
            'raw': raw,
            'mean': mean,
        }
        r = s.get(url, params=args)
        # Parse JSON to get a pandas.DataFrame
        df = pd.read_json(r.text, orient='index')
        # modify the labels by deleting the year
        return df


if __name__ == "__main__":
    import doctest
    doctest.testmod()
