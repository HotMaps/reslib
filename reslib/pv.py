#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 19 10:01:38 2018

@author: ggaregnani
"""

from . import plant as pl
from . import cached_requests as cr

import numpy as np
import pandas as pd


class PV_plant(pl.Plant):
    """
        The class describes a photovoltaic plant providing
        methods to compute different indicators. Additional parameters to
        Plant classs
    """
    def __init__(self, lat, lon, k_pv,
                 date_from='2014-01-01',
                 date_to='2014-12-31',
                 dataset='merra2',
                 peak_power=3,  # kW
                 efficiency=0.75,
                 tracking=0,
                 tilt=30,
                 azim=180):
        """Initialize the base and height attributes.

        :param k_pv: Module efficiency at Standard Test Conditions [kW m^{-2}]
        """
        self.k_pv = k_pv
        # fix coordinates resolution to make them cacheable
        self.lat, self.lon = cr.round_coords(lat, lon, res=0.5, ndigits=1)
        # acept all the other parameters
        self.date_from = date_from
        self.date_to = date_to
        self.dataset = dataset
        self.peak_power = peak_power
        self.efficiency = efficiency
        self.tracking = tracking
        self.tilt = tilt
        self.azim = azim

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

    def profile(self, raw=False, mean=None):
        """
        Return the dataframe with Pv profile
        >>> pvplant = PV_plant(id='test', lat=34.125, lon=39.814,
        ...                   k_pv=0.15, efficiency=0.75,
        ...                   peak_power=3, tokens=[])
        >>> pvplant.hourlyprofile = pvplant.profile()
        >>> min(pvplant.hourlyprofile['output'])
        0.0
        """
        api_base = 'https://www.renewables.ninja/api/'
        url = api_base + 'data/pv'
        args = {
            'lat': self.lat,
            'lon': self.lon,
            'date_from': self.date_from,
            'date_to': self.date_to,
            'dataset': self.dataset,
            'capacity': self.peak_power,
            'system_loss':  100 * (1 - self.efficiency),
            'tracking': self.tracking,
            'tilt': self.tilt,
            'azim': self.azim,
            'format': 'json',
            'metadata': False,
            'raw': raw,
            'mean': mean,
        }
        json = cr.get(url, params=args)
        if json:
            # Parse JSON to get a pandas.DataFrame
            df = pd.read_json(json, orient='index')
            # modify the labels by deleting the year
            return df


if __name__ == "__main__":
    import doctest
    optionflags=doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE | doctest.REPORT_NDIFF
    doctest.testmod(optionflags=optionflags)
