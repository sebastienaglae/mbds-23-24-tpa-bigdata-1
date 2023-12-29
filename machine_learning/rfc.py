from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import customers_treater as ct
import joblib
import os
import pandas as pd

def load_and_preprocess_data():
    print("---------- Fetching the data ----------")
    # verify if the file treated_customers.csv exists
    if os.path.isfile("treated_customers.csv"):
        customers = pd.read_csv("treated_customers.csv")
    else:
        customers = ct.treat_customers()
    print("---------- Data fetched ----------")
    X = customers.drop("car_brand_name_encoded", axis=1)
    y = customers["car_brand_name_encoded"]
    return X, y

def train_and_save_model(X_train, y_train):
    print("---------- Training the RandomForestClassifier ----------")
    rf_classifier = RandomForestClassifier(n_estimators=100, random_state=42)
    rf_classifier.fit(X_train, y_train)
    print("---------- Saving the RandomForestClassifier model ----------")
    joblib.dump(rf_classifier, 'random_forest_model_TEST.joblib')
    return rf_classifier

def evaluate_model(model, X_test, y_test):
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Accuracy: {accuracy}")
    print("Classification Report:")
    print(classification_report(y_test, y_pred))

if __name__ == "__main__":
    X, y = load_and_preprocess_data()
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    rf_model = train_and_save_model(X_train, y_train)
    evaluate_model(rf_model, X_test, y_test)
