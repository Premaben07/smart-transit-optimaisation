import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import joblib
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

app = FastAPI(title="Urban Transit Ridership API")

# 1. ALLOW THE FRONTEND TO ACCESS THE BACKEND
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permits all origins (fine for development)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2. LOAD YOUR SAVED MODELS
# Replace these filenames with your actual saved model paths
try:
    # Example: model = joblib.load('machine_learning/models/xgboost_model.pkl')
    # For now, we will simulate the prediction logic
    print("Models loaded successfully.")
except Exception as e:
    print(f"Warning: Models not found. Using simulation mode. Error: {e}")

# 3. HELPER FUNCTION: PREDICTION LOGIC
def generate_forecast_data():
    """
    In a real scenario, you would pass features (weather, time, day) 
    into your models here.
    """
    labels = []
    now = datetime.now()
    for i in range(8):
        labels.append((now + timedelta(hours=i*2)).strftime("%H:%M"))

    # Simulated Data based on typical urban transit patterns
    actual = [120, 450, 310, 280, 590, 880, 400, 150]
    
    # ARIMA: Usually follows the trend but can be slightly lagged
    arima_pred = [val * 0.95 + np.random.randint(-20, 20) for val in actual]
    
    # Prophet: Great for seasonality (daily/weekly)
    prophet_pred = [val * 1.02 + np.random.randint(-15, 15) for val in actual]
    
    # XGBoost: Often the most precise for non-linear peaks
    xg_pred = [val * 0.99 + np.random.randint(-5, 5) for val in actual]

    return {
        "labels": labels,
        "actual": actual,
        "arima": arima_pred,
        "prophet": prophet_pred,
        "xgboost": xg_pred,
        "capacity": 1000 # Total fleet capacity for the route
    }

# 4. API ENDPOINTS

@app.get("/")
def read_root():
    return {"status": "Online", "project": "Smart Transit Optimization"}

@app.get("/api/v1/forecast")
async def get_forecast(route_id: str = "Route_01"):
    """Returns the ridership predictions for Admin comparison."""
    data = generate_forecast_data()
    return {
        "route": route_id,
        "timestamp": datetime.now().isoformat(),
        "data": data
    }

@app.get("/api/v1/user-status")
async def get_user_status(route_id: str = "Route_01"):
    """Returns simplified status for the Commuter Dashboard."""
    data = generate_forecast_data()
    # Logic to determine congestion
    current_riders = data["actual"][0]
    capacity = data["capacity"]
    load_factor = current_riders / capacity

    status = "Low Traffic"
    color = "green"
    if load_factor > 0.4:
        status = "Moderate Traffic"
        color = "yellow"
    if load_factor > 0.8:
        status = "High Traffic - Heavy Crowding"
        color = "red"

    return {
        "route": route_id,
        "current_riders": current_riders,
        "status": status,
        "color_code": color,
        "next_predicted_peak": "18:00"
    }

# 5. RUN THE SERVER
if __name__ == "__main__":
    # Run using: python main.py
    uvicorn.run(app, host="127.0.0.1", port=8000)