# Grocery trip prediction

## Overview

Based on credit card transactions, store directory(sourced from the web), weather and other data, predict the date of your next grocery shopping trip

<h6>Kernel:</h6> Python3 and R

<h6>Logs:</h6> Absent

<h6>License:</h6> MIT

<h6>Purpose:</h6> Reading credit card statements from a particular bank, that are in PDF format and wrangling transactions data to analyze spending pattern and make predictions for future spends - particularly for grocery shopping.

<h6>Python libraries used:</h6> os, pandas, numpy, datetime, matplotlib, seaborn, sklearn, statsmodels

<h6>Data used for prediction:</h6>
- Weather in the region of residence
- Recent restaurant spend
- Last grocery trip spend

<h6>Files:</h6>
* *Prep.py* - Create a dataset for modeling by merging weather data with credit card transactions data (CC data)
* *Wrangle.py* - Create columns for previous grocery and restaurant spend data in CC data
* *EDA.py* - EDA to determine the most influential parameters, outlier and null value correction and add metrics if necessary
* *modelfit.py* - fitting a prediction model - linear regression, SVM, random forest, lightGBM

## Motivation and problem statement

Managing finances is one of the crucial steps in Adulting. I wanted to work out a solution for understanding my spending and finances in a way that made sense to me and wanted to have a scalable, time-saving option that would work every month, on each one of my statements, giving me a precise picture of my financials.
While I was at it, I wanted to make an educated guess at what triggers me to spend 'x' dollars at a store 'y'. I wanted to build a machine learning model that would learn from my spend pattern and predict when I am likely to go shopping and how much I might spend. The best part about the project is **it could be used by any person that has a bank account with the same bank!**

## The nitty-gritties

* 1. ##### Reading and cleaning transaction data
To get started, we need to read credit card transaction data from monthly PDF statements(my bank and most other banks don't provide an Excel version of statements). R packages pdftools and stringr are used for reading and cleaning the credit card transaction data. To get the required data, we need to find patterns in the parsed text corpse that indicates a new transaction entry and separate detils like date, point of sale, amount from that entry. Code [here] (https://github.com/Nalina-Udaiyakumar/statementDecipher/blob/main/src/Read_statement_CC.R)
 
* 2. ##### Categorizing transactions
My monthly statements do not contain a pre-marked category for the transaction. But profiling spend data require categories for transactions to work with. So we scrape list of all grocery stores, restaurant chains, gas stations and other multi-department chain of stores from the web to create a store directory. The user can also add stores and categories in a custom csv file that is appended to the store directory. Code [here] (https://github.com/Nalina-Udaiyakumar/statementDecipher/blob/main/src/Get_Store_Names.R)

* 3. ##### Matching categories to transactions
After creating a store directory, we have to match the category/store name to each transaction correctly. For this I used a vectorized pattern matching function - vectorized grep in R and str.contains in python pandas. For my data structure and values, the R grep worked way better than the python str.contins. R could match categories for more than 80% of my transaction data. Code: R version [here] (https://github.com/Nalina-Udaiyakumar/statementDecipher/blob/main/src/Match_Store_Names.R) and Python version [here] (https://github.com/Nalina-Udaiyakumar/Grocery-trip-prediction/blob/main/notebooks/1%20CC%20store%20categorize_Py.ipynb)

* 4. ##### Exploratory data analysis
From what we curated so far, we can do some exploratory analysis to find general spend pattern, monthly spending on each category adn most visited stores, etc. We can also find the distribution of data to assess the kind of models that could be a better fit for the data. Plots of data can also help us understand out data and refine/change our problem statement. This process is very crucial to obtain meaningful insights from the exercise.
Code R version [here] (https://github.com/Nalina-Udaiyakumar/statementDecipher/blob/main/src/Charts_and_reports.R) and Python version [here] (https://github.com/Nalina-Udaiyakumar/Grocery-trip-prediction/blob/main/src/EDA.py)

* 5. ##### Add weather data for each transaction
I wanted to analyse if my decision to go out of the house for an evening and spend money is dependent on weather or not and how does weather impact my spending pattern. So I downloaded the weather data for my place of residence (and spending) from Daily weather report, [Canada] (https://climate.weather.gc.ca) and joined wind, temperature and precipitation data to each transaction by date.
Code [here] (https://github.com/Nalina-Udaiyakumar/Grocery-trip-prediction/blob/main/src/Prep.py)

* 6. ##### Wrangle data - add new columns and create metrics as needed 
Further cleaned the joined data, added columns and metrics to fit models. Some of the columns added were - weekday, month and year of transaction, days since last grocery trip, last grocery trip spend, days since last resturant trip, last restaurant spend, categorical columns for windy/snowy/rainy weather based on temp and precipitation values.
Code [here] (https://github.com/Nalina-Udaiyakumar/Grocery-trip-prediction/blob/main/src/Wrangle.py)

* 7. ##### Fit and tune machine learning models and plots
Treat data for missing values and outliers and proceed to fit models - Linear regression, SVM, random forest and light GBM. Evaluate each of these models and compare results.
Code [here] (https://github.com/Nalina-Udaiyakumar/Grocery-trip-prediction/blob/main/notebooks/2%20Link%20weather%20data%20and%20models.ipynb) and plots [here] (https://github.com/Nalina-Udaiyakumar/Grocery-trip-prediction/tree/main/Plots)
