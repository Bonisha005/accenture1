import pandas as pd
import sqlite3
import os

UPLOAD_FOLDER = "uploads"
DB_PATH = "retail_agents.db"

def load_csv_to_db(filename, table_name):
    path = os.path.join(UPLOAD_FOLDER, filename)
    df = pd.read_csv(path)
    conn = sqlite3.connect(DB_PATH)
    df.to_sql(table_name, conn, if_exists="replace", index=False)
    conn.close()
    print(f"Loaded {filename} into {table_name}.")

if __name__ == "__main__":
    load_csv_to_db("demand_forecasting.csv", "demand_forecasting")
    load_csv_to_db("inventory_monitoring.csv", "inventory_monitoring")
    load_csv_to_db("pricing_optimization.csv", "pricing_optimization")