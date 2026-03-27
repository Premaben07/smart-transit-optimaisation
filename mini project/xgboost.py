import pandas as pd
import xgboost as xgb
import matplotlib.pyplot as plt

def train_xgboost(X_train, y_train):
    """Initializes and trains the XGBoost Regressor model."""
    model = xgb.XGBRegressor(
        n_estimators=100,
        learning_rate=0.1,
        random_state=42,
        tree_method='hist' # For faster training
    )
    model.fit(X_train, y_train)
    return model

def main():
    print("1. Loading data...")
    # Make sure 'cta_ridership.csv' is in the same folder as this script
    df = pd.read_csv('cta_ridership.csv')

    print("2. Preprocessing data...")
    # Clean commas from 'total_rides' and convert to float/int
    if df['total_rides'].dtype == 'object':
        df['total_rides'] = df['total_rides'].str.replace(',', '').astype(float)
    
    # Convert date column to datetime
    df['service_date'] = pd.to_datetime(df['service_date'], format='mixed')
    
    # Select relevant columns, set index, and sort
    df = df[['service_date', 'total_rides']].copy()
    df.set_index('service_date', inplace=True)
    df.sort_index(inplace=True)

    print("3. Feature Engineering...")
    # Extract features from the index (service_date)
    df['year'] = df.index.year
    df['month'] = df.index.month
    df['day'] = df.index.day
    df['dayofweek'] = df.index.dayofweek
    df['dayofyear'] = df.index.dayofyear
    df['weekofyear'] = df.index.isocalendar().week.astype(int)

    # Define features (X) and target (y)
    features = ['year', 'month', 'day', 'dayofweek', 'dayofyear', 'weekofyear']
    X = df[features]
    y = df['total_rides']

    print("4. Training XGBoost model...")
    model = train_xgboost(X, y)
    print("Model trained successfully!")

    print("5. Generating 30-day forecast...")
    # Generate future dates (30 days into the future, starting the day after the last date)
    last_date = df.index[-1]
    future_dates = pd.date_range(start=last_date + pd.Timedelta(days=1), periods=30)
    
    # Create future dataframe and engineer the exact same features
    future = pd.DataFrame(index=future_dates)
    future['year'] = future.index.year
    future['month'] = future.index.month
    future['day'] = future.index.day
    future['dayofweek'] = future.index.dayofweek
    future['dayofyear'] = future.index.dayofyear
    future['weekofyear'] = future.index.isocalendar().week.astype(int)
    
    # Predict
    X_future = future[features]
    predictions = model.predict(X_future)

    # Save predictions to CSV
    forecast = pd.DataFrame({'predicted_rides': predictions}, index=future_dates)
    forecast.index.name = 'service_date'
    forecast.to_csv("predictions.csv")
    print("-> Predictions saved to your folder as 'predictions.csv'")

    print("6. Visualizing results...")
    plt.figure(figsize=(12, 6))
    
    # Plotting only the last 365 days of actual data so the 30-day forecast is easy to see
    plt.plot(df.index[-365:], df["total_rides"].iloc[-365:], label="Actual Rides (Last 365 days)", color='blue')
    plt.plot(future_dates, predictions, label="Forecast (Next 30 days)", color='orange', linestyle='--')
    
    plt.legend()
    plt.title("XGBoost Transit Ridership Forecast")
    plt.xlabel("Date")
    plt.ylabel("Total Rides")
    plt.tight_layout()
    
    # Save the plot as an image in your folder
    plt.savefig("xgboost_forecast.png")
    print("-> Chart saved to your folder as 'xgboost_forecast.png'")
    
    # Show the plot in a pop-up window
    plt.show()

if __name__ == "__main__":
    main()