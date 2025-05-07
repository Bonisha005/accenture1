import sqlite3

def cleanup_logs():
    conn = sqlite3.connect("retail_agents.db")
    cursor = conn.cursor()

    # Find logs where details column has 'SUCCESS' or 'FAILURE'
    cursor.execute("""
        SELECT id, details, status FROM agent_logs
        WHERE details IN ('SUCCESS', 'FAILURE')
    """)
    rows = cursor.fetchall()

    # Swap the values of details and status
    for row in rows:
        log_id, details, status = row
        print(f"Fixing log ID {log_id}: details='{details}', status='{status}'")
        cursor.execute("""
            UPDATE agent_logs
            SET details = ?, status = ?
            WHERE id = ?
        """, (status, details, log_id))

    conn.commit()
    conn.close()
    print("Log cleanup complete.")

if __name__ == "__main__":
    cleanup_logs()