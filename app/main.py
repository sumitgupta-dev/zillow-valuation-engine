from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import numpy as np
import joblib
from knn_engine import find_similar_houses

# ---------------------------------------------------------
# 1. LOAD EVERYTHING GLOBALLY (When server starts)
# ---------------------------------------------------------
print("Loading ML Model and Scaler...")
model = joblib.load('../models/house_price_model.pkl')
scaler = joblib.load('../models/scaler.pkl')

# Load the database of houses to search through for KNN
print("Loading House Database...")
df_db = pd.read_csv('../data/kc_house_data.csv')

# For the KNN, we only want to use a few core features to calculate "distance"
# Make sure these columns match exactly how you will scale the user input!
knn_features = [
    'sqft_living', 'bedrooms', 'bathrooms', 'floors', 
    'waterfront', 'view', 'condition', 'grade', 'yr_built',
    'lat', 'long'
]
db_features_raw = df_db[knn_features]

# Scale the database features ONCE when the server starts
db_features_scaled = scaler.transform(db_features_raw)
print("Everything loaded!")

# ---------------------------------------------------------
# 2. SETUP FASTAPI
# ---------------------------------------------------------
app = FastAPI()

class HouseInput(BaseModel):
    sqft_living: int
    bedrooms: int
    bathrooms: float

# ---------------------------------------------------------
# 3. THE PREDICTION ENDPOINT
# ---------------------------------------------------------
@app.post("/predict")
def predict_house(data: HouseInput):
    # 1. Auto-fill the missing features with smart defaults!
    waterfront = 0       # Assume no waterfront
    view = 0             # Assume average view
    condition = 3        # Assume average condition
    grade = 7            # Assume average construction grade
    yr_built = 1990      # Assume average age
    # Inside your predict_house function:
    lat = 47.6
    long = -122.3

    # 2. Combine user input with your auto-filled defaults
    user_input_raw = np.array([[
        data.sqft_living, data.bedrooms, data.bathrooms, 1.0, # 1.0 is floors default
        waterfront, view, condition, grade, yr_built,
        lat, long
    ]])
    
    
    # 2. Scale the user input using the SAME scaler
    user_input_scaled = scaler.transform(user_input_raw)
    
    # 3. Predict the price! 
    # (We use the same core features for the model prediction)
    predicted_price = model.predict(user_input_scaled)[0]
    
    # 4. Run your custom DSA KNN Algorithm!
    comparable_houses = find_similar_houses(
        user_input_scaled[0], 
        db_features_scaled, 
        df_db, 
        k=3
    )
    
    # 5. Return the final JSON response
    return {
        "predicted_price": round(predicted_price, 2),
        "comparable_houses": comparable_houses
    }