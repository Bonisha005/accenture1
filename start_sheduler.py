import schedule
import time
from agents.store_agent import run as run_store_agent
from agents.warehouse_agent import run as run_warehouse_agent
from agents.demand_forecaster import run as run_demand_forecaster
from agents.pricing_optimizer import run as run_pricing_optimizer
from agents.orchestrator_agent import run as run_orchestrator_agent

def run_all():
    print("Running all agents...")
    run_store_agent()
    run_warehouse_agent()
    run_demand_forecaster()
    run_pricing_optimizer()
    run_orchestrator_agent()
    print("All agents finished.")

# Schedule to run every hour (you can adjust to every X minutes)
schedule.every(1).hours.do(run_all)

if __name__ == "__main__":
    print("Starting agent scheduler...")
    run_all()  # Optional: Run immediately on start
    while True:
        schedule.run_pending()
        time.sleep(60)