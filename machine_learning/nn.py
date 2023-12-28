from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
from sklearn.preprocessing import StandardScaler
import pandas as pd
import joblib
import customers_treater as ct

# Call the function to retrieve data
customers = ct.treat_customers()

# Features and target
X = customers.drop("car_brand_name_encoded", axis=1)  # Features
y = customers["car_brand_name_encoded"]  # Target

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Scale the input features (neural networks are sensitive to feature scales)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Create an MLPClassifier (Neural Network)
mlp_classifier = MLPClassifier(hidden_layer_sizes=(100,), max_iter=1000, random_state=42)

# Train the model
mlp_classifier.fit(X_train_scaled, y_train)

# Save the trained model using joblib
joblib.dump(mlp_classifier, 'neural_network_model.joblib')

# Make predictions on the test set
y_pred = mlp_classifier.predict(X_test_scaled)

# Evaluate the model
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy}")

# Show the classification report
print(classification_report(y_test, y_pred))
