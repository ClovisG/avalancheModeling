#!/usr/bin/env python
import cdsapi
c = cdsapi.Client()

from pandas import DataFrame, read_csv
import matplotlib.pyplot as plt
import pandas as pd
import csv


def normaliseDate(date):
    day = date[0:2]
    month = date[3:5]
    year = date[6:]
    return [day,month,year]

def normaliseHeure(heure):
    if (heure == "nan"):
        return '12:00'
    else:
        return heure[:3]+'00'

def normaliseNeige(neige):
    if(neige == "nan"):
        return 'undefined'
    else:
        return neige


# with open('avalanchesWeather.csv', mode='w') as outputFile:
#     dataWriter = csv.writer(outputFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)


# dataWriter.writerow(['Id', 'Orientation', 'Date', 'Heure', 'Neige', 'Lat', 'Long',
#             '2m_temperature','clear_sky_direct_solar_radiation_at_surface',
#             'large_scale_precipitation','large_scale_snowfall','snow_density','snow_depth',
#             'snowmelt'])

    # employee_writer.writerow(['John Smith', 'Accounting', 'November'])
    # employee_writer.writerow(['Erica Meyers', 'IT', 'March'])


inputFile = r'../data/avalanches_2018.10.10-17.12.xls'
df = pd.read_excel(inputFile)


# remove messy data
df = df[df['Decl a distance'] != 'true']


for i in range(4,10):
    print(i)
    id = df['Id'][i]
    orientation = df['Orientation'][i]
    date = df['Date'][i]
    heure = str(df['Heure'][i])
    neige = df['Qualite neige'][i]
    lat = df['latitude'][i]
    lon = df['longitude'][i]

    [day, month, year] = normaliseDate(date)

    heure = normaliseHeure(heure)

    print(heure)
    print(day)
    print(month)
    print(year)
    print(lon)
    print(lat)



    c.retrieve(
    'reanalysis-era5-single-levels',
    {
        'product_type':'reanalysis',
        'lat':lat,
        'lon':lon,
        'format':'netcdf',
        'variable':[
            '2m_temperature',
            'clear_sky_direct_solar_radiation_at_surface',
            'large_scale_precipitation',
            'large_scale_snowfall',
            'snow_density',
            'snow_depth',
            'snowmelt'
        ],
        'year':year,
        'month':month,
        'day':day,
        'time':heure
    },
    '../download/download'+str(i)+'.nc')
