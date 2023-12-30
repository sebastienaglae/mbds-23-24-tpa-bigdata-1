from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import customers_treater as ct
import joblib
import os
import pandas as pd

def load_and_preprocess_data(prediction_type: str = "carmodel"):
    """
    Load and preprocess customer data based on the prediction type.

    Parameters:
    - prediction_type (str): Type of prediction ("carmodel" or "category").

    Returns:
    - X (DataFrame): Features.
    - y (Series): Target variable.
    """
    print("---------- Fetching the data ----------")
    # Verify if the file treated_customers.csv exists
    if os.path.isfile("treated_customers.csv"):
        customers = pd.read_csv("treated_customers.csv")
    else:
        customers = ct.treat_customers()
    
    # Display the dataset shape
    print(f"Dataset shape: {customers.shape}")

    print("---------- Data fetched ----------")
    
    if prediction_type == "carmodel":
        X = customers.drop("car_brand_name_encoded", axis=1)
        y = customers["car_brand_name_encoded"]
    elif prediction_type == "category":
        X = customers.drop("category_id", axis=1)
        y = customers["category_id"]
    
    return X, y

def train_and_save_model(X_train, y_train, prediction_type: str = "carmodel"):
    """
    Train a RandomForestClassifier and save the model.

    Parameters:
    - X_train (DataFrame): Training features.
    - y_train (Series): Training target variable.
    - prediction_type (str): Type of prediction ("carmodel" or "category").

    Returns:
    - RandomForestClassifier: Trained model.
    """
    print(f"---------- Training the RandomForestClassifier for {prediction_type} ----------")
    rf_classifier = RandomForestClassifier(n_estimators=100, random_state=42)
    rf_classifier.fit(X_train, y_train)
    
    # Save the model
    model_filename = f'random_forest_prediction_{prediction_type}.joblib'
    joblib.dump(rf_classifier, model_filename)
    
    print(f"---------- RandomForestClassifier model saved as {model_filename} ----------")
    
    return rf_classifier

def evaluate_model(model, X_test, y_test):
    """
    Evaluate the performance of the model.

    Parameters:
    - model: Trained model.
    - X_test (DataFrame): Test features.
    - y_test (Series): Test target variable.
    """
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Accuracy: {accuracy}")
    print("Classification Report:")
    print(classification_report(y_test, y_pred))

if __name__ == "__main__":
    X, y = load_and_preprocess_data("category")
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    rf_model = train_and_save_model(X_train, y_train, prediction_type="category")
    evaluate_model(rf_model, X_test, y_test)
