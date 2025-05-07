import sqlite3
from datetime import datetime

def insert_log(agent_name, action, status, message):
    conn = sqlite3.connect('db/retail_agents.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO agent_logs (agent_name, action, status, details, timestamp)
        VALUES (?, ?, ?, ?, ?)
    """, (agent_name, action, status, message, datetime.now()))

    conn.commit()
    conn.close()