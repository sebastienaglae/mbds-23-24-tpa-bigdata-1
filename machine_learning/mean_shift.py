from sklearn.cluster import MeanShift
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import pandas as pd
import joblib
import customers_treater as ct

# Charger les données
customers = ct.treat_customers()

# Features and target
X = customers.drop("car_brand_name_encoded", axis=1)  # Features
y = customers["car_brand_name_encoded"]  # Target

# Division des données
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Création du modèle MeanShift
mean_shift = MeanShift()

# Entraînement du modèle
mean_shift.fit(X_train)

# Sauvegarde du modèle
joblib.dump(mean_shift, 'mean_shift_model.joblib')

# Comme MeanShift est un modèle de clustering, on n'aura pas y_train pour l'entraînement

# Prédiction sur le jeu de test
y_pred = mean_shift.predict(X_test)

# Évaluation du modèle
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy}")

# Affichage du rapport de classification
print(classification_report(y_test, y_pred))