#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 19 10:01:38 2018

@author: ggaregnani
"""
import numpy as np

from . import cached_requests as cr


class Financial:
    def __init__(self, investement_cost, yearly_cost, plant_life, **kwargs):
        """

        The class describes the financial feasibility of a plant providing
        methods to compute different indicators

        :param investement_cost: Total investment [positive real number]
        :param yearly_cost: (Outflow) variable cost [positive real number]
        :param plant_life: number of year of plant life [integer]
        """
        self.investement_cost = investement_cost
        self.yearly_cost = yearly_cost
        self.plant_life = plant_life
        for k in kwargs.keys():
            self.__setattr__(k, kwargs[k])

    def lcoe(self, energy_production, i_r=0.03):
        """
        Computes th Levelized cost of Energy

        :param i_r: discount rate [0.0< positive real number<1.0]
        :param energy_production: total energy generated during a year
                                  [kWh/year] [ positive real number]
        :param self: Feasibility object with costs and plant life
        :returns: the levelized cost of energy [Euro/kWh]

        test: geothermal savings oil
        >>> feasability = Financial(7473340, 4918, 27)
        >>> feasability.lcoe(6962999, 0.03)
        0.05926970484809364

        test: geothermal savings gas
        """

        flows = []
        flows.append(self.investement_cost)

        for i in range(1, self.plant_life + 1):
            flow_k = self.yearly_cost * np.power(float(1 + i_r), -i)
            flows.append(flow_k)

        tot_inv_and_sum_annual_discounted_costs = sum(flows)

        discounted_ener = []

        for i in range(1, self.plant_life + 1):
            discounted_ener_k = energy_production * np.power(float(1 + i_r), -i)
            discounted_ener.append(discounted_ener_k)

        total_discounted_energy = sum(discounted_ener)

        lcoe = tot_inv_and_sum_annual_discounted_costs / total_discounted_energy
        return lcoe


# TODO a class plant exists in many of our codes, we have to unify them
class Plant:
    """

        The class describes the financial feasibility of a plant providing
        methods to compute different indicators

        :param investement_cost: Total investment [positive real number]
        :param yearly_cost: (Outflow) variable cost [positive real number]
        :param plant_life: number of year of plant life [integer]
    """

    api_base = "https://www.renewables.ninja/api/"

    def __init__(
        self,
        id_plant,
        lat=None,
        lon=None,
        peak_power=None,
        efficiency=None,
        energy_production=None,
    ):
        """Initialize the base and height attributes."""
        self._lat = None
        self._lon = None

        self.id = id_plant
        self.lat = lat
        self.lon = lon
        self.peak_power = peak_power
        self.energy_production = energy_production
        self.efficiency = efficiency

    def working_hours(self):
        """Calculate and return the area of the rectangle."""
        return self.energy_production / self.peak_power

    def _get_lat(self):
        return self._lat

    def _set_lat(self, lat):
        if lat is None:
            self._lat = None
        else:
            self._lat = cr.round_coords(lat)[0]

    lat = property(
        fget=_get_lat,
        fset=_set_lat,
        doc="""
    >>> plant = Plant("PV", lat=45.2345678)
    >>> plant.lat
    45.0
""",
    )

    def _get_lon(self):
        return self._lon

    def _set_lon(self, lon):
        if lon is None:
            self._lon = None
        else:
            self._lon = cr.round_coords(lon)[0]

    lon = property(
        fget=_get_lon,
        fset=_set_lon,
        doc="""
    >>> plant = Plant("PV", lon=10.8945678)
    >>> plant.lat
    10.5
""",
    )


if __name__ == "__main__":
    import doctest

    doctest.testmod()
