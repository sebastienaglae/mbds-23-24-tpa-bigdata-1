import pandas as pd
from sklearn.cluster import SpectralClustering
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split, GridSearchCV
import joblib
import customers_treater as ct

# Charger les données
customers = ct.treat_customers()

# Sélection des caractéristiques et de la cible
X = customers.drop("car_brand_name_encoded", axis=1)
y = customers["car_brand_name_encoded"]

# Standardisation des caractéristiques
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Réduction de dimensionnalité avec PCA
pca = PCA(n_components=3)  # Ajustez ce nombre en fonction de vos données
X_pca = pca.fit_transform(X_scaled)

# Application du clustering spectral
spectral = SpectralClustering(n_clusters=13, affinity='rbf', random_state=42)
clusters = spectral.fit_predict(X_pca)

# Préparation des données pour la classification
X_train, X_test, y_train, y_test = train_test_split(clusters.reshape(-1, 1), y, test_size=0.2, random_state=42)

# Optimisation des hyperparamètres du RandomForestClassifier avec GridSearchCV
param_grid = {
    'n_estimators': [100, 200, 300],
    'max_depth': [10, 20, 30]
}
grid_search = GridSearchCV(RandomForestClassifier(random_state=42), param_grid, cv=4)
grid_search.fit(X_train, y_train)

# Meilleur modèle RandomForest
best_rf = grid_search.best_estimator_

# Prédiction et évaluation avec le meilleur modèle
y_pred = best_rf.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"Précision améliorée: {accuracy * 100:.2f}%")
print(classification_report(y_test, y_pred))

# Sauvegarde du modèle
joblib.dump(best_rf, 'spectral_rf_model_optimized.joblib')
