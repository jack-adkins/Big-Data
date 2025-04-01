import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.sparse import coo_matrix

file_path = 'C:\\Users\\jacks\\OneDrive\\Documents\\BigData\\chicago-taxi-rides.csv'
taxi_data = pd.read_csv(file_path)

# Removing null values from columns
taxi_data_cleaned = taxi_data.dropna(subset=['pickup_community_area', 'dropoff_community_area'])

# Making sure everything is ints
pickup = taxi_data_cleaned['pickup_community_area'].astype(int)
dropoff = taxi_data_cleaned['dropoff_community_area'].astype(int)
trips = taxi_data_cleaned['trips']

# Scatterplotting
plt.figure(figsize=(10, 8))
plt.scatter(taxi_data_cleaned['dropoff_community_area'], taxi_data_cleaned['pickup_community_area'], s=taxi_data_cleaned['trips'] * 0.001, alpha=0.5)
plt.title('Scatter Plot of Chicago Taxi Rides')
plt.ylabel('Pickup Community Area')
plt.xlabel('Dropoff Community Area')
plt.grid(True)







# Creating the matrix based on there being 77 Community Areas
num_com_areas = 77

traffic_matrix = coo_matrix((trips, (pickup - 1, dropoff - 1)), shape=(num_com_areas, num_com_areas))

traffic_matrix_dense = traffic_matrix.toarray()

beta_decay = 0.85  
num_iterations = 6 

# CReating the rank vector with equal probabilities to start
rank_vector = np.ones(num_com_areas) / num_com_areas

# Normalizing the original matrix to transfer it into the new one
row_sums = traffic_matrix_dense.sum(axis=1)
transition_matrix = np.divide(traffic_matrix_dense, row_sums[:, np.newaxis], where=row_sums[:, np.newaxis] != 0)

rank_vectors = [rank_vector]

# Iterate through 0-6 times
for _ in range(num_iterations):
    new_rank_vector = beta_decay * np.dot(rank_vector, transition_matrix) + (1 - beta_decay) / num_com_areas
    rank_vectors.append(new_rank_vector)
    rank_vector = new_rank_vector

# Transfer it into a dataframe to be able to view the ranks
rank_df = pd.DataFrame(rank_vectors, columns=[f'Area {i+1}' for i in range(num_com_areas)], index=[f'Iteration {i}' for i in range(num_iterations + 1)])
print(rank_df)








