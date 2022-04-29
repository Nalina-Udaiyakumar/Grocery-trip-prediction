## from the EDA and KDE plots, we can fit linear regression model and SVR onto data

#libraries
import statsmodels.api as sm
from sklearn.svm import SVR
from sklearn import metrics
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

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
print('adjusted coefficient of determination:', results.rsquared_adj) # adjusted R2 for this model is around 57%(varies with training sample)
print('regression coefficients:', results.params)
#plotting predictions
test_pred = results.predict(testdata[['MaxGust', 'MeanTemp', 'GroceryDiff']])
testdata['PredictedOLS'] = test_pred
sns.lineplot(x='Date',y='Actual',data=testdata, color='darkgrey')
sns.lineplot(x='Date',y='PredictedOLS', data=testdata, color='red')
plt.title('Actual vs predicted values - OLS regression')
plt.legend(labels=['Actual','Predicted'])
plt.savefig("Actual vs predicted values - OLS regression.png")


## fitting SVR model to compare wiht OLS model
regressor = SVR(kernel='rbf') # choosing rbf/gaussian kernel coz the relationship of regressors is not linear
regressor.fit(X,y)

#print the predicted values
testdata['PredictedSVM'] = regressor.predict(testdata[['MaxGust', 'MeanTemp', 'GroceryDiff']])
sns.lineplot(x='Date',y='Actual',data=testdata, color='darkgrey')
sns.lineplot(x='Date',y='PredictedOLS', data=testdata, color='red')
plt.title('Actual vs predicted values - SVM')
plt.legend(labels=['Actual','Predicted'])
plt.savefig("Actual vs predicted values - SVM.png")
# SVR model is better than the OLS regression model
