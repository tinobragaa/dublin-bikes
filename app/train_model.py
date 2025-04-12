import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import make_pipeline
from sklearn.compose import ColumnTransformer
import joblib

# Load the dataset
df = pd.read_csv("instance/sample_station_data.csv")  # Adjust path if needed

# Features and target
X = df[['station_id', 'day', 'hour']]
y = df['bikes_available']

# One-hot encode 'day'
categorical_features = ['day']
numeric_features = ['station_id', 'hour']

preprocessor = ColumnTransformer(
    transformers=[
        ('cat', OneHotEncoder(), categorical_features)
    ],
    remainder='passthrough'  # Keeps station_id and hour
)

# Create a pipeline with preprocessing + model
model = make_pipeline(preprocessor, LinearRegression())

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the model
model.fit(X_train, y_train)

# Save the model
joblib.dump(model, 'instance/bike_predictor.pkl')
print("✅ Model trained and saved as 'bike_predictor.pkl'")
