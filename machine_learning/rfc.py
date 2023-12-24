from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import pandas as pd
from get_data import get_data
import joblib

# Call the function to retrieve data
_, _, client_df, immatriculation_df = get_data()

# merge client_df and inmatriculation_df with the key inmatriculation
merged_df = pd.merge(client_df, immatriculation_df, on="inmatriculation")

# Features and target
X =  merged_df.drop("marque_nom_encoded", axis=1)  # Features
y = merged_df["marque_nom_encoded"]  # Target

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Create a RandomForestClassifier
rf_classifier = RandomForestClassifier(n_estimators=100, random_state=42)

# Train the model
rf_classifier.fit(X_train, y_train)

# Save the trained model using joblib
joblib.dump(rf_classifier, 'random_forest_model.joblib')

# Make predictions on the test set
y_pred = rf_classifier.predict(X_test)

# Evaluate the model
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy}")