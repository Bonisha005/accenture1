import sqlite3


DB_PATH = "db/retail_agents.db"

def get_connection():
    conn = sqlite3.connect('db/retail_agents.db')
    conn.row_factory = sqlite3.Row
    return conn


def execute_query(query, params=None):
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(query, params or [])
    conn.commit()
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def insert_log(agent_name, action, details):
    query = """
    INSERT INTO agent_logs (agent_name, action, details)
    VALUES (?, ?, ?)
    """
    execute_query(query, [agent_name, action, details])

def execute_non_query(query, params=None):
    conn = sqlite3.connect("db/retail_agents.db")
    cursor = conn.cursor()
    if params:
        cursor.execute(query, params)
    else:
        cursor.execute(query)
    conn.commit()
    conn.close()

if __name__== "__main__":
    insert_log("StoreAgent", "restock_request", "Requested 20 units of item_123")
    