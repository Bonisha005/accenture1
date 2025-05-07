from agents.base_agent import BaseAgent
from db.db_utils import execute_query
from tools.memory_tool import save_memory, search_memory
import pandas as pd
from datetime import datetime, timedelta
from sklearn.linear_model import LinearRegression
import numpy as np


class DemandForecaster(BaseAgent):
    def __init__(self, store_id):
        super().__init__(name=f"DemandForecaster_{store_id}")
        self.store_id = store_id

    def get_sales_data(self):
        query = """
        SELECT product_id, sale_date, quantity
        FROM sales_history
        WHERE store_id = ?
        """
        return execute_query(query, [self.store_id])
    
    def get_all_products(self):
        query = """
        SELECT DISTINCT product_id FROM sales_history
        WHERE store_id = ?
        """
        results = execute_query(query, [self.store_id])
        return [row['product_id'] for row in results]

    def forecast(self, sales_df):
        forecasts = {}
        for product_id in sales_df['product_id'].unique():
            df = sales_df[sales_df['product_id'] == product_id].copy()
            df['sale_date'] = pd.to_datetime(df['sale_date'])
            df['day'] = (df['sale_date'] - df['sale_date'].min()).dt.days
            X = df[['day']]
            y = df['quantity']

            if len(X) >= 7:  # enough data
                model = LinearRegression()
                model.fit(X, y)
                next_day = pd.DataFrame({'day':[X['day'].max() +1]})
                forecast_qty = model.predict(next_day)[0]
                confidence = model.score(X, y)
                forecasts[product_id] = (int(max(forecast_qty, 0)), confidence)
        return forecasts

    def store_forecast(self, forecast_data):
        for product_id, (qty, confidence) in forecast_data.items():
            execute_query("""
            INSERT INTO demand_forecast (product_id, forecast_qty, timeframe, confidence)
            VALUES (?, ?, ?, ?)
            """, [product_id, qty, "1_day", confidence])
            self.log("forecast", f"{product_id} = {qty} units (conf: {confidence:.2f})")

    def run(self):
        sales_data = self.get_sales_data()
        sales_df = pd.DataFrame(sales_data, columns=["product_id", "sale_date", "quantity"])

        forecast_data = self.forecast(sales_df)

        for product_id, (forecast_qty, confidence) in forecast_data.items():
            note = f"Forecasted {forecast_qty} units for {product_id}"
            save_memory(self.name, note)

            similar = search_memory(self.name, note)
            self.log("memory_recall", f"Forecast memory for {product_id}: {similar}")

        self.store_forecast(forecast_data)
def main():
        print("Running demand forecaster agent....")
        return "Forecast agent finished"
def run():
        return main()
if __name__=="__main__":
        main()

    