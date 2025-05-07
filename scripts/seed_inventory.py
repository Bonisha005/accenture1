import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from db.db_utils import execute_query

# Sample data: store_1 has low stock on item_101
sample_data = [
    ("store_1", "item_101", 5),
    ("store_1", "item_102", 15),
    ("store_1", "item_103", 8),
]

for store_id, product_id, stock_level in sample_data:
    query = """
    INSERT INTO inventory (store_id, product_id, stock_level)
    VALUES (?, ?, ?)
    """
    execute_query(query, [store_id, product_id, stock_level])

print("✅ Inventory seeded.")
