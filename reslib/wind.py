#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 19 10:01:38 2018

@author: ggaregnani
"""
import json

from . import plant as pl
from . import cached_requests as cr

import pandas as pd

# TODO: the idea is to set also a class for the planning rules in order to
# have the possibility to analyze potential territorial conflicts. this
# is a first tentative


class Wind_plant(pl.Plant):
    """
    The class describes a wind plant providing
    methods to compute different indicators. Additional parameters to
    Plant class
    """
    resource = 'data/wind'

    def __init__(self,
                 efficiency=0.4,
                 swept_area=None,
                 height=None,
                 model=None, **kwargs):
        """Initialize the base and height attributes."""
        super().__init__(**kwargs)
        self.efficiency = efficiency
        self.swept_area = swept_area
        self.height = height
        self.model = model

    def compute_energy(self, speed, rho=1.225, working_hours=1700,
                       conv=1/1000):
        """Calculate the energy production on the base of the mean
           velocity

        :param speed: wind mean velocity [m/s]
        :param rho: air density [kg/m3]
        :param conv: conversion from Wh to kWh

        return the energy production according to the conversion factor,
        (default unit) kWh

        >>> plant = Wind_plant(id_plant="test", swept_area=8495, height=50,
        ...                    efficiency=0.4, model='Enercon E48 800')
        >>> plant.compute_energy(speed=12)
        6113953.44
        """
        e_p = (0.5 * self.efficiency * rho * self.swept_area *
               speed**3) * working_hours * conv
        return e_p

    def profile(self,
                date_from='2014-01-01',
                date_to='2014-12-31',
                dataset='merra2',
                height=None,
                model=None,
                raw=False, mean=None):
        """
        Return the dataframe with Wind turbine profile
        >>> windplant = Wind_plant(id='test', lat=34.125, long=39.814,
        ...                        peak_power=800, height=50, swept_area=8495,
        ...                        model='Enercon E48 800')
        >>> windplant.hourlyprofile = windplant.profile()
        >>> min(windplant.hourlyprofile['output'])
        0.0
        """
        args = {
            'lat': self.lat,
            'lon': self.lon,
            'date_from': date_from,
            'date_to': date_to,
            'dataset': dataset,
            'height': height,
            'capacity': self.peak_power,
            'turbine': model,
            'format': 'json',
            'metadata': False,
            'raw': raw,
            'mean': mean,
        }
        jsn = cr.get(self.api_base + self.resource, params=args)
        if jsn:
            # Parse JSON to get a pandas.DataFrame
            info = json.loads(jsn)
            df = pd.read_json(json.dumps(info["data"]), orient='index')
            # modify the labels by deleting the year
            return df


if __name__ == "__main__":
    import doctest
    doctest.testmod()
