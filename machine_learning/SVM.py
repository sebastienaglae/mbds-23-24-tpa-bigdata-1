from sklearn.svm import SVC
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import accuracy_score, classification_report
import pandas as pd
import joblib
import os
import customers_treater as ct

def load_and_preprocess_data():
    print("---------- Fetching the data ----------")
    data_file = "treated_customers.csv"
    
    if os.path.isfile(data_file):
        customers = pd.read_csv(data_file)
    else:
        customers = ct.treat_customers()
        customers.to_csv(data_file, index=False)
    
    print("---------- Data fetched ----------")
    X = customers.drop("car_brand_name_encoded", axis=1)
    y = customers["car_brand_name_encoded"]
    return X, y

def split_data(X, y, test_size=0.2, random_state=42):
    print("---------- Splitting the data ----------")
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state)
    return X_train, X_test, y_train, y_test

def perform_grid_search(X_train, y_train):
    print("---------- Performing Grid Search ----------")
    param_grid = {
        'C': [50, 100, 150],
        'gamma': [0.01, 0.1, 'scale'],
        'kernel': ['rbf', 'poly'],
        'class_weight': ['balanced']
    }

    grid_search = GridSearchCV(SVC(random_state=42), param_grid, refit=True, verbose=2, cv=3)
    grid_search.fit(X_train, y_train)

    print("Best parameters found: ", grid_search.best_params_)
    return grid_search.best_estimator_

def save_and_evaluate_model(model, X_test, y_test):
    print("---------- Saving the model ----------")
    joblib.dump(model, 'optimized_svm_model.joblib')

    print("---------- Evaluating the model ----------")
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Accuracy of SVM: {accuracy:.2f}")
    print(classification_report(y_test, y_pred, zero_division=0))

if __name__ == "__main__":
    X, y = load_and_preprocess_data()
    X_train, X_test, y_train, y_test = split_data(X, y)
    
    # Perform Grid Search for hyperparameter tuning
    best_svm_model = perform_grid_search(X_train, y_train)
    
    # Save and evaluate the optimized SVM model
    save_and_evaluate_model(best_svm_model, X_test, y_test)
