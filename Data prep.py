## Prep, join and create metrics to model

# Libraries
import os
import pandas as pd
import numpy as np
from datetime import datetime

# Set working directory
os.chdir("---Your working directory path")
print(os.getcwd())

# Import the categorized CCS data
CCdata = pd.read_csv("--path to categorized credit card transactions data",header=0, index_col=False)
print(CCdata.shape)

# Import weather data
## Importing from:  https://climate.weather.gc.ca/climate_data/daily_data_e.html
weather2019 = pd.read_csv("en_climate_daily__2019_P1D.csv",header=0)
print(weather2019.shape)

weather2020 = pd.read_csv("en_climate_daily__2020_P1D.csv",header=0)
print(weather2020.shape)

weather2021 = pd.read_csv("en_climate_daily__2021_P1D.csv",header=0)
print(weather2021.shape)

# Combine the individual years' weather data into a single df
weatherData = weather2019.append([weather2020,weather2021],ignore_index=True)
print(weatherData.shape)

# Examining the columns in the weather data
print(weatherData.head(20))
print(weatherData.columns)
print(weatherData.dtypes)
## Wow! the data is mostly clean :-)

# Set the date column in weather data as a datetime object and then as index of df
weatherData['Date'] = pd.to_datetime(weatherData['Date/Time'], format="%Y-%m-%d")
print(weatherData.dtypes)

weatherData = weatherData.set_index('Date')
weatherData.head(5)

weatherData = weatherData.rename({'Max Temp (°C)':'Max Temp', 
                                  'Min Temp (°C)':'Min Temp',
                                  'Mean Temp (°C)':'Mean Temp',
                                 'Heat Deg Days (°C)':'Heat Deg Days',
                                 'Cool Deg Days (°C)':'Cool Deg Days',
                                 'Total Precip (mm)':'Total Precip',
                                  'Total Rain (mm)':'Total Rain',
                                  'Total Snow (cm)':'Total Snow',
                                  'Snow on Grnd (cm)':'Snow Grnd',
                                  'Spd of Max Gust (km/h)':'Max Gust'}, axis=1)

weatherData['Temp Diff'] = weatherData['Max Temp'] - weatherData['Min Temp']

statCols = ['Total Precip','Total Rain','Total Snow','Snow Grnd',
            'Max Gust','Max Temp','Min Temp','Temp Diff','Mean Temp']
print(weatherData[statCols].describe())

## Clean the date column in the CC data and set it to datetime format
print(CCdata['Transaction Date'].dtype)
print(CCdata.loc[0:1,'Transaction Date'])
print(CCdata['Year'].dtype)
print(CCdata.loc[0:1,'Year'])

# Create a date column in CCdata by combining date,month and year
# Separate day and month
CCdata['Day'] = CCdata['Transaction Date'].str.extract('([0-9]+)',expand=False)
print(CCdata['Day'].head(10))
CCdata['Month'] = CCdata['Transaction Date'].str.extract('([A-Za-z]+)',expand=False)
print(CCdata['Month'].head(10))

# Combine day,month and year to form the date column
cols = ['Day','Month','Year']
CCdata['Date'] = CCdata[cols].astype(str).apply('-'.join, axis=1)
print(CCdata['Date'].head(10))

# Setting the date column to type datatime64 and as index of the df
CCdata['Date'] = pd.to_datetime(CCdata['Date'], format="%d-%b-%Y")
print(CCdata.dtypes)
CCdata = CCdata.set_index('Date')
CCdata.head(5)

# Joining weather data with the CC data based on date
requiredCols = ['Total Precip','Total Rain','Total Snow','Snow Grnd',
            'Max Gust','Max Temp','Min Temp','Temp Diff','Mean Temp']
requiredWeatherData = weatherData[requiredCols]
print(requiredWeatherData.columns)

CCdata_merged = CCdata.join(requiredWeatherData, how='left')  
##pd.merge doesn't work here bcoz date is not an explicit column here, its the index of these 2 dataframes
print(CCdata_merged.shape)
print(CCdata_merged.head(20))

# Note that the temperature, precipitation and gust speed data is missing on some days. 
# These days have to be filtered out before fitting a model

# Wrangle data and add the following columns:
#    a. Number of days since last grocery shopping trip
#    b. The amount of last grocery shopping
#    c. Number of days since you last ordered from a restaurant
#    d. The amount of last restaurant order (>=$20, to keep put petty orders and coffees)
