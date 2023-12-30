from get_data import get_data
from sklearn.preprocessing import LabelEncoder
import joblib

def treat_cars():

    cars, _, _, _ = get_data(["cars"])

    # Encode the "brand" column using Label Encoding
    brand_encoder = LabelEncoder()
    cars["brand_encoded"] = brand_encoder.fit_transform(cars["brand"])

    # Encode "color" column using Label Encoding
    color_encoder = LabelEncoder()
    cars["color_encoded"] = color_encoder.fit_transform(cars["color"])

    # Encode "name" using Label Encoding
    name_encoder = LabelEncoder()
    cars["name_encoded"] = name_encoder.fit_transform(cars["name"])

    # in "used" column, replace False with 0 and True with 1. create a new column "used_encoded"
    cars["used_encoded"] = cars["used"].astype(int)

    # encode "length" column using Label Encoding
    length_encoder = LabelEncoder()
    cars["length_encoded"] = length_encoder.fit_transform(cars["length"])

    # For the column "bonus_malus", where None, put 0
    cars["bonus_malus"].fillna(0, inplace=True)

    # For the column "co2_emissions", where None, put 0
    cars["co2_emissions"].fillna(0, inplace=True)

    # For the column "energy_cost", where None, put 0
    cars["energy_cost"].fillna(0, inplace=True)

    return cars