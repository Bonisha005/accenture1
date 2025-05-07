import pandas as pd
import os
import joblib
import pickle
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import mean_squared_error, r2_score

# ===== PRICING MODEL TRAINING =====
print("\n=== Training Pricing Model ===")
pricing_path = '../data/pricing_optimization.csv'
df_pricing = pd.read_csv(pricing_path)

# Rename columns for consistency
df_pricing.rename(columns={
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

required_pricing_cols = [
    'product_id', 'store_id', 'price', 'competitor_prices', 'discounts',
    'sales_volume', 'reviews', 'return_rate', 'storage_cost', 'elasticity_index'
]

missing = [col for col in required_pricing_cols if col not in df_pricing.columns]
if missing:
    raise ValueError(f"Missing pricing columns: {missing}")

# Features and target
X_pricing = df_pricing.drop(columns=['price', 'product_id', 'store_id'])
y_pricing = df_pricing['price']

# Scale features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X_pricing)

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y_pricing, test_size=0.2, random_state=42)

# Train model
pricing_model = RandomForestRegressor(n_estimators=100, random_state=42)
pricing_model.fit(X_train, y_train)

# Evaluate
y_pred = pricing_model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)
print(f"Pricing Model MSE: {mse:.2f} | R²: {r2:.4f}")

# Save model and scaler
os.makedirs('../ml_models', exist_ok=True)
joblib.dump(pricing_model, '../ml_models/pricing_model.pkl')
joblib.dump(scaler, '../ml_models/pricing_scaler.pkl')
print("Pricing model + scaler saved.")

# ===== DEMAND FORECASTING MODEL TRAINING =====
print("\n=== Training Demand Forecasting Model ===")
demand_path = '../data/demand_forecasting.csv'
df_demand = pd.read_csv(demand_path)

# Rename columns for consistency
df_demand.rename(columns={
    'Product ID': 'product_id',
    'Date': 'date',
    'Store ID': 'store_id',
    'Sales Quantity': 'sales_quantity',
    'Price': 'price',
    'Promotions': 'promotions',
    'Seasonality Factors': 'seasonality',
    'External Factors': 'external_factors',
    'Demand Trend': 'trend',
    'Customer Segments': 'customer_segment'
}, inplace=True)

required_demand_cols = [
    'product_id', 'date', 'store_id', 'sales_quantity', 'price',
    'promotions', 'seasonality', 'external_factors', 'trend', 'customer_segment'
]

missing = [col for col in required_demand_cols if col not in df_demand.columns]
if missing:
    raise ValueError(f"Missing demand columns: {missing}")

# Clean and encode
df_demand['promotions'] = df_demand['promotions'].str.strip().str.lower().map({'yes': 1, 'no': 0})
df_demand['trend'] = df_demand['trend'].str.strip().str.lower().map({'increasing': 1, 'stable': 0, 'decreasing': -1})
df_demand.dropna(subset=['price', 'promotions', 'seasonality', 'trend', 'sales_quantity'], inplace=True)

# Encode seasonality
le = LabelEncoder()
df_demand['seasonality_encoded'] = le.fit_transform(df_demand['seasonality'])

# Final features
X_demand = df_demand[['price', 'promotions', 'seasonality_encoded', 'trend']]
y_demand = df_demand['sales_quantity']

print(f"Final rows used for training demand model: {len(X_demand)}")

# Train/test split
X_train_d, X_test_d, y_train_d, y_test_d = train_test_split(X_demand, y_demand, test_size=0.2, random_state=42)

# Train model
demand_model = LinearRegression()
demand_model.fit(X_train_d, y_train_d)

# Evaluate
y_pred_d = demand_model.predict(X_test_d)
mse_d = mean_squared_error(y_test_d, y_pred_d)
r2_d = r2_score(y_test_d, y_pred_d)
print(f"Demand Forecasting MSE: {mse_d:.2f} | R²: {r2_d:.4f}")

# Save model
with open('../ml_models/demand_model.pkl', 'wb') as f:
    pickle.dump(demand_model, f)
print("Demand model saved.")

import os
import pandas as pd
import joblib
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

# --------- Inventory Model Training ---------
csv_inventory_path = '../data/inventory_monitoring.csv'
df_inventory = pd.read_csv(csv_inventory_path)

# Rename columns for consistency
df_inventory.rename(columns={
    'Product ID': 'product_id',
    'Store ID': 'store_id',
    'Stock Levels': 'stock_levels',
    'Supplier Lead Time (days)': 'lead_time',
    'Stockout Frequency': 'stockout_freq',
    'Reorder Point': 'reorder_point',
    'Expiry Date': 'expiry_date',
    'Warehouse Capacity': 'warehouse_cap',
    'Order Fulfillment Time (days)': 'fulfillment_time'
}, inplace=True)

# Convert date to numeric (optional: days until expiry)
df_inventory['days_until_expiry'] = pd.to_datetime(df_inventory['expiry_date'], errors='coerce') - pd.Timestamp.today()
df_inventory['days_until_expiry'] = df_inventory['days_until_expiry'].dt.days
df_inventory.drop(columns=['expiry_date'], inplace=True)

# Drop rows with missing values
df_inventory.dropna(inplace=True)

# Features and target
X = df_inventory[['lead_time', 'stockout_freq', 'reorder_point', 'warehouse_cap', 'fulfillment_time', 'days_until_expiry']]
y = df_inventory['stock_levels']

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the model
model_inventory = LinearRegression()
model_inventory.fit(X_train, y_train)

# Evaluate model
y_pred_inventory = model_inventory.predict(X_test)
inventory_mse = mean_squared_error(y_test, y_pred_inventory)
print(f"Inventory Model trained. Test MSE: {inventory_mse:.2f}")

# Save the model
os.makedirs('ml_models', exist_ok=True)
joblib.dump(model_inventory, 'ml_models/inventory_model.pkl')
print("Inventory Model saved to ml_models/inventory_model.pkl")