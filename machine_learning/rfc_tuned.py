from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import accuracy_score, classification_report
import joblib
import pandas as pd
import customers_treater as ct
import os

def load_and_preprocess_data(prediction_type: str = "carmodel"):
    """
    Load and preprocess customer data based on the prediction type.

    Parameters:
    - prediction_type (str): Type of prediction ("carmodel" or "category").

    Returns:
    - X (DataFrame): Features.
    - y (Series): Target variable.
    """
    print("---------- Getting the data ----------")
    # Verify if the file treated_customers.csv exists
    if os.path.isfile("treated_customers.csv"):
        customers = pd.read_csv("treated_customers.csv")
    else:
        customers = ct.treat_customers()
    print("---------- Data retrieved ----------")
    
    if prediction_type == "carmodel":
        X = customers.drop(["car_id", "car_category_id"], axis=1)
        y = customers["car_id"]
    elif prediction_type == "category":
        X = customers.drop(["car_category_id", "car_id"], axis=1)
        y = customers["car_category_id"]
        
    return X, y

def split_data(X, y, test_size=0.2, random_state=42):
    """
    Split data into training and testing sets.

    Parameters:
    - X (DataFrame): Features.
    - y (Series): Target variable.
    - test_size (float): Size of the test set.
    - random_state (int): Random seed for reproducibility.

    Returns:
    - X_train, X_test, y_train, y_test: Split datasets.
    """
    print("---------- Splitting the data ----------")
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state)
    return X_train, X_test, y_train, y_test

def hyperparameter_tuning(X_train, y_train):
    """
    Perform hyperparameter tuning using GridSearchCV.

    Parameters:
    - X_train (DataFrame): Training features.
    - y_train (Series): Training target variable.

    Returns:
    - best_params (dict): Best hyperparameters.
    """
    print("---------- Hyperparameter Tuning ----------")
    param_grid = {
        'n_estimators': [50, 100, 150],
        'max_depth': [None, 10, 20],
        'min_samples_split': [2, 5, 10],
        'min_samples_leaf': [1, 2, 4]
    }

    rf_classifier = RandomForestClassifier(random_state=42)
    grid_search = GridSearchCV(rf_classifier, param_grid, cv=3, scoring='accuracy')
    grid_search.fit(X_train, y_train)

    best_params = grid_search.best_params_
    print(f"Best Hyperparameters: {best_params}")

    return best_params

def train_and_save_random_forest(X_train, y_train, best_params):
    """
    Train RandomForestClassifier with tuned hyperparameters and save the model.

    Parameters:
    - X_train (DataFrame): Training features.
    - y_train (Series): Training target variable.
    - best_params (dict): Best hyperparameters.

    Returns:
    - rf_classifier: Trained model.
    """
    print("---------- Training RandomForestClassifier ----------")
    rf_classifier = RandomForestClassifier(random_state=42, **best_params)
    rf_classifier.fit(X_train, y_train)
    print("---------- Saving the model ----------")
    joblib.dump(rf_classifier, f'random_forest_model_{best_params}_{prediction_type}.joblib')
    return rf_classifier

def feature_importance_analysis(model, X_train):
    """
    Perform feature importance analysis.

    Parameters:
    - model: Trained model.
    - X_train (DataFrame): Training features.
    """
    print("---------- Feature Importance Analysis ----------")
    feature_importances = model.feature_importances_
    feature_importance_df = pd.DataFrame({'Feature': X_train.columns, 'Importance': feature_importances})
    feature_importance_df = feature_importance_df.sort_values(by='Importance', ascending=False)
    print("Top 5 Important Features:")
    print(feature_importance_df.head())

if __name__ == "__main__":
    # Specify the prediction type: "carmodel" or "category"
    prediction_type = "category"
    
    X, y = load_and_preprocess_data(prediction_type)
    X_train, X_test, y_train, y_test = split_data(X, y)
    
    # Hyperparameter tuning
    best_params = hyperparameter_tuning(X_train, y_train)
    
    # Train and evaluate RandomForestClassifier with tuned hyperparameters
    random_forest_model = train_and_save_random_forest(X_train, y_train, best_params)
    y_pred = random_forest_model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Accuracy on Test Set: {accuracy:.2f}")
    
    # Feature Importance Analysis
    feature_importance_analysis(random_forest_model, X_train)
