#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 19 10:01:38 2018

@author: ggaregnani
"""
import json

import pandas as pd

from . import plant as pl
from . import cached_requests as cr


class PvPlant(pl.Plant):
    """
        The class describes a photovoltaic plant providing
        methods to compute different indicators. Additional parameters to
        Plant classs
    """

    resource = "data/pv"

    def __init__(self, k_pv, peak_power=3, efficiency=0.75, **kwargs):  # kW
        """Initialize the base and height attributes.

        :param k_pv: Module efficiency at Standard Test Conditions [kW m^{-2}]
        """
        super().__init__(**kwargs)
        self.k_pv = k_pv
        self.peak_power = peak_power
        self.area = self.pv_area()
        self.efficiency = efficiency

    def pv_area(self):
        """Return the area required by the pv system."""
        return self.peak_power / self.k_pv

    def compute_energy(self, irradiation):
        """Calculate the energy production on the base
           of the mean irradiation
        :param irradiation: mean irradiation [kWh/kWp/year]
        :return: the energy produced by the pv panels [kWh/year]

        >>> pvplant = PvPlant(id_plant='test',k_pv=0.15, efficiency=0.75,
        ...                    peak_power=3)
        >>> pvplant.compute_energy(1350)
        3037.5
        """
        return irradiation * self.peak_power * self.efficiency

    def profile(
        self,
        date_from="2014-01-01",
        date_to="2014-12-31",
        dataset="merra2",
        tracking=0,
        tilt=30,
        azim=180,
        mean=None,
    ):
        """
        Return the dataframe with Pv profile
        >>> pvplant = PvPlant(id_plant='test', lat=34.125, lon=39.814,
        ...                   k_pv=0.15, efficiency=0.75,
        ...                   peak_power=3)
        >>> pvplant.hourlyprofile = pvplant.profile()
        >>> min(pvplant.hourlyprofile['output'])
        0.0
        """
        args = {
            "lat": self.lat,
            "lon": self.lon,
            "date_from": date_from,
            "date_to": date_to,
            "dataset": dataset,
            "capacity": 1,
            "system_loss": 0,
            "tracking": tracking,
            "tilt": tilt,
            "azim": azim,
            "format": "json",
            "raw": True,
            "mean": mean,
        }
        jsn = cr.get(self.api_base + self.resource, params=args)
        if jsn:
            # Parse JSON to get a pandas.DataFrame
            info = json.loads(jsn)
            df = pd.read_json(json.dumps(info["data"]), orient="index")
            df["electricity"] = df["electricity"] * self.peak_power * self.efficiency
            # modify the labels by deleting the year
            return df

    def compute_profile_energy(self, df):
        """Return a dataframe with the hourly PV energy produced by the plant
        """
        df["energy_el"] = df["irradiance_direct"] * self.peak_power * self.efficiency
        return df


if __name__ == "__main__":
    import doctest

    optionflags = doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE | doctest.REPORT_NDIFF
    doctest.testmod(optionflags=optionflags)
