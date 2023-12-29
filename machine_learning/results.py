import joblib
import marketing_treater as mt

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