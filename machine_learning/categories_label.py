
from get_data import get_data
from databus import Databus
import yaml
import asyncio
import pandas as pd
import numpy as np

with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

databus = Databus(config["nats"])
databus_connect_task = databus.connect()
loop = asyncio.get_event_loop()
loop.run_until_complete(databus_connect_task)

# Get cars data
car_dealer_df, _, _, _ = get_data(["cars"])

# Divide the cars by "category_id"
cars_by_category = car_dealer_df.groupby("category_id")

# I want to label each category with a name
# For the category with less power mean, I will label it "economic"
# For the category with more power mean, I will label it "sport"
# For the category with the mean between the two, I will label it "standard"
# If the mean lenght is "very_long" I will label it "family"
# If the mean lenght is "very_short" I will label it "city"
# For the categoty with the highest mean price, I will label it "luxury"

category_names = ["economic", "standard", "sport", "family", "city", "luxury"]

category_0 = cars_by_category.get_group(0)
category_1 = cars_by_category.get_group(1)
category_2 = cars_by_category.get_group(2)
category_3 = cars_by_category.get_group(3)
category_4 = cars_by_category.get_group(4)
category_5 = cars_by_category.get_group(5)

category_0_mean_power = category_0["power"].mean()
category_1_mean_power = category_1["power"].mean()
category_2_mean_power = category_2["power"].mean()
category_3_mean_power = category_3["power"].mean()
category_4_mean_power = category_4["power"].mean()
category_5_mean_power = category_5["power"].mean()

# The length is a string (very_short, very_short, very_short, long, very_long)
# Count the number of cars for each length
category_0_length_counts = category_0["length"].value_counts()
category_1_length_counts = category_1["length"].value_counts()
category_2_length_counts = category_2["length"].value_counts()
category_3_length_counts = category_3["length"].value_counts()
category_4_length_counts = category_4["length"].value_counts()
category_5_length_counts = category_5["length"].value_counts()

# For the category with the highest mean price, I will label it "luxury"
category_0_mean_price = category_0["price"].mean()
category_1_mean_price = category_1["price"].mean()
category_2_mean_price = category_2["price"].mean()
category_3_mean_price = category_3["price"].mean()
category_4_mean_price = category_4["price"].mean()
category_5_mean_price = category_5["price"].mean()

# Define labels based on the calculated statistics. The relation between the label and the category is: 1:1
category_mapping = {}

# List of categories availables
categories_availables = [0, 1, 2, 3, 4, 5]

# For the second category with less power mean, I will label it "economic"
second_less_power_mean_categories = [category_0_mean_power, category_1_mean_power, category_2_mean_power, category_3_mean_power, category_4_mean_power, category_5_mean_power].index(sorted([category_0_mean_power, category_1_mean_power, category_2_mean_power, category_3_mean_power, category_4_mean_power, category_5_mean_power])[1])
category_mapping[second_less_power_mean_categories] = "economic"

# Remove the category with less power mean from the list
categories_availables.pop(second_less_power_mean_categories)

# For the second category with more power mean, I will label it "sport"
second_more_power_mean_categories = [category_0_mean_power, category_1_mean_power, category_2_mean_power, category_3_mean_power, category_4_mean_power, category_5_mean_power].index(sorted([category_0_mean_power, category_1_mean_power, category_2_mean_power, category_3_mean_power, category_4_mean_power, category_5_mean_power])[4])
category_mapping[second_more_power_mean_categories] = "sport"

# Remove the category with more power mean from the list
print(second_more_power_mean_categories)
categories_availables.pop(second_less_power_mean_categories)


# For the category with highest mean price, I will label it "luxury"
highest_mean_price_categories = [category_0_mean_price, category_1_mean_price, category_2_mean_price, category_3_mean_price, category_4_mean_price, category_5_mean_price].index(max(category_0_mean_price, category_1_mean_price, category_2_mean_price, category_3_mean_price, category_4_mean_price, category_5_mean_price))
category_mapping[highest_mean_price_categories] = "luxury"

# Remove the category with highest mean price from the list
categories_availables.pop(highest_mean_price_categories)

# For the category with the lowest mean price, I will label it "standard"
lowest_mean_price_categories = [category_0_mean_price, category_1_mean_price, category_2_mean_price, category_3_mean_price, category_4_mean_price, category_5_mean_price].index(min(category_0_mean_price, category_1_mean_price, category_2_mean_price, category_3_mean_price, category_4_mean_price, category_5_mean_price))
category_mapping[lowest_mean_price_categories] = "standard"

# Remove the category with lowest mean price from the list
categories_availables.pop(lowest_mean_price_categories)

# For the category with the most cars with "very_long" length, I will label it "family"
most_cars_very_long_categories = [category_0_length_counts["very_long"], category_1_length_counts["very_long"], category_2_length_counts["very_long"], category_3_length_counts["very_long"], category_4_length_counts["very_long"], category_5_length_counts["very_long"]].index(max(category_0_length_counts["very_long"], category_1_length_counts["very_long"], category_2_length_counts["very_long"], category_3_length_counts["very_long"], category_4_length_counts["very_long"], category_5_length_counts["very_long"]))
category_mapping[most_cars_very_long_categories] = "family"

# Remove the category with most cars with "very_long" length from the list
categories_availables.pop(most_cars_very_long_categories)

# For the category with the most cars with "very_short" length, I will label it "city"
most_cars_very_short_categories = [category_0_length_counts["very_short"], category_1_length_counts["very_short"], category_2_length_counts["very_short"], category_3_length_counts["very_short"], category_4_length_counts["very_short"], category_5_length_counts["very_short"]].index(max(category_0_length_counts["very_short"], category_1_length_counts["very_short"], category_2_length_counts["very_short"], category_3_length_counts["very_short"], category_4_length_counts["very_short"], category_5_length_counts["very_short"]))
category_mapping[most_cars_very_short_categories] = "city"

# Remove the category with most cars with "very_short" length from the list
categories_availables.pop(most_cars_very_short_categories)

# Add the "category_name" column to the DataFrame
car_dealer_df["category_name"] = car_dealer_df["category_id"].map(category_mapping)

# Create a df with the "category_id" and "category_name" columns (category_id is the index unique identifier)
category_df = car_dealer_df[["category_id", "category_name"]].drop_duplicates().set_index("category_id")

print(category_df)
