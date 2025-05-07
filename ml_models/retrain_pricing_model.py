# ml_models/retrain_pricing_model.py
import pandas as pd
import os
import joblib
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

def retrain_pricing_model():
    csv_path = 'data/pricing_optimization.csv'
    model_path = 'ml_models/pricing_model.pkl'

    df = pd.read_csv(csv_path)
    df.rename(columns={
        'Product ID': 'product_id',
        'Store ID': 'store_id',
        'Price': 'price',
        'Competitor Prices': 'competitor_prices',
        'Discounts': 'discounts',
        'Sales Volume': 'sales_volume',
        'Customer Reviews': 'reviews',
        'Return Rate (%)': 'return_rate',
        'Storage Cost': 'storage_cost',
        'Elasticity Index': 'elasticity_index'
    }, inplace=True)

    required_columns = [
        'product_id', 'store_id', 'price', 'competitor_prices', 'discounts',
        'sales_volume', 'reviews', 'return_rate', 'storage_cost', 'elasticity_index'
    ]
    if not all(col in df.columns for col in required_columns):
        raise ValueError("Missing columns in dataset")

    X = df.drop(columns=['price', 'product_id', 'store_id'])
    y = df['price']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)

    os.makedirs(os.path.dirname(model_path), exist_ok=True)
    joblib.dump(model, model_path)

    return mse, model_path