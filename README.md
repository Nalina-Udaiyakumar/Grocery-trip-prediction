# Grocery-trip-prediction
Based on cresit card transactions and other data, predict the date of your next grocery shopping trip


Other data used for prediction:
Weather in the region of residence
Recent restaurant spend
Last grocery trip spend


Files: 
Dataprep.py - Create a dataset for modelling by merging weather data with credit card transactions data (CC data)
Datawrangle.py - Create columns for previous grocery and restaurant spend data in CC data
CC_EDA.py - EDA to determine the most influential parameters and add metrics if necessary
Grocery prediction.py - fitting a prediction model and tune
