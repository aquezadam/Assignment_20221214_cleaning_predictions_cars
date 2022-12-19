# • • • •  Perform the data cleaning operations on rest of the columns in car data v3.csv.
# Refer to comments in the code files section.

# To clean this dataframe, is essential to consider duplicate rows,
# the required format/type of the values, missing/wrong values and outliers.

# Step 1: Install and import necessary (pandas) packages
import pandas as pd

# Step 2: Read csv file using the pandas method pd.read_csv("file_name.csv")
df = pd.read_csv("Car details v3.csv")
print("MAIN INFO FOR CAR DETAILS DF")
print(df.info())
print("\n")

# Step 3: Due to the errors in the dataset, is beneficial to first remove duplicate rows.
# The method is df_name.drop_duplicates(subset=None, keep="first", inplace=False)
# subset=None means that it takes all columns, inplace=False means that a new db without the duplicates will be created.
# Afterwards, describing and making a csv file to check the data and see the difference in total rows.
non_duplicates_df = df.drop_duplicates(subset=None, keep="first", inplace=False)
print("MAIN INFO FOR CAR DETAILS NON DUPLICATES DF")
print(non_duplicates_df.info())
non_duplicates_df.describe(include="all").to_csv("summary_stats_cars.csv")
print("\n")
# Step 4: Now is time to check the format/type of the values and adjust as necessary.
# I will try it with a function and also with lambda just to see the difference on each approach
# In this case, after taking a look at the df, this step is needed for the columns: mileage, engine and max power.
# These columns have numeric value and the unit of measurement. For the purpose of this table,
# I only need the numeric information. Therefore, I need to: a) make each column a list to make iterable,
# b) make an empty list of the colum_name I need to place the num value, c) iterate with for loop each column list,
# d)split the string at the space character to get a list [num, unit], e) append the result to the empty list holding
# the num_value and f) drop the original columns and keep the ones with only the num value.

mileage_list = list(non_duplicates_df.mileage)
engine_list = list(non_duplicates_df.engine)
max_power_list = list(non_duplicates_df.max_power)

mileage_num = []
engine_num = []
max_power_num = []

def get_num_value(column_list, colum_num_value_list, data_frame, column_name_str):
    '''
    This function has a for loop to iterate through each row in the column, get the str, split it,
    extract the num, make it a float and append it to the empty list of that column. In case of no value, make it 0.
    Afterwards, it takes the df and creates a series with the pd.Series(). This pd method creates a "column" of an
    array. Then, I assign the result of the series to the df[column_name].
    :param column_list: The list with the values of the column to perform the operation
    :param colum_num_value_list: The list where all num values will be appended
    :param data_frame: Where I will add the num values given by pd.Series()
    :param column_name_str: The columns with str values that should be num
    :return:
    '''
    for i in column_list:
        try:
            num_value = i.split(' ')[0]
            colum_num_value_list.append(float(num_value))
        except:
            colum_num_value_list.append(0)

    series_column_num = pd.Series(colum_num_value_list)
    data_frame[column_name_str] = series_column_num.values

get_num_value(mileage_list, mileage_num, non_duplicates_df,"mileage_kmpl")
get_num_value(engine_list, engine_num, non_duplicates_df, "engine_CC")
get_num_value(max_power_list, max_power_num,non_duplicates_df, "max_power_bhp")


# pd.set_option('display.max_columns', None)
# print("SNEAK PEAK NON DUPLICATES DF")
# print(non_duplicates_df.info())
# print(non_duplicates_df.head())
# print("\n")

desired_data_type_df = non_duplicates_df.drop(["mileage", "engine", "max_power"], axis=1)
pd.set_option('display.max_columns', None)
print("MAIN INFO FOR CAR DETAILS DESIRED DATA TYPE DF")
desired_data_type_df.to_csv("car_details_desired_data_type.csv")
print(desired_data_type_df.info())
print(desired_data_type_df.head())
print("\n")

# Step 5: Treatment for wrong/missing values. After getting the desire data type per column, some values are either
# missing(seats) or have 0 as value because we assigned that while adjusting the data type.  For this step we can
# replace the wrong/missing value with the mean. To achieve so,
# a) count how many rows have wrong values for each column by making a list and using .count(value)
# b) Find the median of the columns that need replacing/filling.
# (Median, since the data still has outliers, median could be better suited)
# c) replace the values using the df["column_name"].replace(existing value, desired value)
# Just to have an idea of how many need replacing and confirm if is a good approach to replace

#a)
print("How many wrong rows for the columns mileage, engine, max_power:")
# print(list(desired_data_type_df.seats).count(""))
print(list(desired_data_type_df.mileage_kmpl).count(0.0))
print(list(desired_data_type_df.engine_CC).count(0.0))
print(list(desired_data_type_df.max_power_bhp).count(0.0))
#b)
seats_median = round(desired_data_type_df["seats"].median(), 3)
mileage_median = round(desired_data_type_df["mileage_kmpl"].median(), 3)
engine_median = round(desired_data_type_df["engine_CC"].median(), 3)
max_power_median = round(desired_data_type_df["max_power_bhp"].median(), 3)
km_driven_median = round(desired_data_type_df["km_driven"].median(), 3)
print(f'''The median for seats is {seats_median}, the median for mileage is {mileage_median}, 
the median for engine is {engine_median} and the median for max_power is {max_power_median}. 
The median for km_driven is {km_driven_median}''')
#c)
desired_data_type_df["seats"] = desired_data_type_df["seats"].fillna(seats_median)
desired_data_type_df["mileage_kmpl"] = desired_data_type_df["mileage_kmpl"].replace(0.0, mileage_median)
desired_data_type_df["engine_CC"] = desired_data_type_df["engine_CC"].replace(0.0, engine_median)
desired_data_type_df["max_power_bhp"] = desired_data_type_df["max_power_bhp"].replace(0.0, max_power_median)

print("MAIN INFO FOR CAR DETAILS CORRECTish VALUES DF")
desired_data_type_df.to_csv("car_details_correctish_values.csv")
print(desired_data_type_df.info())
print(desired_data_type_df.head())
print("\n")

# Step 6: Identify outliers. Outliers are numbers bigger than statistical maximum or less than statistical minimum.
# To get this information, first get the following stats: max, min, q1, q3, iqr= q3-q1, st_max= q3 + (1.5*iqr) and
# st_min = q1 - (1.5*iqr). Compare the rows with values outside st_max and st_min. Only keep the data with no outliers
# To achieve this, I write a function to print max, min, stmax and stmin and be able to draw decisions.


def stats_before_outliers(df, column_name):
    '''
    This function calculates the stats to identify st_max and st_min. It also prints the max, min, st_max
    and st_min for a column.
    :param df:
    :param column_name:
    :return: A dictionary with the st_max and st_min
    '''
    max_value = df[column_name].max()
    min_value = df[column_name].min()
    q1_value = df[column_name].quantile(0.25)
    q3_value = df[column_name].quantile(0.75)
    iqr_value = q3_value - q1_value
    st_max_value = q3_value + (1.5 * iqr_value)
    st_min_value = q1_value - (1.5 * iqr_value)
    print(f'''For {column_name}:
    - The max value is {max_value:,.2f}
    - The min value is {min_value:,.2f}
    - The stmax value is {st_max_value:,.2f}
    - The stmin value is {st_min_value:,.2f}
''')
    return {"st_max_value": st_max_value, "st_min_value":  st_min_value, }


# assign to a variable the function, knowing that the return is a dictionary. I can then access the values of this
# dictionary when I need to make comparisons based on the values of the dict.
dict_selling_price = stats_before_outliers(desired_data_type_df, "selling_price")
dict_km_driven = stats_before_outliers(desired_data_type_df, "km_driven")
dict_seats = stats_before_outliers(desired_data_type_df, "seats")
dict_mileage_kmpl = stats_before_outliers(desired_data_type_df, "mileage_kmpl")
dict_engine_CC = stats_before_outliers(desired_data_type_df, "engine_CC")
dict_max_power_bhp = stats_before_outliers(desired_data_type_df, "max_power_bhp")

# Once I know that there are outliers on each column with numeric values,
# I want to remove those outliers from each column and create a new_df.
# To do so, I need to create a new df. It will find all the rows that do not have outliers (between stmax and stmin)
# by making a comparison statement and using the & operator,
# new_df = current_df[(current_df["column_name"] <= dict_column_name["stmax]) &
#                     (current_df["column_name"] >= dict_column_name["stmin])]
# I need a new_df for each column in which I eliminate the outliers. Every new df depends on the previous
# one. E.g.: The df with only the non_outliers of selling_price is the base point for the new_df that will have only the
# non outliers of the km_driven df. This applies for all columns and all new_df's


def get_non_outliers_df(current_df, column_name):
    '''
    This function calls the stats_before_outliers function to have access to the dict with st_max and st_min.
    Then it creates a new_df based on the current datafrmae by selecting the values within st_max and st_min.
    This is done by means of comparison combined with & operator.
    :param current_df:
    :param column_name:
    :return: a new df
    '''
    st_max_min = stats_before_outliers(current_df, column_name)
    new_df = current_df[(current_df[column_name] <= st_max_min["st_max_value"]) &
                     (current_df[column_name] >= st_max_min["st_min_value"])]

    return new_df

# Calling the fn for each column w/ continuous data and then printing
# the shape to make sure the amount of rows reduces as a remove outliers in each column
df_non_outliers_price = get_non_outliers_df(desired_data_type_df,"selling_price")
previous_df_non_outliers_and_km_driven = get_non_outliers_df(df_non_outliers_price,"km_driven")
previous_df_non_outliers_and_seats = get_non_outliers_df(previous_df_non_outliers_and_km_driven,"seats")
previous_df_non_outliers_and_mileage_kmpl = get_non_outliers_df(previous_df_non_outliers_and_seats,"mileage_kmpl")
previous_df_non_outliers_and_engine_CC = get_non_outliers_df(previous_df_non_outliers_and_mileage_kmpl,"engine_CC")
df_non_outliers_overall = get_non_outliers_df(previous_df_non_outliers_and_engine_CC,"max_power_bhp")
print(f"SHAPE without outliers in selling_price:  {df_non_outliers_price.shape}.")
print(f"SHAPE without outliers in km_driven:      {previous_df_non_outliers_and_km_driven.shape}.")
print(f"SHAPE without outliers in seats:          {previous_df_non_outliers_and_seats.shape}.")
print(f"SHAPE without outliers in mileage_kmpl:   {previous_df_non_outliers_and_mileage_kmpl.shape}.")
print(f"SHAPE without outliers in engine_CC:      {previous_df_non_outliers_and_engine_CC.shape}.")
print(f"SHAPE without outliers overall:           {df_non_outliers_overall.shape}.")

# Then I print the head o take a sneak-peek of the df without outliers. Afterwards I make a csv file
print(df_non_outliers_overall.head())
df_non_outliers_overall.to_csv("non_outliers_car_details.csv")

# Then I want to know how many rows I lost in the process
print(f'''The shape of dataframe with outliers is {desired_data_type_df.shape} and the shape without outliers is {df_non_outliers_overall.shape}''')
print(f"In this process I lost {6926-4898} rows. That is about{-1*((4898-6926)/6926)*100: .2f} % decrease of rows.")
print("\n")





