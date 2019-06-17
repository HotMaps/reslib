#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 17 09:30:15 2019

@author: ggaregnani
"""

# TODO: the idea is to set also a class for the planning rules in order to
# have the possibility to analyze potential territorial conflicts. this
# is a first tentative


class Planning_rules:
    def __init__(self, area_target, energy_target,
                 area_available, energy_available):
        """
        The class defines the rule in the use of the energy reosurce

        :param area_target: max availavble area to be exploited
        :param energy_target: target of the administrative unit
        of energy production
        :param area_available: total exploitable area
        :param energy_available: total energy available
        """
        self.area_target = area_target
        self.energy_target = energy_target
        self.area_available = area_available
        self.energy_available = energy_available

    def n_plants(self, plant):
        """
        Compute the number of plants in a region accounting for the minimum
        bewteen energy and area targets

        :param plant: plant object
        """
        n_plants_area = self.area_target / plant.area
        n_plants_energy = self.energy_target / plant.energy_production
        return min(int(n_plants_area), int(n_plants_energy))

    def validity(self):
        """
        Verify the consistency between constraints
        """
        consistency = ((self.area_target <= self.area_available) *
                       (self.energy_target <= self.energy_available))
        return consistency
