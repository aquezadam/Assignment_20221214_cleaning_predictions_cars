# • • • • Consider the sample_dataset of sales from mongo db and convert the document
# structure into dataframe with multiple columns. Convert the data frame into csv
# to submit in the zip file

# Step 1: Install and import necessary (pandas, pymongo, certifi) packages
import pandas as pd
import pymongo
import certifi

import password

# Step 2: Connect with the database and collection
client = pymongo.MongoClient(f"mongodb+srv://aqm:{password.password}@assignment20221214.5jkaupz.mongodb.net/?retryWrites=true&w=majority", tlsCAFile=certifi.where())
db = client["sample_supplies"]
collection = db["sales"]

# Step 3: Take a look at the collection by appending an empty list with all the documents fetched using the .find({}).
# Access the first row and use .keys() to take a look at the schema of the document.
db_list = []
for document in collection.find({}):
    db_list.append(document)
print("First row. Sneak peak")
print(db_list[0])
print("First row. Schema")
print(db_list[0].keys())
print("\n")

# Step 4: Get the keys of the documents that have embedded documents.
# Use .keys() for dictionaries and indexing for lists
keys_in_customers = db_list[0]["customer"].keys()
print("keys_in_customers")
print(keys_in_customers)
keys_in_items = db_list[0]["items"][0]
print("keys_in_items")
print(keys_in_items)
print("\n")

# Step 5:Make empty lists for each key of each document
sale_date_list = []
store_location_list = []
coupon_used_list = []
purchase_method_list = []
# In case of documents with embedded documents,
# make an empty list for the keys inside dictionaries/object. In this case customers
customer_gender_list = []
customer_age_list = []
customer_email_list = []
customer_satisfaction_list = []
# For the documents that are lists/arrays, make an empty list for each key inside each dictionary element of the array.
# In this case, items is an array with dictionaries: [{"name":value, "tags":[value], "price":value, "quantity": value}]
items_name_list = []
items_tags_list = []
items_price_list = []
items_quantity_list = []

# Do a for loop per document in collection and append the values to the corresponding empty list.
for document in db_list:
    #  for documents: key_list.append(iterable["key_name"])
    sale_date_list.append(document["saleDate"])
    store_location_list.append(document["storeLocation"])
    coupon_used_list.append(document["couponUsed"])
    purchase_method_list.append(document["purchaseMethod"])
    # for embedded documents: mainkey_innerkey_list.append(document["mainkey_name"]["innerkey_name"])
    customer_gender_list.append(document["customer"]["gender"])
    customer_age_list.append(document["customer"]["age"])
    customer_email_list.append(document["customer"]["email"])
    customer_satisfaction_list.append(document["customer"]["satisfaction"])

#   for the items array: The elements inside the array are dictionaries.
#   Make an empty list for each key of the dictionary element. These empty lists will be appended later.
    items_name = []
    items_tags = []
    items_price = []
    items_quantity = []

# to populate the items array, do a for loop iterating through each dictionary element inside the array.
# Append each key inside each dictionary element of the array to the empty list that refers to array_key

    for i in document["items"]:
        items_name.append(i["name"])
        items_tags.append(i["tags"])
        items_price.append(i["price"])
        items_quantity.append(i["quantity"])

# Append the list from the inner loop to the corresponding global empty list.
    items_name_list.append(items_name)
    items_tags_list.append(items_tags)
    items_price_list.append(items_price)
    items_quantity_list.append(items_quantity)


# Step 6: With the help of the pandas package, use the pd.DataFrame to create a dataframe based on the collection.
# Inside use the zip() method, to compress the variables that will become columns in the dataframe.
# A suggestion for the signature is
# df = pd.DataFrame(zip(variable1_populate_dataframe, ... ,variableN_populate_dataframe))
df = pd.DataFrame(zip(sale_date_list, items_name_list, items_tags_list, items_price_list, items_quantity_list,
                      store_location_list, customer_gender_list, customer_age_list, customer_email_list,
                      customer_satisfaction_list, coupon_used_list, purchase_method_list))

# To define the columns' names, specify the elements of the column attribute of the dataframe.
# The order and name of the columns should correspond to the  order and name of the variables
# that serves as argument of the zip() method
df.columns = ["sale_date", "item_name", "item_tags", "item_price","item_quantity", "store_location", "customer_gender",
              "customer_age", "customer_email", "customer_satisfaction", "coupon_used", "purchase_method"]
pd.set_option('display.max_columns', None)
print(df.head())

# Step 7. Make it a csv file with the signature: dataframe_name.to_csv("file_name.csv")
df.to_csv("sample_supplies_sales.csv")







