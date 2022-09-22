# Grocery trip prediction
Based on credit card transactions, store directory(sourced from the web), weather and other data, predict the date of your next grocery shopping trip

Kernel: Python3

Logs: Absent

License: MIT

Purpose: Reading credit card statements from a particular bank, that are in PDF format and analysing transactions to present spending pattern.

Python libraries used: os, pandas, numpy, datetime, matplotlib, seaborn, sklearn, statsmodels

Data used for prediction:
Weather in the region of residence
Recent restaurant spend
Last grocery trip spend

Files: 
Prep.py - Create a dataset for modelling by merging weather data with credit card transactions data (CC data)

Wrangle.py - Create columns for previous grocery and restaurant spend data in CC data

EDA.py - EDA to determine the most influential parameters, outlier and null value correction and add metrics if necessary

modelfit.py - fitting a prediction model - linear regression, SVM, random forest, lightGBM
