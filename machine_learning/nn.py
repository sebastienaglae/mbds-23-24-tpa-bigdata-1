from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
from sklearn.preprocessing import StandardScaler
import joblib
import pandas as pd
import customers_treater as ct
import os

def load_and_preprocess_data():
    print("---------- Getting the data ----------")
    # verify if the file treated_customers.csv exists
    if os.path.isfile("treated_customers.csv"):
        customers = pd.read_csv("treated_customers.csv")
    else:
        customers = ct.treat_customers()
    print("---------- Data retrieved ----------")
    X = customers.drop("car_brand_name_encoded", axis=1)  # Features
    y = customers["car_brand_name_encoded"]  # Target
    return X, y

def split_data(X, y, test_size=0.2, random_state=42):
    print("---------- Splitting the data ----------")
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state)
    return X_train, X_test, y_train, y_test

def scale_features(X_train, X_test):
    print("---------- Scaling the input features ----------")
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    return X_train_scaled, X_test_scaled

def train_and_save_neural_network(X_train_scaled, y_train):
    print("---------- Training the MLPClassifier (Neural Network) ----------")
    mlp_classifier = MLPClassifier(hidden_layer_sizes=(100,), max_iter=1000, random_state=42)
    mlp_classifier.fit(X_train_scaled, y_train)
    print("---------- Saving the Neural Network model ----------")
    joblib.dump(mlp_classifier, 'neural_network_model.joblib')
    return mlp_classifier

def evaluate_model(model, X_test_scaled, y_test):
    print("---------- Evaluating the model ----------")
    y_pred = model.predict(X_test_scaled)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Accuracy: {accuracy}")
    print("Classification Report:")
    print(classification_report(y_test, y_pred))

if __name__ == "__main__":
    X, y = load_and_preprocess_data()
    X_train, X_test, y_train, y_test = split_data(X, y)
    X_train_scaled, X_test_scaled = scale_features(X_train, X_test)
    neural_network_model = train_and_save_neural_network(X_train_scaled, y_train)
    evaluate_model(neural_network_model, X_test_scaled, y_test)
