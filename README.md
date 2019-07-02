# reslib

## Summary
Library with the class describing a renewable plant and all the useful methods for defining a RES plant. The library is currently used by the wind and solar CM modules

## Description

This project provides Class and Methods to define renewable energy plants:
- Photovoltaic Plant
- Wind Turbine
- Solar Thermal Plant

The Class provide also a method to compute the hourly profile based on the renewable.ninja API.
For more information see the [documentaion](https://www.renewables.ninja/documentation)

## How to install


```
pip install git+https://github.com/HotMaps/reslib.git
```

## Environmental variables

The environmental variable `RES_NINJA_TOKENS` set the tokens available
to be used by the library.

Use the environmental variable: `LRU_CACHE_MAXSIZE` to set the maximum size
of the LRU cache, the default value is 2048.



## Examples

### Photovoltaic plant

In this example a photovoltaic plant is created:

```
>>> import reslib.pv as pv
>>> pvplant = pv.PV_plant(id='test', lat=34.125, long=39.814,
...                   k_pv=0.15, efficiency=0.75,
...                   peak_power=3)
>>> pvplant.compute_energy(1350)
>>> pvplant.hourlyprofile = pvplant.profile()
```

Here a wind turbine:

```
>>> import reslib.wind as wind
>>> windplant = wind.Wind_plant(id='test', lat=34.125, long=39.814,
...                             peak_power=800, height=50, swept_area=8495,
...                             model='Enercon E48 800')
>>> windplant.hourlyprofile = windplant.profile()
```
and, finally, a solar thermal plant

```
>>> import reslib.st as st
>>> stplant = st.ST_plant(id='test', lat=34.125, long=39.814,
...                         area=6)
>>> stplant.hourlyprofile = stplant.profile()
```

## Authors

Giulia Garegnani<sup>1</sup>
Pietro Zambelli<sup>1</sup>

<sup>1</sup> Eurac Research

Institute for Renewable Energy
VoltaStraße/Via Via A. Volta 13/A
39100 Bozen/Bolzano


## Acknowledgement

We would like to convey our deepest appreciation to the Horizon 2020
[Hotmaps Project](http://www.hotmaps-project.eu/) (Grant Agreement number 723677),
which provided the funding to carry out the present investigation.

