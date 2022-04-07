## from the EDA and KDE plots, we can fit linear regression model and SVR onto data

#libraries
import statsmodels.api as sm


# Splitting train and test data - 80%-20% split
traindata = CCdata_merged_GR.loc[CCdata_merged_GR['Grocery Flag']==1,]
traindata = traindata[['Grocery Amount', 'MaxGust',
                                 'MeanTemp',
                                 'GroceryDiff']]  ## choosing only the 3 factors that have higher correlation

sample80 = np.random.rand(len(traindata)) <= 0.8 
testdata = traindata[~sample80]
traindata = traindata[sample80]

print(f"No. of training examples: {traindata.shape[0]}")
print(f"No. of testing examples: {testdata.shape[0]}")

print("The percentage of null values in each column: \n",traindata.isnull().mean()*100)

## Fitting linear regression model with regressors
y = traindata['Grocery Amount']
X = traindata[['MaxGust', 'MeanTemp', 'GroceryDiff']]

model = sm.OLS(y, X)
results = model.fit()
print(results.summary())  ## gives all details of the model, required to evaluate and compare models
print('coefficient of determination:', results.rsquared)
print('adjusted coefficient of determination:', results.rsquared_adj)
print('regression coefficients:', results.params)


## fitting SVR model to compare wiht OLS model
regressor = SVR(kernel='rbf') # choosing rbf/gaussian kernel coz the relationship of regressors is not linear
regressor.fit(X,y)

#print the predicted values
svm_pred = regressor.predict(testdata[['MaxGust', 'MeanTemp', 'GroceryDiff']])
print(svm_pred)
