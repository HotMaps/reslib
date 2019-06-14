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

## Examples

### Photovoltaic plant

In this example a photovoltaic plant is created:

```
>>> import plant.pv as pv
>>> pv_plant = pv(id='test', k_pv=0.15, efficiency=0.75,
...               peak_power=3)
>>> pvplant.compute_energy(1350)
>>> pvplant = PV_plant(id='test', lat=34.125, long=39.814,
...                   k_pv=0.15, efficiency=0.75,
...                   peak_power=3)
>>> pvplant.hourlyprofile = pvplant.profile()
>>> min(pvplant.hourlyprofile['output'])
```

Here a wind turbine:

```
>>> import plant.wind as Wind_plant
>>> windplant = Wind_plant(id='test', lat=34.125, long=39.814,
...                        peak_power=800, height=50, swept_area=8495,
...                        model='Enercon E48 800')
>>> windplant.hourlyprofile = windplant.profile()
>>> min(windplant.hourlyprofile['output'])
```

and, finally, a solar thermal plant

```
>>> import plant.wind as Wind_plant
>>> windplant = Wind_plant(id='test', lat=34.125, long=39.814,
...                        peak_power=800, height=50, swept_area=8495,
...                        model='Enercon E48 800')
>>> windplant.hourlyprofile = windplant.profile()
>>> min(windplant.hourlyprofile['output'])
```


