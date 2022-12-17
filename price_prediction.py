# MODEL PREDICTION:
# **Linear regression** analysis is used to predict the value of a variable based on the value of another variable.
# The variable you want to predict is called the dependent variable. The variable you are using to predict the other
# variable's value is called the independent variable.


# Step 0: Install and import necessary (pandas, scikit-learn) packages and files
import main_cars
import pandas as pd
from sklearn.model_selection import train_test_split # module to split data into training and testing
from sklearn.linear_model import LinearRegression   # linear regression is a class with an algorithm

# Step 1
# Create a new df including the column_names of the dependent column and the independent columns.
df_base_model = main_cars.df_non_outliers_overall[["selling_price", "km_driven", "fuel", "transmission", "mileage_kmpl",
                                 "engine_CC", "max_power_bhp"]]
# Step 2. Use the pd.get_dummies(df, columns=[column_name_1, column_name_n])
# to do ONE HOT ENCODING. It will make "dummy" columns for each repeated value in the columns passed as arguments.

df_linear_regression = pd.get_dummies(df_base_model, columns=["fuel", "transmission"])
print(df_linear_regression.info())
print("\n")

# Step 3. Figure out which type of fuel and transmission types are the most common.
# To do so I will do the df.groupby(["column_name])["column_name].count() -- Google told me to do this to count
# Then print to take a sneak-peek and "manually" choose. I could also try a for loop :/ but is almost midnight
cng_count_df = df_linear_regression.groupby(["fuel_CNG"])["fuel_CNG"].count()
diesel_count_df = df_linear_regression.groupby(["fuel_Diesel"])["fuel_Diesel"].count()
lpg_count_df = df_linear_regression.groupby(["fuel_LPG"])["fuel_LPG"].count()
petrol_count_df = df_linear_regression.groupby(["fuel_Petrol"])["fuel_Petrol"].count()
automatic_count_df = df_linear_regression.groupby(["transmission_Automatic"])["transmission_Automatic"].count()
manual_count_df = df_linear_regression.groupby(["transmission_Manual"])["transmission_Manual"].count()
print(f'''  - The amount of rows with fuel_CNG is: {cng_count_df}.
            - The amount of rows with fuel_diesel is: {diesel_count_df}
            - The amount of rows with fuel_lpg is: {lpg_count_df}
            - The amount of rows with fuel_petrol is: {petrol_count_df}
            - The amount of rows with automatic transmission is: {automatic_count_df}
            - The amount of rows with manual transmission is: {manual_count_df}''')
print("\n")

# Step 4.
# With the knowledge that I am doing linear regression and that the formula looks like this:
# y = mX+c                                                             y = m1*x1 + m2*x2 + mN*xN + c.
# "The formula for simple linear regression is Y = mX + c, where Y is the response (dependent) variable,
# X is the predictor (independent) variable, m is the estimated slope, and c is the estimated intercept."
# Create variables for y = df["column_to_predict"] and x = df["columns_for_prediction"]
y = df_linear_regression["selling_price"]
# In this case, simply drop the "selling_price" column from the df_linear_regression. Axis=1 refers to columns
# and in this case inplace=True because we want to modify the df
x = df_linear_regression.drop("selling_price", axis=1)

# When doing machine learning, the data is split into learning data and testing data. In this case,
# for industry purposes, 70% is for learning and 30% for testing.
# I can use train_test_split(x, y, train_size = decimal_between_0and1, random_state = None)
# the random_state TRUE would be if we want the data that constitute the percentage of
# data used for training to be gathered at random. This method returns a list containing train-test split of inputs.
x_train, x_test, y_train, y_test = train_test_split(x, y, train_size=0.70, random_state=None)
print("y_train:")
print(y_train)
print("x_train")
print(type(x_train))
print(x_train)

# Since the linear regression inside the package is a class, I need to make an instance of a class.
# We can then access the method .fit(x_train, y_train). Then we can access the attribute coefficient,
# the attribute intercept.
model = LinearRegression()
model.fit(x_train, y_train) # model.fit receives the variables x and y of the linear regression
print("The coefficients are: ", model.coef_)
print("The intercept is: ", model.intercept_)
# I can also take a sneak-peek at the columns. Since x_train is a pandas df, I can access its attribute column
# This will then help me give a list of predictors to test the model.
print("Columns to train: ")
print(x_train.columns)
print("\n")
# Get the mean of the predictor columns with continuous data. These values will be used as the mean case for a car.
km_driven_mean = round(main_cars.df_non_outliers_overall["km_driven"].mean(), 3)
mileage_mean = round(main_cars.df_non_outliers_overall["mileage_kmpl"].mean(), 3)
engine_mean = round(main_cars.df_non_outliers_overall["engine_CC"].mean(), 3)
max_power_mean = round(main_cars.df_non_outliers_overall["max_power_bhp"].mean(), 3)
print(f'''After droping duplicates, obtaining num values for what should be continuous data and removing outliers, 
the mean for km_driven is {km_driven_mean}, the mean for mileage is {mileage_mean}, 
the mean for engine is {engine_mean} and the mean for max_power is {max_power_mean}. ''')
print("\n")


# Store the prediction in variable with the method of the class model.predict([2d array])
# As a side note, dataframes are 2D arrays [[]].
selling_price_prediction_mean_median = model.predict([[km_driven_mean, mileage_mean, engine_mean,
                                                         max_power_mean, 0, 0, 0, 1, 0, 1]])
print(f'''The following prediction is based on the most repeated fuel -petrol- and the most popular transmission -manual-. 
Additionally, the mean values considered are km_driven ({km_driven_mean:,.2f}), mileage ({mileage_mean: .2f} kmpl),
engine({engine_mean: .2f} CC) and max_power({max_power_mean: .2f} bhp). 
With this in mind, the predicted price is {selling_price_prediction_mean_median}''')
print("\n")


# • • Other predictions of selling price based testing fuel and transmission.
# selling_price_prediction_CNG_automatic = model.predict([[km_driven_mean, mileage_mean, engine_mean,
#                                                          max_power_mean, 1, 0, 0, 0, 1, 0]])
# print(f'''Based on a used car with {km_driven_mean:,.2f} km driven, {mileage_mean: .2f} kmpl of mileage,
# {engine_mean: .2f} bhp of max power, fuel is CNG and the transmission is automatic, the price will be:
# {selling_price_prediction_CNG_automatic} ''')
# print("\n")
#
# selling_price_prediction_diesel_automatic = model.predict([[km_driven_mean, mileage_mean, engine_mean,
#                                                          max_power_mean, 0, 1, 0, 0, 1, 0]])
# print(f'''Based on a used car with {km_driven_mean:,.2f} km driven, {mileage_mean: .2f} kmpl of mileage,
# {engine_mean: .2f} bhp of max power, fuel is diesel and the transmission is automatic, the price will be:
# {selling_price_prediction_diesel_automatic} ''')
# print("\n")
# selling_price_prediction_LPG_automatic = model.predict([[km_driven_mean, mileage_mean, engine_mean,
#                                                          max_power_mean, 0, 0, 1, 0, 1, 0]])
# print(f'''Based on a used car with {km_driven_mean:,.2f} km driven, {mileage_mean: .2f} kmpl of mileage,
# {engine_mean: .2f} bhp of max power, fuel is LPG and the transmission is automatic, the price will be:
# {selling_price_prediction_LPG_automatic} ''')
# print("\n")
# selling_price_prediction_petrol_automatic = model.predict([[km_driven_mean, mileage_mean, engine_mean,
#                                                          max_power_mean, 0, 0, 0, 1, 1, 0]])
# print(f'''Based on a used car with {km_driven_mean:,.2f} km driven, {mileage_mean: .2f} kmpl of mileage,
# {engine_mean: .2f} bhp of max power, fuel is petrol and the transmission is automatic, the price will be:
# {selling_price_prediction_petrol_automatic} ''')
# print("\n")
# print("\n")
#
# selling_price_prediction_CNG_manual = model.predict([[km_driven_mean, mileage_mean, engine_mean,
#                                                          max_power_mean, 1, 0, 0, 0, 0, 1]])
# print(f'''Based on a used car with {km_driven_mean:,.2f} km driven, {mileage_mean: .2f} kmpl of mileage,
# {engine_mean: .2f} bhp of max power, fuel is CNG and the transmission is manual, the price will be:
# {selling_price_prediction_CNG_manual} ''')
# print("\n")
# selling_price_prediction_diesel_manual = model.predict([[km_driven_mean, mileage_mean, engine_mean,
#                                                          max_power_mean, 0, 1, 0, 0, 0, 1]])
# print(f'''Based on a used car with {km_driven_mean:,.2f} km driven, {mileage_mean: .2f} kmpl of mileage,
# {engine_mean: .2f} bhp of max power, fuel is diesel and the transmission is manual, the price will be:
# {selling_price_prediction_diesel_manual} ''')
# print("\n")
# selling_price_prediction_LPG_manual = model.predict([[km_driven_mean, mileage_mean, engine_mean,
#                                                          max_power_mean, 0, 0, 1, 0, 0, 1]])
# print(f'''Based on a used car with {km_driven_mean:,.2f} km driven, {mileage_mean: .2f} kmpl of mileage,
# {engine_mean: .2f} bhp of max power, fuel is LPG and the transmission is manual, the price will be:
# {selling_price_prediction_LPG_manual} ''')
# print("\n")
# selling_price_prediction_petrol_manual = model.predict([[km_driven_mean, mileage_mean, engine_mean,
#                                                          max_power_mean, 0, 0, 0, 1, 0, 1]])
# print(f'''Based on a used car with {km_driven_mean:,.2f} km driven, {mileage_mean: .2f} kmpl of mileage,
# {engine_mean: .2f} bhp of max power, fuel is petrol and the transmission is manual, the price will be:
# {selling_price_prediction_petrol_manual} ''')
# print("\n")

# Try more parameters