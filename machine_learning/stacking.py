from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, ExtraTreesClassifier, StackingClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
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

def train_and_save_stacking_classifier(X_train, y_train):
    print("---------- Training StackingClassifier ----------")
    # Define individual classifiers
    rf_classifier = RandomForestClassifier(n_estimators=100, random_state=42)
    gb_classifier = GradientBoostingClassifier(n_estimators=100, random_state=42)
    et_classifier = ExtraTreesClassifier(n_estimators=100, random_state=42)

    # Create a StackingClassifier
    stacking_classifier = StackingClassifier(
        estimators=[('rf', rf_classifier), ('gb', gb_classifier), ('et', et_classifier)],
        final_estimator=RandomForestClassifier(n_estimators=50, random_state=42),
        stack_method='auto',  # 'auto' uses the estimator's default stacking method
        cv=3  # Number of cross-validation folds for stacking
    )

    # Train the StackingClassifier
    stacking_classifier.fit(X_train, y_train)

    # Save the trained model using joblib
    print("---------- Saving the model ----------")
    joblib.dump(stacking_classifier, 'stacking_classifier_model.joblib')

    return stacking_classifier

def evaluate_model(model, X_test, y_test):
    print("---------- Evaluating StackingClassifier ----------")
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Accuracy: {accuracy}")
    print("Classification Report:")
    print(classification_report(y_test, y_pred))

if __name__ == "__main__":
    X, y = load_and_preprocess_data()
    X_train, X_test, y_train, y_test = split_data(X, y)
    
    # Train and evaluate StackingClassifier
    stacking_classifier_model = train_and_save_stacking_classifier(X_train, y_train)
    evaluate_model(stacking_classifier_model, X_test, y_test)
