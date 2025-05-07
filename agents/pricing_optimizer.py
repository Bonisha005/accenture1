from agents.base_agent import BaseAgent
from db.db_utils import execute_query
from tools.embedding_tool import cosine_similarity
from tools.memory_tool import save_memory, search_memory
import json
from datetime import datetime

class PricingOptimizer(BaseAgent):
    def __init__(self, store_id):
        self.store_id = store_id
        super().__init__(name=f"PricingOptimizer_{store_id}")

    def get_inventory(self):
        return execute_query("""
        SELECT product_id, stock_level
        FROM inventory
        WHERE store_id = ?
        """, [self.store_id])

    def get_forecast(self):
        data = execute_query("""
        SELECT product_id, forecast_qty
        FROM demand_forecast
        """)
        return {pid: qty for pid, qty in data}

    def get_current_prices(self):
        data = execute_query("""
        SELECT product_id, current_price
        FROM pricing
        """)
        return {pid: price for pid, price in data}

    def optimize_price(self, product_id, stock, forecast, current_price):
        try:
            stock = float(stock)
            forecast = float(forecast)
            current_price = float(current_price)
        except ValueError:
            self.log("error", f"Invalid number format for product {product_id}")
            return current_price  # fallback to current price

        if forecast == 0:
            return current_price  # avoid division by zero

        stock_to_demand_ratio = stock / forecast

        # Example pricing logic
        if stock_to_demand_ratio > 2:
            new_price = current_price * 0.95  # slight discount
        elif stock_to_demand_ratio < 0.5:
            new_price = current_price * 1.10  # price hike for low stock
        else:
            new_price = current_price

        return round(new_price, 2)

    def store_price(self, product_id, price):
        execute_query("""
        INSERT INTO pricing (product_id, current_price, suggested_price, last_updated)
        VALUES (?, ?, ?, ?)
        ON CONFLICT(product_id) DO UPDATE
        SET suggested_price = excluded.suggested_price,
            last_updated = excluded.last_updated
        """, [product_id, price, price, datetime.now().isoformat()])

    def run(self):
        self.log("run_start", f"Optimizing prices for {self.store_id}")

        inventory = self.get_inventory()
        forecast = self.get_forecast()
        prices = self.get_current_prices()

        for product_id, stock_level in inventory:
            forecast_qty = forecast.get(product_id, 0)
            current_price = prices.get(product_id, 100.0)

            new_price = self.optimize_price(product_id, stock_level, forecast_qty, current_price)

            note = f"Price change for {product_id}: {current_price} → {new_price}"
            save_memory(self.name, note)

            similar = search_memory(self.name, note)
            self.log("memory_recall", f"Similar past price changes: {similar}")

            self.store_price(product_id, new_price)

def main():
    print("Running pricing agent...")
    return "Pricing agent finished"

def run():
    return main()

if __name__ == "__main__":
    main()