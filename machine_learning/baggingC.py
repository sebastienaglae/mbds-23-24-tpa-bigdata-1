from sklearn.ensemble import BaggingClassifier, RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import joblib
import customers_treater as ct
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

def train_and_save_bagging_classifier(X_train, y_train):
    print("---------- Training BaggingClassifier ----------")
    base_classifier = RandomForestClassifier(n_estimators=100, random_state=42)
    bagging_classifier = BaggingClassifier(base_classifier, n_estimators=10, random_state=42)
    bagging_classifier.fit(X_train, y_train)
    print("---------- Saving BaggingClassifier model ----------")
    joblib.dump(bagging_classifier, 'bagging_classifier_model.joblib')
    return bagging_classifier

def evaluate_model(model, X_test, y_test):
    print("---------- Evaluating BaggingClassifier ----------")
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Accuracy: {accuracy}")
    print("Classification Report:")
    print(classification_report(y_test, y_pred))

if __name__ == "__main__":
    X, y = load_and_preprocess_data()
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Train and evaluate BaggingClassifier
    bagging_classifier_model = train_and_save_bagging_classifier(X_train, y_train)
    evaluate_model(bagging_classifier_model, X_test, y_test)
