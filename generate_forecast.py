import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import numpy as np
import os

def generate_forecast(csv_path="data/Sample_Superstore.csv", output_path="data/forecast.csv"):
    # Load the dataset
    df = pd.read_csv(csv_path)

    # Convert 'Order Date' to datetime
    df['Order Date'] = pd.to_datetime(df['Order Date'], errors='coerce')

    # Drop rows where Order Date or Sales is missing
    df = df.dropna(subset=['Order Date', 'Sales'])

    # Group by date and sum sales
    daily_sales = df.groupby('Order Date')['Sales'].sum().reset_index()
    daily_sales = daily_sales.sort_values('Order Date')

    # Convert dates to ordinal for regression
    daily_sales['DateOrdinal'] = daily_sales['Order Date'].map(pd.Timestamp.toordinal)

    # Train/Test Split
    X = daily_sales[['DateOrdinal']]
    y = daily_sales['Sales']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)

    # Model training
    model = LinearRegression()
    model.fit(X_train, y_train)

    # Forecast next 30 days
    last_date = daily_sales['Order Date'].max()
    future_dates = pd.date_range(start=last_date + pd.Timedelta(days=1), periods=30)
    future_ordinals = future_dates.map(pd.Timestamp.toordinal).values.reshape(-1, 1)
    future_sales = model.predict(future_ordinals)

    # Prepare forecast DataFrame
    forecast_df = pd.DataFrame({
        "Date": future_dates,
        "Predicted_Sales": future_sales.round(2)
    })

    # Save to CSV
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    forecast_df.to_csv(output_path, index=False)

    return forecast_df
