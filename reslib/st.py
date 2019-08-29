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


class ST_plant(pl.Plant):
    """
    The class describes a solarthermal plant providing
    methods to compute different indicators. Additional parameters to
    Plant class

    :param area: Surface area of the module [m^{2}]
    """

    resource = "data/pv"

    def __init__(self, area, efficiency=0.90, **kwargs):
        """Initialize the base and height attributes."""
        super().__init__(**kwargs)
        self.area = area
        self.efficiency = efficiency

    def compute_energy(self, irradiation):
        """Calculate the energy production on the base"""
        return irradiation * self.area * self.efficiency

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
        >>> stplant = ST_plant(id='test', lat=34.125, lon=39.814,
        ...                   area=6, efficiency=0.90)
        >>> stplant.hourlyprofile = stplant.profile()
        >>> min(stplant.hourlyprofile['output'])
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
            # modify the labels by deleting the year
            df["thermal"] = (
                (df["irradiance_diffuse"] + df["irradiance_direct"])
                * self.area
                * self.efficiency
            )
            return df


if __name__ == "__main__":
    import doctest

    doctest.testmod()
