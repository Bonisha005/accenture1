import sqlite3
import os

DB_DIR = "db"
DB_PATH = os.path.join(DB_DIR, "retail_agents.db")

def create_demand_predictions_table(conn):
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS demand_predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id TEXT NOT NULL,
            store_id TEXT NOT NULL,
            predicted_quantity INTEGER NOT NULL,
            timestamp TEXT NOT NULL
        )
    """)
    print("✅ demand_predictions table ensured.")

def create_model_versions_table(conn):
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS model_versions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            model_name TEXT NOT NULL,
            version TEXT NOT NULL,
            mse REAL,
            r_squared REAL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)
    print("✅ model_versions table ensured.")

def execute_schema_file(conn):
    script_dir = os.path.dirname(__file__)
    schema_path = os.path.join(script_dir, "schema.sql")

    if os.path.exists(schema_path):
        with open(schema_path, "r") as f:
            schema = f.read()
            conn.executescript(schema)
        print("✅ schema.sql executed successfully.")
    else:
        print("⚠ schema.sql not found, skipping.")

def init_db():
    os.makedirs(DB_DIR, exist_ok=True)  # Ensure the 'db' folder exists
    conn = sqlite3.connect(DB_PATH)
    create_demand_predictions_table(conn)
    create_model_versions_table(conn)
    execute_schema_file(conn)
    conn.commit()
    conn.close()
    print("✅ Database initialized at:", DB_PATH)

if __name__ == "__main__":
    init_db()