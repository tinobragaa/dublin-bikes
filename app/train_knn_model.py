import pandas as pd
import numpy as np
from sklearn.neighbors import NearestNeighbors
import joblib

# Load station data from CSV
df = pd.read_csv("instance/stations_data.csv")

# Check for missing values in the 'lat' and 'lng' columns
print("Missing values in 'lat' and 'lng':")
print(df[['lat', 'lng']].isnull().sum())

# Drop rows where lat or lng is NaN
df.dropna(subset=['lat', 'lng'], inplace=True)

# Extract the coordinates and convert them into radians
coords = df[['lat', 'lng']].values
coords_rad = np.radians(coords)

# Initialize and train the Nearest Neighbors model using the haversine metric
knn_model = NearestNeighbors(n_neighbors=5, metric='haversine')
knn_model.fit(coords_rad)

# Save the trained model to a file
joblib.dump(knn_model, "instance/stations_knn_model.pkl")
print("✅ KNN model trained and saved as 'stations_knn_model.pkl'")
