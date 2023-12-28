from sklearn.svm import SVC
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import accuracy_score, classification_report
from sklearn.decomposition import PCA
import pandas as pd
import customers_treater as ct
import joblib

# Traitement des données
customers = ct.treat_customers()

# Longueur du DataFrame 'customers'
length_of_customers_df = len(customers)
print(f"Nombre de lignes dans le DataFrame 'customers': {length_of_customers_df}")


# Sélection des caractéristiques et de la cible
X = customers.drop("car_brand_name_encoded", axis=1)
y = customers["car_brand_name_encoded"]

# PCA pour la réduction de dimensionnalité
pca = PCA(n_components=3)  
X_pca = pca.fit_transform(X)

# Division des données en ensembles d'entraînement et de test
X_train_pca, X_test_pca, y_train, y_test = train_test_split(X_pca, y, test_size=0.2, random_state=42)

# Définition de la grille de recherche pour GridSearchCV
param_grid = {
    'C': [50, 100, 200],
    'gamma': [0.01, 0.1, 'scale'],
    'kernel': ['rbf', 'poly'],
    'class_weight': ['balanced'] 
}

# Recherche par grille avec prise en compte de l'équilibre des classes
grid_search = GridSearchCV(SVC(random_state=42), param_grid, refit=True, verbose=2, cv=5)
grid_search.fit(X_train_pca, y_train)

# Affichage des meilleurs paramètres
print("Meilleurs paramètres trouvés : ", grid_search.best_params_)

# Sauvegarde du modèle avec les meilleurs paramètres
best_svm_model = grid_search.best_estimator_
joblib.dump(best_svm_model, 'optimized_svm_pca_model.joblib')

# Prédiction avec le meilleur modèle
y_pred = best_svm_model.predict(X_test_pca)

# Évaluation du modèle optimisé
accuracy = accuracy_score(y_test, y_pred)
print(f"Précision du SVM avec PCA: {accuracy:.2f}")
print(classification_report(y_test, y_pred, zero_division=0)) 
