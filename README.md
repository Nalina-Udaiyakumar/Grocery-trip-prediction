# Grocery-trip-prediction
Based on credit card transactions, store directory(sourced from the web), weather and other data, predict the date of your next grocery shopping trip


Other data used for prediction:
Weather in the region of residence
Recent restaurant spend
Last grocery trip spend


Files: 
Dataprep.py - Create a dataset for modelling by merging weather data with credit card transactions data (CC data)
Datawrangle.py - Create columns for previous grocery and restaurant spend data in CC data
EDA and prep.py - EDA to determine the most influential parameters, data prep and add metrics if necessary
Grocery prediction.py - fitting a prediction model and tune
