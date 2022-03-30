## EDA plots and bivariate analyses on CCdata_merged
print(CCdata_merged.shape)
print(CCdata_merged.columns)

# filter restaurnt and grocery data
CCdata_merged_GR = CCdata_merged[(CCdata_merged['Grocery Flag']==1) | (CCdata_merged['Restaurant Flag']==1)]
CCdata_merged_GR = CCdata_merged_GR[CCdata_merged_GR['Amount']>=0]
print(CCdata_merged_GR.shape)
print(CCdata_merged_GR.columns)

# Adding columns for number of days from the previous grocery and restaurant trips
CCdata_merged_GR = CCdata_merged_GR.reset_index()
print(CCdata_merged_GR['Date'].dtype)
CCdata_merged_GR['GroceryDiff'] = CCdata_merged_GR['Date'] - CCdata_merged_GR['PrevGroceryDate']
# the difference obtained is in seconds. Converting it to number of days between Date and PrevGroceryDate
CCdata_merged_GR['GroceryDiff'] = (CCdata_merged_GR['GroceryDiff']/np.timedelta64(1,'D')).astype(int)
CCdata_merged_GR['RestaurantDiff'] = CCdata_merged_GR['Date'] - CCdata_merged_GR['PrevRestaurantDate']
CCdata_merged_GR['RestaurantDiff'] = (CCdata_merged_GR['RestaurantDiff']/np.timedelta64(1,'D')).astype(int)
print(np.sort(CCdata_merged_GR['GroceryDiff'].unique()))
print(np.sort(CCdata_merged_GR['RestaurantDiff'].unique()))

# CCdata_merged_GR.to_csv("CCdata_merged.csv",header=True,index=True)

# prevGroceryAmount and PrevGroceryFlag avg vs GroceryDiff
graphData = CCdata_merged_GR.groupby('GroceryDiff', as_index=False).agg({'PrevGroceryAmount':'mean',
                                                                        'PrevGroceryFlag':'sum'})
sns.relplot(x="GroceryDiff", y="PrevGroceryAmount",color = "green", data=graphData)
sns.relplot(x="GroceryDiff", y="PrevGroceryFlag",color = "red", data=graphData)

#PrevRestaurantAmount and PrevRestaurantFlag avg vs RestaurantDiff
graphData = CCdata_merged_GR.groupby('RestaurantDiff', as_index=False).agg({'PrevRestaurantAmount':'mean',
                                                                        'PrevRestaurantFlag':'sum'})
sns.relplot(x="RestaurantDiff", y="PrevRestaurantAmount",color = "darkblue", data=graphData)
sns.relplot(x="RestaurantDiff", y="PrevRestaurantFlag",color = "red", data=graphData)

# General grocery and restaurant spending pattern
CCdata_merged_GR['Grocery Amount'] = CCdata_merged_GR['Amount'] * CCdata_merged_GR['Grocery Flag']
CCdata_merged_GR['Restaurant Amount'] = CCdata_merged_GR['Amount'] * CCdata_merged_GR['Restaurant Flag']

graphData = CCdata_merged_GR.groupby('Weekday', as_index=False).agg({'Grocery Amount':'mean',
                                                                    'Restaurant Amount':'mean',
                                                                    'Grocery Flag':'mean',
                                                                    'Restaurant Flag':'mean'})
## redefining Weekday column as a categorical variable with ordered levels, to order the points on the graph
graphData.Weekday = pd.Categorical(graphData.Weekday,
                            categories=['Monday', 'Tuesday', 'Wednesday',
                                        'Thursday', 'Friday', 'Saturday', 'Sunday'],
                            ordered=True)

graphData = graphData.sort_values('Weekday')
print(graphData)

plt.rcParams["figure.figsize"] = [11.00, 6.00]
plt.rcParams["figure.autolayout"] = True

# Weekday vs avg grocery and restaurant spend
f, axes = plt.subplots(1, 2)
sns.scatterplot(x="Weekday", y="Grocery Amount", color = "green", data=graphData, ax=axes[0])
sns.scatterplot(x="Weekday", y="Restaurant Amount", color = "maroon", data=graphData, ax=axes[1])
plt.show()

# weekday vs avg groceruy and restaurant trips
f, axes = plt.subplots(1, 2)
sns.scatterplot(x="Weekday", y="Grocery Flag", color = "green", data=graphData, ax=axes[0])
sns.scatterplot(x="Weekday", y="Restaurant Flag", color = "maroon", data=graphData, ax=axes[1])
plt.show()

# Monthly spending pattern
graphData = CCdata_merged_GR.groupby(['Month','Year'], as_index=False).agg({'Grocery Amount':'sum',
                                                                        'Restaurant Amount':'sum',
                                                                            'PrevGroceryAmount':'sum',
                                                                        'PrevRestaurantAmount':'sum'})
graphData['Month'] = pd.Categorical(graphData.Month,
                            categories=['Jan', 'Feb', 'Mar','Apr','May','Jun',
                                        'Jul','Aug','Sep','Oct','Nov','Dec'],
                            ordered=True)
graphData = graphData.sort_values('Month')

plt.rcParams["figure.figsize"] = [14.00, 7.00]
plt.rcParams["figure.autolayout"] = True

# Month vs avg grocery and restaurant spend
f, axes = plt.subplots(1, 2)
sns.lineplot(x="Month", y="Grocery Amount", hue="Year", data=graphData, ax=axes[0], palette=["k", "r"])
sns.lineplot(x="Month", y="Restaurant Amount", hue="Year", data=graphData, ax=axes[1], palette=["k", "r"])
plt.show()

# Month vs avg prev grocery and prev restaurant spend
f, axes = plt.subplots(1, 2)
sns.lineplot(x="Month", y="PrevGroceryAmount", hue="Year", data=graphData, ax=axes[0], palette=["C0", "C1"])
sns.lineplot(x="Month", y="PrevRestaurantAmount", hue="Year", data=graphData, ax=axes[1], palette=["C0", "C1"])
plt.show()

graphData = CCdata_merged_GR[['GroceryDiff','Grocery Amount','PrevGroceryAmount']].groupby('GroceryDiff', as_index=False).mean()
print(graphData)

sns.lineplot(x="GroceryDiff", y="Grocery Amount", data=graphData)
sns.lineplot(x="GroceryDiff", y="PrevGroceryAmount", data=graphData)
plt.legend(labels=["Grocery Amount","PrevGroceryAmount"])

# Column description, null and outlier correction
print("The percentage of null values in each column: \n",CCdata_merged_GR.isnull().mean()*100)

print("Column decriptions: \n",featureData.describe())
featureData = featureData.quantile([0.05,0.10,0.80,0.90,0.95,0.97,0.98,0.99])
print("Percentile values of columns: \n",quantileData)

# Scatter plots of all variables that are to be regressed
print(CCdata_merged_GR.columns)
# Filter columns that are to be regressed
featureData = CCdata_merged_GR[['Total Precip', 'Max Gust',
                                 'Temp Diff','Mean Temp',
                                 'GroceryDiff','RestaurantDiff',
                                 'PrevGroceryAmount','PrevRestaurantAmount']]

# Get distribution plots of all the above columns in a multi-grid plot
f, axes = plt.subplots(4, 2, figsize=(7, 7))

sns.kdeplot(x=featureData["Total Precip"], color="skyblue", ax=axes[0, 0])
sns.kdeplot(x=featureData["Max Gust"], color="olive", ax=axes[0, 1])
sns.kdeplot(x=featureData["Temp Diff"], color="gold", ax=axes[1, 0])
sns.kdeplot(x=featureData["Mean Temp"], color="teal", ax=axes[1, 1])
sns.kdeplot(x=featureData["GroceryDiff"], color="skyblue", ax=axes[2, 0])
sns.kdeplot(x=featureData["RestaurantDiff"], color="olive", ax=axes[2, 1])
sns.kdeplot(x=featureData["PrevGroceryAmount"], color="gold", ax=axes[3, 0])
sns.kdeplot(x=featureData["PrevRestaurantAmount"], color="teal", ax=axes[3, 1])

plt.show()

# Observations from the density plots: Total Precip, GroceryDiff, RestaurantDiff and PrevGroceryAmount are all heavily right skewed
# Solution: Looking at the percentile values of these columns, we can remove observations corresponding to >95%ile in these columns
# Removing the last 5%ile of values of these columns
CCdata_merged_GR[['OF1','OF2','OF3','OF4']] = 0
CCdata_merged_GR.loc[CCdata_merged_GR['Total Precip'] > CCdata_merged_GR['Total Precip'].quantile(.95),'OF1'] = 1
CCdata_merged_GR.loc[CCdata_merged_GR['GroceryDiff'] > CCdata_merged_GR['GroceryDiff'].quantile(.95),'OF2'] = 1
CCdata_merged_GR.loc[CCdata_merged_GR['RestaurantDiff'] > CCdata_merged_GR['RestaurantDiff'].quantile(.95),'OF3'] = 1
CCdata_merged_GR.loc[CCdata_merged_GR['PrevGroceryAmount'] > CCdata_merged_GR['PrevGroceryAmount'].quantile(.95),'OF4'] = 1
print(CCdata_merged_GR['OF1'].sum())
print(CCdata_merged_GR['OF2'].sum())
print(CCdata_merged_GR['OF3'].sum())
print(CCdata_merged_GR['OF4'].sum())
# CCdata_merged_GR['OF'] = CCdata_merged_GR['OF1']+CCdata_merged_GR['OF2']+CCdata_merged_GR['OF3']+CCdata_merged_GR['OF4']
CCdata_merged_GR['OF'] = CCdata_merged_GR[['OF1','OF2','OF3','OF4']].sum(axis=1)
print(CCdata_merged_GR['OF'].sum())
print(CCdata_merged_GR.loc[CCdata_merged_GR['OF']>0,"OF"].count())

# Filter out outliers from CCdata_merged_GR
print(CCdata_merged_GR.shape)
CCdata_merged_GR = CCdata_merged_GR[CCdata_merged_GR['OF']==0]
print(CCdata_merged_GR.shape)

## Plotting KDE of the regression variables after outlier correction
featureData = CCdata_merged_GR[['Total Precip', 'Max Gust',
                                 'Temp Diff','Mean Temp',
                                 'GroceryDiff','RestaurantDiff',
                                 'PrevGroceryAmount','PrevRestaurantAmount']]

# Get distribution plots of all the above columns in a multi-grid plot
f, axes = plt.subplots(4, 2, figsize=(7, 7))

sns.kdeplot(x=featureData["Total Precip"], color="skyblue", ax=axes[0, 0])
sns.kdeplot(x=featureData["Max Gust"], color="olive", ax=axes[0, 1])
sns.kdeplot(x=featureData["Temp Diff"], color="gold", ax=axes[1, 0])
sns.kdeplot(x=featureData["Mean Temp"], color="teal", ax=axes[1, 1])
sns.kdeplot(x=featureData["GroceryDiff"], color="skyblue", ax=axes[2, 0])
sns.kdeplot(x=featureData["RestaurantDiff"], color="olive", ax=axes[2, 1])
sns.kdeplot(x=featureData["PrevGroceryAmount"], color="gold", ax=axes[3, 0])
sns.kdeplot(x=featureData["PrevRestaurantAmount"], color="teal", ax=axes[3, 1])

plt.show()
## now valuesof each column are less skewed
