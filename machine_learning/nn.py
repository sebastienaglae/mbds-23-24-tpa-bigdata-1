from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
from sklearn.preprocessing import StandardScaler
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
        y_column = "car_brand_name_encoded"
    elif prediction_type == "category":
        y_column = "category_id"
    else:
        raise ValueError("Invalid prediction type. Supported types: 'carmodel' or 'category'.")

    X = customers.drop(y_column, axis=1)  # Features
    y = customers[y_column]  # Target
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

def scale_features(X_train, X_test):
    """
    Scale input features using StandardScaler.

    Parameters:
    - X_train (DataFrame): Training features.
    - X_test (DataFrame): Testing features.

    Returns:
    - X_train_scaled, X_test_scaled: Scaled datasets.
    """
    print("---------- Scaling the input features ----------")
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    return X_train_scaled, X_test_scaled

def train_and_save_neural_network(X_train_scaled, y_train):
    """
    Train MLPClassifier (Neural Network) and save the model.

    Parameters:
    - X_train_scaled (DataFrame): Scaled training features.
    - y_train (Series): Training target variable.

    Returns:
    - mlp_classifier: Trained model.
    """
    print("---------- Training the MLPClassifier (Neural Network) ----------")
    mlp_classifier = MLPClassifier(hidden_layer_sizes=(100,), max_iter=1000, random_state=42)
    mlp_classifier.fit(X_train_scaled, y_train)
    print("---------- Saving the Neural Network model ----------")
    joblib.dump(mlp_classifier, f'neural_network_model_{prediction_type}.joblib')
    return mlp_classifier

def evaluate_model(model, X_test_scaled, y_test):
    """
    Evaluate the model.

    Parameters:
    - model: Trained model.
    - X_test_scaled (DataFrame): Scaled testing features.
    - y_test (Series): Testing target variable.
    """
    print("---------- Evaluating the model ----------")
    y_pred = model.predict(X_test_scaled)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Accuracy: {accuracy}")
    print("Classification Report:")
    print(classification_report(y_test, y_pred))

if __name__ == "__main__":
    # Specify the prediction type: "carmodel" or "category"
    prediction_type = "category"
    
    X, y = load_and_preprocess_data(prediction_type)
    X_train, X_test, y_train, y_test = split_data(X, y)
    X_train_scaled, X_test_scaled = scale_features(X_train, X_test)
    neural_network_model = train_and_save_neural_network(X_train_scaled, y_train)
    evaluate_model(neural_network_model, X_test_scaled, y_test)
