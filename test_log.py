from db.db_utils import execute_query
from db.logger import insert_log

# Log test entries
insert_log("DemandForecaster", "forecast_demand", "SUCCESS", "Forecasting complete")
insert_log("PricingOptimizer", "optimize_prices", "FAILURE", "Price data missing")
insert_log("StoreAgent", "test_action", "SUCCESS", "Test message from test_log.py")

print("Log inserted successfully.")

# Display logs
logs = execute_query("SELECT * FROM agent_logs")
for log in logs:
    print(dict(log))