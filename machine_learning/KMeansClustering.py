from sklearn.cluster import KMeans
from sklearn.model_selection import train_test_split
from sklearn.metrics import silhouette_score
import customers_treater as ct
import joblib
import os
import pandas as pd

def load_and_preprocess_data():
    """
    Load and preprocess customer data.

    Returns:
    - X (DataFrame): Features.
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
    
    X = customers.drop(["car_category_id", "car_brand_name_encoded"], axis=1)
    
    return X

def train_and_save_kmeans_model(X, n_clusters=3):
    """
    Train a KMeans model and save the model.

    Parameters:
    - X (DataFrame): Features.
    - n_clusters (int): Number of clusters.

    Returns:
    - KMeans: Trained model.
    """
    print(f"---------- Training the KMeans model with {n_clusters} clusters ----------")
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    kmeans.fit(X)
    
    # Save the model
    model_filename = f'kmeans_{n_clusters}_clusters.joblib'
    joblib.dump(kmeans, model_filename)
    
    print(f"---------- KMeans model saved as {model_filename} ----------")
    
    return kmeans

def evaluate_kmeans_model(model, X):
    """
    Evaluate the performance of the KMeans model.

    Parameters:
    - model: Trained KMeans model.
    - X (DataFrame): Features.
    """
    labels = model.predict(X)
    silhouette = silhouette_score(X, labels)
    print(f"Silhouette Score: {silhouette}")

if __name__ == "__main__":
    X = load_and_preprocess_data()
    kmeans_model = train_and_save_kmeans_model(X, n_clusters=3)
    evaluate_kmeans_model(kmeans_model, X)
