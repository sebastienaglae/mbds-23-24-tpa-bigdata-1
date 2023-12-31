from sklearn.cluster import KMeans
import cars_treater as ct
from databus import Databus
import yaml
import asyncio
import matplotlib.pyplot as plt
import seaborn as sns

with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

databus = Databus(config["nats"])
databus_connect_task = databus.connect()
loop = asyncio.get_event_loop()
loop.run_until_complete(databus_connect_task)

# Fetch and treat the data
cars = ct.treat_cars()

# Select relevant features for clustering
features_for_clustering = ['bonus_malus', 'co2_emissions', 'energy_cost', 'number_doors', 'power',
                            'price', 'seating_capacity', 'used_encoded', 'brand_encoded', 'color_encoded',
                            'name_encoded', 'length_encoded']

X = cars[features_for_clustering]

# Perform K-means clustering with multiple k values (3 to 7)
k_values = list(range(3, 7))
inertia_values = []

for k in k_values:
    kmeans = KMeans(n_clusters=k, random_state=42)
    kmeans.fit(X)
    inertia_values.append(kmeans.inertia_)

# Plot the elbow curve
plt.figure(figsize=(8, 6))
sns.lineplot(x=k_values, y=inertia_values, marker='o')
plt.title('Elbow Method for Optimal k')
plt.xlabel('Number of Clusters (k)')
plt.ylabel('Inertia (Within-cluster Sum of Squares)')
plt.show()

# Perform K-means clustering with optimal k value
optimal_k = 6
kmeans = KMeans(n_clusters=optimal_k, random_state=42)
cars['category_id'] = kmeans.fit_predict(X)

# Remove the encoded columns
cars.drop(['brand_encoded', 'color_encoded', 'name_encoded', 'length_encoded', 'used_encoded'], axis=1, inplace=True)

def transform_data(row_tuple):
    _, row = row_tuple
    return {
        "id": row["id"],
        "category_id": row["category_id"]
    }

databus_publish_task = databus.publish_result("catalog_car", cars.iterrows(), "id", transform_data, mode="update")
loop.run_until_complete(databus_publish_task)
