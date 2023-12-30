from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, mean_squared_error
import customers_treater as ct
import joblib
import os
import pandas as pd
import numpy as np

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
        X = customers.drop(["car_id", "car_category_id"], axis=1)
        y = customers["car_id"]
    elif prediction_type == "category":
        X = customers.drop(["car_category_id", "car_id"], axis=1)
        y = customers["car_category_id"]
    
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
    rf_classifier = RandomForestRegressor(n_estimators=100, random_state=42)
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

def evaluate_regression_model(model, X_test, y_test):
    print("---------- Evaluating the Regression model ----------")
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)
    r_squared = model.score(X_test, y_test)

    print(f"Mean Squared Error (MSE): {mse}")
    print(f"Root Mean Squared Error (RMSE): {rmse}")
    print(f"R-squared: {r_squared}")

if __name__ == "__main__":
    prediction_type = "carmodel"
    X, y = load_and_preprocess_data(prediction_type)
    print(f"X shape: {X.shape}")
    print(f"y shape: {y.shape}")
    print(f"X head:\n{X.head()}")
    print(f"y head:\n{y.head()}")
    # print y data type
    print(f"y data type: {y.dtype}")
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    # rf_model = train_and_save_model(X_train, y_train, prediction_type=prediction_type)
    # evaluate_model(rf_model, X_test, y_test)
    rf_regressor = train_and_save_model(X_train, y_train, prediction_type)
    evaluate_regression_model(rf_regressor, X_test, y_test)
