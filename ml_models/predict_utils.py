import pandas as pd
from db.db_utils import get_connection

def prepare_demand_features(product_id, store_id):
    conn = get_connection()
    query = """
        SELECT "Price", "Promotions", "Seasonality Encoded", "External Factors", "Demand Trend"
        FROM demand_forecasting
        WHERE "Product ID" = ? AND "Store ID" = ?
        ORDER BY date DESC LIMIT 1
    """
    row = conn.execute(query, (product_id, store_id)).fetchone()
    conn.close()

    if not row:
        row_dict = {
            "Price": 50,
            "Promotions": 1,
            "Seasonality Encoded": 0,
            "External Factors": 0,
            "Demand Trend": 1
        }
    else:
        row_dict = {
            "Price": row[0],
            "Promotions": row[1],
            "Seasonality Encoded": row[2],
            "External Factors": row[3],
            "Demand Trend": row[4]
        }

    return pd.DataFrame([row_dict])


def prepare_pricing_features(product_id, store_id):
    conn = get_connection()
    query = """
        SELECT "Price", "Competitor Prices", "Discounts", "Sales Volume", "Elasticity Index", 
               "Reviews", "Return Rate", "Storage Cost"
        FROM pricing_optimization
        WHERE "Product ID" = ? AND "Store ID" = ?
        ORDER BY ROWID DESC LIMIT 1
    """
    row = conn.execute(query, (product_id, store_id)).fetchone()
    conn.close()

    if not row:
        row_dict = {
            "Price": 50,
            "Competitor Prices": 50,
            "Discounts": 0,
            "Sales Volume": 100,
            "Elasticity Index": 1.0,
            "Reviews": 4.0,
            "Return Rate": 0.05,
            "Storage Cost": 2.0
        }
    else:
        row_dict = {
            "Price": row[0],
            "Competitor Prices": row[1],
            "Discounts": row[2],
            "Sales Volume": row[3],
            "Elasticity Index": row[4],
            "Reviews": row[5],
            "Return Rate": row[6],
            "Storage Cost": row[7]
        }

    return pd.DataFrame([row_dict])


def prepare_inventory_features(product_id, store_id):
    conn = get_connection()
    query = """
        SELECT 
            [Stock Levels], 
            [Supplier Lead Time (days)], 
            [Stockout Frequency], 
            [Reorder Point], 
            [Order Fulfillment Time (days)]
        FROM inventory_monitoring
        WHERE [Product ID] = ? AND [Store ID] = ?
        ORDER BY ROWID DESC LIMIT 1
    """
    row = conn.execute(query, (product_id, store_id)).fetchone()
    conn.close()

    if not row:
        row_dict = {
            "Stock Levels": 100,
            "Supplier Lead Time (days)": 3,
            "Stockout Frequency": 0.1,
            "Reorder Point": 20,
            "Order Fulfillment Time (days)": 2
        }
    else:
        row_dict = {
            "Stock Levels": row[0],
            "Supplier Lead Time (days)": row[1],
            "Stockout Frequency": row[2],
            "Reorder Point": row[3],
            "Order Fulfillment Time (days)": row[4]
        }

    return pd.DataFrame([row_dict])