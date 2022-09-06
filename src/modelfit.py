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

sample80 = int(len(traindata)*0.8)
testdata = df[sample80:]
traindata = df[:sample80]

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
# We can see that the OLS model doesn't predict the pattern very well. We could refit the OLS model on box-cox transformed training data

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


### Trying Box-cox transformation to make feature data distribution more normal
# Studying regressors before and after Box-cox transformation:
# Filter columns that are to be regressed
featureData = CCdata_merged_GR[['TotalPrecip', 'MaxGust',
                                 'TempDiff','MeanTemp',
                                 'GroceryDiff','RestaurantDiff',
                                 'PrevGroceryAmount','PrevRestaurantAmount']]
# skewness and kurtosis of features
print("Features: ",featureData.columns)
print("Skewness of features: ", stats.skew(featureData, bias=False))
print("Kurtosis of features: ", stats.kurtosis(featureData, bias=False))

# let's get feature data description
print(featureData.describe())

featureDataBxcx = featureData.copy()
print(featureDataBxcx.head(5))
## adding constants to columns that have 0 and -ve values
featureDataBxcx['TotalPrecip'] = featureDataBxcx['TotalPrecip'] + 0.01
featureDataBxcx['GroceryDiff'] = featureDataBxcx['GroceryDiff'] + 0.01
featureDataBxcx['RestaurantDiff'] = featureDataBxcx['RestaurantDiff'] + 0.01
featureDataBxcx['PrevGroceryAmount'] = featureDataBxcx['PrevGroceryAmount'] + 0.01
featureDataBxcx['PrevRestaurantAmount'] = featureDataBxcx['PrevRestaurantAmount'] + 0.01
featureDataBxcx['MeanTemp'] = featureDataBxcx['MeanTemp'] + 13.1
print(featureDataBxcx.head(5))

bestLambda = []   ## we need the lambda values for getting inverse box-cox transforms after fitting model
for col in featureDataBxcx.columns:
    boxcoxFeatures = featureDataBxcx[col]
    boxcoxFeatures, Lambda_iter = stats.boxcox(boxcoxFeatures)
    bestLambda.append(Lambda_iter)

# Get distribution plots of all the above columns in a multi-grid plot
f, axes = plt.subplots(4, 2, figsize=(7, 7))

sns.kdeplot(x=featureDataBxcx["TotalPrecip"], color="skyblue", ax=axes[0, 0])
sns.kdeplot(x=featureDataBxcx["MaxGust"], color="olive", ax=axes[0, 1])
sns.kdeplot(x=featureDataBxcx["TempDiff"], color="gold", ax=axes[1, 0])
sns.kdeplot(x=featureDataBxcx["MeanTemp"], color="teal", ax=axes[1, 1])
sns.kdeplot(x=featureDataBxcx["GroceryDiff"], color="skyblue", ax=axes[2, 0])
sns.kdeplot(x=featureDataBxcx["RestaurantDiff"], color="olive", ax=axes[2, 1])
sns.kdeplot(x=featureDataBxcx["PrevGroceryAmount"], color="gold", ax=axes[3, 0])
sns.kdeplot(x=featureDataBxcx["PrevRestaurantAmount"], color="teal", ax=axes[3, 1])
plt.suptitle('KDE of features after box-cox transformation')
plt.show()
plt.savefig('KDE of features_Box cox transformed.png')
    
## Fit decision tree model
from sklearn.tree import DecisionTreeRegressor
from sklearn.tree import export_text
from sklearn.metrics import mean_squared_error, r2_score

y = traindata['Grocery Amount']
X = traindata[['TotalPrecip', 'MaxGust',
                   'TempDiff','MeanTemp', 
                   'GroceryDiff','RestaurantDiff',
                   'PrevGroceryAmount','PrevRestaurantAmount']]

# Train the model
DTmodel = DecisionTreeRegressor().fit(X, y)
print (DTmodel, "\n")

# Visualize the model tree
decisionTree = export_text(DTmodel)
print(decisionTree)

X_test = testdata[['TotalPrecip', 'MaxGust',
                   'TempDiff','MeanTemp', 
                   'GroceryDiff','RestaurantDiff',
                   'PrevGroceryAmount','PrevRestaurantAmount']]
y_test = testdata['Grocery Amount']
# Evaluate the model using the test data
predictions = DTmodel.predict(X_test)
mse = mean_squared_error(y_test, predictions)
print("MSE:", mse)
rmse = np.sqrt(mse)
print("RMSE:", rmse)
r2 = r2_score(y_test, predictions)
print("R2:", r2)

# Plot predicted vs actual
testdata['PredictedDT'] = predictions
sns.lineplot(x='Date',y='Grocery Amount',data=testdata, color='darkgrey')
sns.lineplot(x='Date',y='PredictedDT', data=testdata, color='red')
plt.title('Actual vs predicted values - Decision tree')
plt.legend(labels=['Actual','Predicted'])
plt.savefig("Actual vs predicted values - Decision tree.png")


## Fit random forest model
from sklearn.ensemble import RandomForestRegressor

# Train the model
model = RandomForestRegressor().fit(X, y)
print (model, "\n")

# Evaluate the model using the test data
predictions = model.predict(X_test)
mse = mean_squared_error(y_test, predictions)
print("MSE:", mse)
rmse = np.sqrt(mse)
print("RMSE:", rmse)
r2 = r2_score(y_test, predictions)
print("R2:", r2)

# Plot predicted vs actual
testdata['PredictedRF'] = predictions
sns.lineplot(x='Date',y='Grocery Amount',data=testdata, color='darkgrey')
sns.lineplot(x='Date',y='PredictedRF', data=testdata, color='red')
plt.title('Actual vs predicted values - Random forest regressor')
plt.legend(labels=['Actual','Predicted'])
plt.savefig("Actual vs predicted values - Random forest regressor.png")

## Fit Light GBM model
import lightgbm as lgb

params = {
    'task': 'train', 
    'boosting': 'gbdt',
    'objective': 'regression',
    'num_leaves': 10,
    'learnnig_rage': 0.05,
    'metric': {'l2','l1'},
    'verbose': -1
}
 
# loading data
lgb_train = lgb.Dataset(X, y)
lgb_eval = lgb.Dataset(X_test, y_test, reference=lgb_train)

# fitting the model
model = lgb.train(params,
                 train_set=lgb_train,
                 valid_sets=lgb_eval,
                 early_stopping_rounds=30)

# predictions using the model
y_pred = model.predict(X_test)

# model evaluation metrics
mse = mean_squared_error(y_test, y_pred)
rmse = mse**(0.5)
print("MSE: %.2f" % mse)
print("RMSE: %.2f" % rmse)

testdata['PredictedLGBM'] = predictions
sns.lineplot(x='Date',y='Grocery Amount',data=testdata, color='darkgrey')
sns.lineplot(x='Date',y='PredictedLGBM', data=testdata, color='red')
plt.title('Actual vs predicted values - Light GBM')
plt.legend(labels=['Actual','Predicted'])
plt.savefig("Actual vs predicted values - Light GBM.png")
