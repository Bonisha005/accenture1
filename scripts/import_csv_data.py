import pandas as pd
import sqlite3

# Paths to your CSV files
demand_path = "data/demand_forecasting.csv"
inventory_path = "data/inventory_monitoring.csv"
pricing_path = "data/pricing_optimization.csv"

# Read the CSVs
df_demand = pd.read_csv(demand_path)
df_inventory = pd.read_csv(inventory_path)
df_pricing = pd.read_csv(pricing_path)

# Connect to SQLite DB
conn = sqlite3.connect("retail_agents.db")

# Insert data into tables
df_demand.to_sql("demand_forecasting", conn, if_exists="replace", index=False)
df_inventory.to_sql("inventory_monitoring", conn, if_exists="replace", index=False)
df_pricing.to_sql("pricing_optimization", conn, if_exists="replace", index=False)

print("Data imported successfully.")
conn.close()