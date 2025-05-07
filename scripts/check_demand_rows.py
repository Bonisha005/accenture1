import sqlite3

conn = sqlite3.connect("retail_agents.db")
cursor = conn.cursor()
cursor.execute("SELECT COUNT(*) FROM demand_forecasting")
count = cursor.fetchone()[0]
conn.close()

print(f"Total rows in demand_forecasting table: {count}")