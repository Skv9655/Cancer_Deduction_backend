from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pickle
import pandas as pd
import numpy as np
import os
import json

app = FastAPI(title="Cancer Deduction API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load Model
MODEL_PATH = os.path.join(os.path.dirname(__file__), "XGBoost.pkl")
MEANS_PATH = os.path.join(os.path.dirname(__file__), "feature_means.json")

try:
    with open(MODEL_PATH, "rb") as f:
        model = pickle.load(f)
        
    with open(MEANS_PATH, "r") as f:
        feature_means = json.load(f)
        
    # Extract feature names expected by the model
    expected_features = model.feature_names_in_
except Exception as e:
    print(f"Error loading model or means: {e}")
    model = None
    feature_means = {}
    expected_features = []

class CancerFeatures(BaseModel):
    perimeter_worst: float
    perimeter_mean: float
    radius_worst: float
    concave_points_mean: float
    concave_points_worst: float
    radius_mean: float
    texture_worst: float
    area_worst: float
    area_mean: float
    concavity_worst: float
    compactness_worst: float
    smoothness_worst: float
    compactness_se: float
    area_se: float
    texture_mean: float

@app.post("/predict")
def predict(features: CancerFeatures):
    if not model:
        raise HTTPException(status_code=500, detail="Model not loaded")
        
    # Map pydantic fields back to original feature names
    input_data = {
        "perimeter_worst": features.perimeter_worst,
        "perimeter_mean": features.perimeter_mean,
        "radius_worst": features.radius_worst,
        "concave points_mean": features.concave_points_mean,
        "concave points_worst": features.concave_points_worst,
        "radius_mean": features.radius_mean,
        "texture_worst": features.texture_worst,
        "area_worst": features.area_worst,
        "area_mean": features.area_mean,
        "concavity_worst": features.concavity_worst,
        "compactness_worst": features.compactness_worst,
        "smoothness_worst": features.smoothness_worst,
        "compactness_se": features.compactness_se,
        "area_se": features.area_se,
        "texture_mean": features.texture_mean
    }
    
    # Fill missing features with their means
    full_features = {}
    for feature in expected_features:
        if feature in input_data:
            full_features[feature] = input_data[feature]
        else:
            full_features[feature] = feature_means.get(feature, 0.0)
            
    # Convert to DataFrame in the exact order expected
    df = pd.DataFrame([full_features])[expected_features]
    
    prediction = model.predict(df)[0]
    
    # Check if predict_proba is available
    probability = None
    if hasattr(model, "predict_proba"):
        prob_array = model.predict_proba(df)[0]
        probability = float(prob_array[prediction])
        
    result = "Malignant" if prediction == 1 else "Benign"
    
    return {
        "prediction": result,
        "prediction_code": int(prediction),
        "probability": probability
    }

@app.get("/")
def home():
    return {
        "status": "running",
        "message": "Cancer Prediction API is live"
    }

@app.get("/health")
def health():
    return {"status": "healthy"}
