from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import pandas as pd
import customers_treater as ct
import joblib
from sklearn.metrics import f1_score


customers = ct.treat_customers()

# Features and target
X =  customers.drop("car_brand_name_encoded", axis=1)  # Features
y = customers["car_brand_name_encoded"]  # Target

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

# Show the classification report
print(classification_report(y_test, y_pred))