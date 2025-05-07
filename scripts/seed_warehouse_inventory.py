from db.db_utils import execute_query
from datetime import datetime, timedelta
import random

store_id = "store_1"
products = ["item_101", "item_102", "item_103"]
start_date = datetime.today() - timedelta(days=30)

for day in range(30):
    date = start_date + timedelta(days=day)
    for product in products:
        qty = random.randint(2, 15)
        execute_query("""
        INSERT INTO sales_history (store_id, product_id, sale_date, quantity)
        VALUES (?, ?, ?, ?)
        """, [store_id, product, date.strftime("%Y-%m-%d"), qty])

print("✅ Sales history seeded.")
