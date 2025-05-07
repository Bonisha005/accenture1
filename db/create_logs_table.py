import sqlite3

def create_logs_table():
    conn = sqlite3.connect("db/retail_agents.db")  # simplified path
    cursor = conn.cursor()

    cursor.execute("DROP TABLE IF EXISTS agent_logs")  # optional: to clean
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS agent_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        agent_name TEXT NOT NULL,
        action TEXT NOT NULL,
        status TEXT NOT NULL,
        message TEXT NOT NULL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()
    print("✅ agent_logs table created successfully!")

if __name__ == "__main__":
    create_logs_table()