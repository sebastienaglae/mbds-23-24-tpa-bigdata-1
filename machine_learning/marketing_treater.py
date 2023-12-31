import pandas as pd
from get_data import get_data

def marketing_treater():

    _, marketing, _, _ = get_data(["customer_marketing"])

    # Replace values in the "marital_status" column
    marketing["marital_status"].replace({"single": 1, "couple": 2, "married": 2, "divorced": 1}, inplace=True)

    # Replace values in the "has_second_car" column
    marketing["has_second_car"] = marketing["has_second_car"].astype(int)

    # Drop the column id
    marketing.drop("id", axis=1, inplace=True)

    # Replace values in the "gender" column
    marketing["gender"].replace({"F": 0, "M": 1}, inplace=True)


    print(marketing.head())
    return marketing