# evapotranspiration

## Introduction
This project calculates the reference evapotranspiration rate (ET0) from meteorological data by using the penman-monteith method recommended by the Food and Agriculture organisation (FAO). More information and definitions of all needed parameters of this equation can be found in the 'Crop evapotranspiration - Guidelines for computing crop water requirements - FAO Irrigation and drainage paper 56' (https://www.fao.org/3/x0490e/x0490e00.htm) 


## Installation
To use this script use the sample file or download meteorlogical data from https://openweathermap.org/. 
The input file should contain meteorological data per day including:
- latitude as decimal coordinates
- minimum temperature in degrees celcius
- maximum temperature in degrees celcius
- mean temperature in degrees celcius
- minimum relative humidity in percentage
- maximum relative humidity in percentage
- average windspeed at a height of 2m
- sunlight hours 
- pressure in KpA
- day in the year
- altitude

The script was developed in the programming language Python (version 3.11.4).

## Usage
To use the script use the following command:

```bash
$ python3 evapotranspiration.py -f [input file] -r [output file]
```
Where `-f` represents the input file in CSV format with meteorlogical data and `-r` represents the name of the output file where the calculated data is saved in CSV format. 

## Contact
For questions reach out to h.s.reefman@st.hanze.nl
