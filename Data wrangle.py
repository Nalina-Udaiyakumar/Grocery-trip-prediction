## Wrangle CCdata_merged and add previous grocery trip, spend and previous restaurant trip, spend or each transaction

# Change amount to float datatype and remove , if any, in the amount value
print(CCdata['Amount'].dtype)
CCdata['Amount'] = CCdata['Amount'].str.replace('\,','') # removing all , in the amount values
CCdata['Amount'] = pd.to_numeric(CCdata['Amount'])

#a. Number of days since last grocery shopping trip and b. The amount of last grocery shopping
# filter rows with category groceries, shopping walmart and store walmart
# extract the date and amount as series from the above  filtered df 
# offset the value by 1 row join with the CC merged data to get the previous grocery trip date and amount
groceryData = CCdata.loc[CCdata['Category'].isin(["Groceries","Shopping-Walmart"])]
# groceryData = groceryData.drop(['Transaction Date','Posting Date','Description','Category'],axis=1)
# Treating duplicates - it's possible to go to multiple grocery stores in a day
print(groceryData.shape)
print(len(pd.unique(groceryData.index)))  # Unique dates in groceryData < no. of rows in groceryData
# Groupby date to create unique values of date and grocery spend - for each date, find sum of grocery spend.
groceryData = groceryData.groupby(['Date']).Amount.sum().reset_index()
# Create month, year and day columns in groceryData and set Date as index
groceryData['Month'] = groceryData['Date'].dt.strftime("%b")
groceryData['Year'] = groceryData['Date'].dt.year.astype(int)
groceryData['Day'] = groceryData['Date'].dt.day.astype(int)
groceryData = groceryData.set_index('Date')

print(groceryData.shape)
print(groceryData.dtypes)
print(groceryData.head(10))


# Creating the columns for last grocery trip date and amount
grocery_temp = pd.DataFrame()
grocery_temp['Date'] = pd.date_range(start=CCdata.index.min(), end=CCdata.index.max(), freq='D')
grocery_temp = grocery_temp.set_index('Date')
print(grocery_temp.head(10))
grocery_temp = grocery_temp.join(groceryData, how='left')
print(grocery_temp.shape)
print(grocery_temp.head(10))

grocery_temp = grocery_temp.shift(1)
grocery_temp = grocery_temp.ffill()
print(grocery_temp.head(10))

#Combine day, month and year to get the last grocery trip date
grocery_temp = grocery_temp.reset_index()
print(grocery_temp.shape)
grocery_temp['Year'] = grocery_temp['Year'].fillna(grocery_temp['Date'].dt.year).astype(int)
# grocery_temp['Month'] = grocery_temp['Month'].fillna(grocery_temp['Date'].dt.month)  
# dt.month doesn't work coz it gives the month number ex.2, not the month name
grocery_temp['Month'] = grocery_temp['Month'].fillna(grocery_temp['Date'].dt.strftime("%b"))
grocery_temp['Day'] = grocery_temp['Day'].fillna(grocery_temp['Date'].dt.day).astype(int)
grocery_temp['Amount'] = grocery_temp['Amount'].fillna(0.0)

grocery_temp = grocery_temp.rename({'Amount':'PrevGroceryAmount'}, axis=1)

grocery_temp = grocery_temp.set_index('Date')
print(grocery_temp.head(10))                                                       
cols = ['Day','Month','Year']
grocery_temp['PrevGroceryDate'] = grocery_temp[cols].astype(str).apply('-'.join, axis=1)
grocery_temp['PrevGroceryDate'] = pd.to_datetime(grocery_temp['PrevGroceryDate'], format="%d-%b-%Y")
print(grocery_temp.dtypes)
print(grocery_temp.head(10))

## Join prev grocery amount and prev grocery date onto CC data_merged
grocery_temp = grocery_temp.drop(['Month','Year','Day'],axis=1)
print(CCdata_merged.shape)
print(CCdata_merged.head(5))
print(grocery_temp.shape)
print(grocery_temp.head(5))

CCdata_merged = CCdata_merged.join(grocery_temp, how='left')
# dropping duplicates in CCdata_merged
CCdata_merged.drop_duplicates(subset=None,keep='first',inplace=True)

print(CCdata_merged.shape)
print(CCdata_merged.columns)
print(CCdata_merged['PrevGroceryAmount'].count())
print(CCdata_merged['PrevGroceryDate'].count())

# getting value counts of year, month and date
print(CCdata_merged.groupby('Year')['Month'].value_counts())
print(CCdata_merged['Day'].value_counts().sort_index(ascending=True))

## c. Number of days since you last ordered from a restaurant and d. The amount of last restaurant order 
# Filter rows of restaurant transactions 
restaurantData = CCdata.loc[CCdata['Category'].isin(["Restaurant","Food - Take out"])]
restaurantData = restaurantData.drop(['Transaction Date','Posting Date','Description','Category'],axis=1)
print(restaurantData.shape)
print(restaurantData.head(10))
print(len(pd.unique(restaurantData.index))) ## If unique length of index < no. of rows of restaurantData, groupby date and sum of restaurant spend
# Unique dates in restaurantData < no. of rows in restaurantData
# Groupby date to create unique values of date and restaurant spend - for each date, find sum of restaurant spend.
restaurantData = restaurantData.groupby(['Date']).Amount.sum().reset_index()
# Create month, year and day columns in restaurantData and set Date as index
restaurantData['Month'] = restaurantData['Date'].dt.strftime("%b")
restaurantData['Year'] = restaurantData['Date'].dt.year.astype(int)
restaurantData['Day'] = restaurantData['Date'].dt.day.astype(int)
restaurantData = restaurantData.set_index('Date')
print(restaurantData.shape)

# Creating the columns for last restaurant trip date and amount
restaurant_temp = pd.DataFrame()
restaurant_temp['Date'] = pd.date_range(start=CCdata.index.min(), end=CCdata.index.max(), freq='D')
restaurant_temp = restaurant_temp.set_index('Date')
print(restaurant_temp.head(10))
restaurant_temp = restaurant_temp.join(restaurantData, how='left')
print(restaurant_temp.shape)
print(restaurant_temp.head(10))

restaurant_temp = restaurant_temp.shift(1)
restaurant_temp = restaurant_temp.ffill()
print(restaurant_temp.head(10))

#Combine day, month and year to get the last restaurant trip date
restaurant_temp = restaurant_temp.reset_index()
print(restaurant_temp.shape)
restaurant_temp['Year'] = restaurant_temp['Year'].fillna(restaurant_temp['Date'].dt.year).astype(int)
# restaurant_temp['Month'] = restaurant_temp['Month'].fillna(restaurant_temp['Date'].dt.month)  
# dt.month doesn't work coz it gives the month number ex.2, not the month name
restaurant_temp['Month'] = restaurant_temp['Month'].fillna(restaurant_temp['Date'].dt.strftime("%b"))
restaurant_temp['Day'] = restaurant_temp['Day'].fillna(restaurant_temp['Date'].dt.day).astype(int)
restaurant_temp['Amount'] = restaurant_temp['Amount'].fillna(0.0)

restaurant_temp = restaurant_temp.rename({'Amount':'PrevRestaurantAmount'}, axis=1)

restaurant_temp = restaurant_temp.set_index('Date')
print(restaurant_temp.head(10))                                                       
cols = ['Day','Month','Year']
restaurant_temp['PrevRestaurantDate'] = restaurant_temp[cols].astype(str).apply('-'.join, axis=1)
print(restaurant_temp.head(20))
restaurant_temp['PrevRestaurantDate'] = pd.to_datetime(restaurant_temp['PrevRestaurantDate'], format="%d-%b-%Y")
print(restaurant_temp.dtypes)

## Join prev restaurant amount and prev restaurant date onto CC data_merged
restaurant_temp = restaurant_temp.drop(['Month','Year','Day'],axis=1)
print(CCdata_merged.shape)
print(restaurant_temp.shape)

CCdata_merged = CCdata_merged.join(restaurant_temp, how='left')
# dropping duplicates in CCdata_merged
CCdata_merged.drop_duplicates(subset=None,keep='first',inplace=True)

print(CCdata_merged.shape)
print(CCdata_merged.columns)
print(CCdata_merged['PrevRestaurantAmount'].count())
print(CCdata_merged['PrevRestaurantDate'].count())
