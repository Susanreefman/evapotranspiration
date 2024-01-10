#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Evapotranspiration
Description: Calculation of reference evapotranspiration through penman-monteith method
Author: Susan Reefman
Date: 13/09/2023
Version:1.1
"""

# Import modules
import sys
import pandas as pd
import math
import argparse
 
# Constants
albedo = 0.23
a_s = 0.25
b_s = 0.50

# Functions
def parse_args():
    """parse command-line arguments for input and output files"""
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file",
                        help="""The location and name to meteorological data in CSV format""",
                        required=True)
    parser.add_argument("-r", "--result",
                        help="""The location and name result file in CSV format""",
                        required=True)
    return parser.parse_args()


def read_data(file):
    "Read file and create dataframe"

    try:
        df = pd.read_csv(file)
            
    except FileNotFoundError:
        print(f"File '{file}' not found.")
    except IOError as e:
        print(f"An error occurred while reading the file: {e}")

    return df


def calculate_VPD(Tmin, Tmax, RHmin, RHmax):
    """Calculate vapour pressure curve
    return mean saturation vapour pressure (es) and actual vapour pressure (ea)"""
        
    e0T_min = 0.618 * math.exp((17.27 * Tmin) / (Tmin + 237.3))
    e0T_max = 0.618 * math.exp((17.27 * Tmax) / (Tmax + 237.3))

    es = (e0T_min + e0T_max) / 2
    ea = ((e0T_min * RHmax) + (e0T_max * RHmin)) / 200
    
    return es, ea
    

def calculate_delta(T_mean):
    """Get vapour pressure from mean temperature
    return delta """
    return 4098 * 0.6108 * math.exp(17.27 * T_mean / (T_mean + 237.3)) / ((T_mean + 237.3) ** 2)
    

def Rn(lat, doy, n, ea, T_min, T_max, altitude):
    """Calculate and return solar radiation"""
    latitude = lat*math.pi/180
    
    d_r = 1 + 0.033 * math.cos(2 * math.pi * doy / 365)
    solar_declination = 0.409 * math.sin(2 * math.pi * doy / 365 - 1.39)
    sunset_hour_angle = math.acos(-math.tan(latitude) * math.tan(solar_declination))
    Ra = 24 * 60 / math.pi * 0.082 * d_r * (sunset_hour_angle * math.sin(latitude) * math.sin(solar_declination) + math.cos(latitude) * math.cos(solar_declination) * math.sin(sunset_hour_angle))
    
    N = (24*sunset_hour_angle) / math.pi 
    Rs = (a_s + ((b_s*n)/N))*Ra
    Rs0 = (0.75 + (2e-5)*altitude)*Ra
    
    Rns = (1-albedo)*Rs
    Rnl = 4.903e-09 * (((T_min+273.16)**4+(T_max + 273)**4)/2) * (0.34 - (0.14 * (ea ** 0.5))) * (1.35 * Rs / Rs0 - 0.35)
    
    return Rns-Rnl    


def penman_monteith(T, delta, wind_speed, Rn, air_pressure, gamma, ea, es):
    """Calculate evapotranspiration using the Penman-Monteith equation."""    
    return ((0.408 * delta * Rn) + (gamma * (900/(T + 273))*wind_speed*(es-ea))) / (delta + gamma*(1 + (0.34 * wind_speed)))

    
def main():
    """Main function"""
    
    # Parse and read file to dataframe
    args = parse_args()
    df = read_data(args.file)
    
    # For each date calculate evapotranspiration
    for index, row in df.iterrows():
        lat = row['lat']
        Tmin = row['Tmin']
        Tmax = row['Tmax']
        Tmean = row['Tmean']
        RHmin = row['RHmin']
        RHmax = row['RHmax']
        uz = row['uz']
        n = row['n']
        pressure = row['pressure']
        doy = row['doy']
        altitude = row['z']
        
        delta = calculate_delta(Tmean)
        
        gamma = 0.000665*pressure 
        
        es, ea = calculate_VPD(Tmin, Tmax, RHmin, RHmax)
        
        solar_radiation = Rn(lat, doy, n, ea, Tmin, Tmax, altitude)
    
        ET0 = penman_monteith(Tmean, delta, uz, solar_radiation, pressure, gamma, ea, es)
                
        df.at[index, 'ET0'] = round(ET0,1)
            
    # Save to csv
    df.to_csv(args.result, index=False)

    print(f'Results saved in "{args.result}"')
    
    return 0


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nScript terminated by the user.")
        sys.exit(1)
