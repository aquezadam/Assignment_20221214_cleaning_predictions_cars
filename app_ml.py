import pickle
import streamlit as st

# regressor is the model
testing_model = pickle.load(open("model.pkl", "rb"))
fuel_options = ["CNG", "Diesel", "LPG", "Petrol"]
transmission_options = ["Automatic", "Manual"]

title = st.title("USED CARS PRICE CALCULATOR")

kms_driven = st.number_input("Please enter KM driven:")
mileage = st.number_input("Please enter mileage kmpl:")
engine = st.number_input("Please enter engine CC:")
max_power = st.number_input("Please enter max_power bhp:")
fuel_selection = st.selectbox("Please select type of fuel:", fuel_options)
transmission_selection = st.radio("Please select type of transmission", transmission_options)


def get_categorical_list(categorical_values_list):
    '''
    This function gets the values of the dummies list and returns
    a list based on the selected category.
    :param categorical_values_list:
    :return: tuple of two lists, one for fuel and one for transmission
    '''
    fuel_conversion = [0, 0, 0, 0]
    transmission_conversions = [0, 0]
    if fuel_selection in fuel_options:
        index_value_f = fuel_options.index(fuel_selection)
        fuel_conversion[index_value_f] = 1
    if transmission_selection in transmission_options:
        index_value_t = transmission_options.index(transmission_selection)
        transmission_conversions[index_value_t] = 1
    return fuel_conversion, transmission_conversions


selected_fuel_list = get_categorical_list(fuel_options)[0]
selected_transmission_list = get_categorical_list(transmission_options)[1]

# BTW, you can concateate lists!!!! To create and "automated list with
list_x_values = [kms_driven, mileage, engine, max_power] + selected_fuel_list + selected_transmission_list
if st.button("Click to predict price based on the given input."):
    prediction_price = testing_model.predict([list_x_values])
    st.success(prediction_price)