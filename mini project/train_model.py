# ==========================================
# Urban Transport Ridership Forecasting
# Statistical Time Series Model (SARIMA)
# Compatible with Python 3.14
# ==========================================

# Install required libraries first:
# pip install pandas matplotlib scikit-learn statsmodels

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import mean_absolute_error, mean_squared_error
from statsmodels.tsa.statespace.sarimax import SARIMAX

# ------------------------------------------
# 1. Load Dataset
# ------------------------------------------

df = pd.read_csv("cta_ridership.csv")

print("Original Dataset Preview:")
print(df.head())

# ------------------------------------------
# 2. Clean Numeric Columns
# ------------------------------------------

df["bus"] = df["bus"].astype(str).str.replace(",", "")
df["rail_boardings"] = df["rail_boardings"].astype(str).str.replace(",", "")
df["total_rides"] = df["total_rides"].astype(str).str.replace(",", "")

df["bus"] = df["bus"].astype(float)
df["rail_boardings"] = df["rail_boardings"].astype(float)
df["total_rides"] = df["total_rides"].astype(float)

# ------------------------------------------
# 3. Convert Date Column
# ------------------------------------------

df["service_date"] = pd.to_datetime(df["service_date"], errors="coerce")

df = df.dropna(subset=["service_date"])

# ------------------------------------------
# 4. Prepare Time Series Data
# ------------------------------------------

df = df.sort_values("service_date")

df.set_index("service_date", inplace=True)

ridership = df["total_rides"]

print("\nCleaned Dataset:")
print(ridership.head())

# ------------------------------------------
# 5. Train SARIMA Model
# ------------------------------------------

print("\nTraining SARIMA model...")

model = SARIMAX(
    ridership,
    order=(1,1,1),
    seasonal_order=(1,1,1,7),
    enforce_stationarity=False,
    enforce_invertibility=False
)

results = model.fit()

print("\nModel training completed")

# ------------------------------------------
# 6. Forecast Future Ridership
# ------------------------------------------

forecast_steps = 365

forecast = results.forecast(steps=forecast_steps)

forecast_dates = pd.date_range(
    start=ridership.index[-1],
    periods=forecast_steps+1,
    freq="D"
)[1:]

forecast_series = pd.Series(forecast, index=forecast_dates)

print("\nForecast Preview:")
print(forecast_series.head())

# ------------------------------------------
# 7. Model Evaluation
# ------------------------------------------

train_pred = results.predict(start=0, end=len(ridership)-1)

mae = mean_absolute_error(ridership, train_pred)
rmse = np.sqrt(mean_squared_error(ridership, train_pred))

print("\nModel Evaluation")
print("MAE:", mae)
print("RMSE:", rmse)

# ------------------------------------------
# 8. Plot Historical + Forecast
# ------------------------------------------

plt.figure(figsize=(12,6))

plt.plot(ridership, label="Historical Ridership")

plt.plot(forecast_series, label="Forecast (Next 365 Days)")

plt.title("Urban Public Transport Ridership Forecast")

plt.xlabel("Date")

plt.ylabel("Ridership")

plt.legend()

plt.show()

# ------------------------------------------
# 9. Save Forecast Results
# ------------------------------------------

forecast_df = forecast_series.reset_index()

forecast_df.columns = ["date", "predicted_ridership"]

forecast_df.to_csv("ridership_forecast.csv", index=False)

print("\nForecast saved as ridership_forecast.csv")
