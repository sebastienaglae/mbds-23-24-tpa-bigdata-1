from sklearn.cluster import KMeans
import cars_treater as ct

# Fetch and treat the data
cars = ct.treat_cars()

# Select relevant features for clustering
features_for_clustering = ['bonus_malus', 'co2_emissions', 'energy_cost', 'number_doors', 'power',
                            'price', 'seating_capacity', 'used_encoded', 'brand_encoded', 'color_encoded',
                            'name_encoded', 'length_encoded']

X = cars[features_for_clustering]

# Perform K-means clustering with 6 clusters
num_clusters = 6
kmeans = KMeans(n_clusters=num_clusters, random_state=42)
cars['category_id'] = kmeans.fit_predict(X)

# Display the distribution of data points in each cluster
cluster_distribution = cars['category_id'].value_counts().sort_index()
print("Cluster distribution:")
print(cluster_distribution)


# Remove the encoded columns
cars.drop(['brand_encoded', 'color_encoded', 'name_encoded', 'length_encoded', 'used_encoded'], axis=1, inplace=True)


# publish_results()