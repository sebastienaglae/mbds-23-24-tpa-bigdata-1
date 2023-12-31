import pandas as pd
from get_data import get_data
from sklearn.preprocessing import LabelEncoder
import joblib

def treat_customers():

    _, _, customers, _ = get_data(["customers"])

    # Replace values in the "marital_status" column
    customers["marital_status"].replace({"single": 1, "couple": 2, "married": 2, "divorced": 1}, inplace=True)

    # Replace values in the "has_second_car" column. If NaN then 0
    customers["has_second_car"].fillna(False, inplace=True)
    customers["has_second_car"] = customers["has_second_car"].astype(int)

    # Replace values in the "gender" column
    customers["gender"].replace({"F": 0, "M": 1}, inplace=True)

    # Drop the "current_registration_id" column
    customers.drop("current_registration_id", axis=1, inplace=True)

    # Merge "car_brand" and "car_name" into a new column "car_brand_name"
    customers["car_brand_name"] = customers["car_brand"] + '_' + customers["car_name"]
    customers["car_brand_name"] = customers["car_brand_name"].str.replace(' ', '_')

    # Encode the "car_brand_name" column using Label Encoding
    # brand_encoder = LabelEncoder()
    # customers["car_brand_name_encoded"] = brand_encoder.fit_transform(customers["car_brand_name"])

    # Drop all the columns starting with "car_" except "car_brand_name_encoded"
    customers.drop(customers.filter(regex='^car_').columns.difference(['car_category_id', 'car_id']), axis=1, inplace=True)

    # joblib.dump(brand_encoder, 'brand_encoder.joblib')

    # Drop null values
    customers.dropna(inplace=True)

    # Drop "customer_id" column
    customers.drop("customer_id", axis=1, inplace=True)

    # save the treated data
    customers.to_csv("treated_customers.csv", index=False)

    return customers
