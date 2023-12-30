import joblib
import marketing_treater as mt
from databus import Databus
import yaml
import asyncio

with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

databus = Databus(config["nats"])
databus_connect_task = databus.connect()
loop = asyncio.get_event_loop()
loop.run_until_complete(databus_connect_task)

# Get the "customer_marketing" file
print("---------- Getting the data ----------")
marketing = mt.marketing_treater()

# use random_forest_model.joblib to make predictions on the "customer_marketing" file
# and store the predictions in the "prediction" column
print("---------- Loading Model ----------")
model = joblib.load('random_forest_model.joblib')

# Drop the "prediction" column if it already exists
print("---------- Making Predictions ----------")

# Make predictions
marketing["prediction"] = model.predict(marketing)

# Decode the predictions using the brand_encoder.joblib file
print("---------- Decoding Predictions ----------")
encoder = joblib.load('brand_encoder.joblib')
marketing["prediction"] = encoder.inverse_transform(marketing["prediction"])

# Display the first 5 rows of the DataFrame
print(marketing.head())

# Save marketing DataFrame to a CSV file called "predictions.csv"
print("---------- Saving Predictions ----------")
marketing.to_csv("predictions.csv", index=False)

# publish_results()
def transform_data(row_tuple):
    _, row = row_tuple
    return {
        "customer_marketing_id": row["id"],
        "catalog_car_id": row["prediction"]
    }

databus_publish_task = databus.publish_result("customer_markting_analysis_data", marketing.iterrows(), "customer_marketing_id", transform_data, mode="upsert")
loop.run_until_complete(databus_publish_task)
