import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from db.db_utils import execute_query

base_prices = {
    "item_101": 80.0,
    "item_102": 120.0,
    "item_103": 60.0,
}

for product_id, price in base_prices.items():
    execute_query("""
    INSERT OR IGNORE INTO pricing (product_id, current_price, suggested_price, last_updated)
    VALUES (?, ?, ?, datetime('now'))
    """, [product_id, price, price])

print("✅ Initial prices seeded.")
