import pandas as pd
from get_data import get_data
from sklearn.preprocessing import LabelEncoder

def treat_customers():

    _, _, customers, _ = get_data()

    # Replace values in the "marital_status" column
    customers["marital_status"].replace({"single": 1, "couple": 2}, inplace=True)

    # Replace values in the "has_second_car" column
    customers["has_second_car"] = customers["has_second_car"].astype(int)

    # Replace values in the "gender" column
    customers["gender"].replace({"F": 0, "M": 1}, inplace=True)

    # Drop the "current_registration_id" column
    customers.drop("current_registration_id", axis=1, inplace=True)

    # Encode the "car_color" column using Label Encoding
    color_encoder = LabelEncoder()
    customers["car_color_encoded"] = color_encoder.fit_transform(customers["car_color"])

    # Drop the original "car_color" column
    customers.drop("car_color", axis=1, inplace=True)

    # Encode the "car_length" column using Label Encoding
    length_encoder = LabelEncoder()
    customers["car_length_encoded"] = length_encoder.fit_transform(customers["car_length"])

    # Drop the original "car_length" column
    customers.drop("car_length", axis=1, inplace=True)

    # Merge "car_brand" and "car_name" into a new column "car_brand_name"
    customers["car_brand_name"] = customers["car_brand"] + '_' + customers["car_name"]
    customers["car_brand_name"] = customers["car_brand_name"].str.replace(' ', '_')

    # Drop unnecessary columns
    customers.drop(["car_brand", "car_name"], axis=1, inplace=True)

    # Encode the "car_brand_name" column using Label Encoding
    brand_encoder = LabelEncoder()
    customers["car_brand_name_encoded"] = brand_encoder.fit_transform(customers["car_brand_name"])

    # Drop the original "car_brand_name" column
    customers.drop("car_brand_name", axis=1, inplace=True)

    # Replace values in the "car_used" column
    customers["car_used"] = customers["car_used"].astype(int)

    # Drop the "category_id" column
    customers.drop("car_category_id", axis=1, inplace=True)

    # Drop null values
    customers.dropna(inplace=True)

    return customers

