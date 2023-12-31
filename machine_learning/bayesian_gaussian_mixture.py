from sklearn.mixture import BayesianGaussianMixture
from sklearn.model_selection import train_test_split
import pandas as pd
from get_data import get_data
import joblib

# Charger les données
_, _, client_df, immatriculation_df = get_data()

# Fusionner les DataFrames
merged_df = pd.merge(client_df, immatriculation_df, on="inmatriculation")

# Sélection des caractéristiques et de la cible
X = merged_df.drop("marque_nom_encoded", axis=1) 
y = merged_df["marque_nom_encoded"]  # Cible

# Division des données
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Création du modèle BayesianGaussianMixture
bayesian_gmm = BayesianGaussianMixture(n_components=10, random_state=42)

# Entraînement du modèle
bayesian_gmm.fit(X_train)

# Sauvegarde du modèle
joblib.dump(bayesian_gmm, 'bayesian_gmm_model.joblib')
