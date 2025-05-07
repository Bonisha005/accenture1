from apscheduler.schedulers.background import BackgroundScheduler
from agents.store_agent import run as run_store_agent
from agents.warehouse_agent import run as run_warehouse_agent
from agents.demand_forecaster import run as run_demand_forecaster
from agents.pricing_optimizer import run as run_pricing_optimizer
from agents.orchestrator_agent import run as run_orchestrator_agent
from api_main import auto_run_status
from state import auto_run_status

def conditional_wrapper(func, agent_name):
    def wrapper():
        if auto_run_status["enabled"]:
            func()
        else:
            print(f"Auto-run disabled: {agent_name}")
    return wrapper

def start_scheduler():
    scheduler = BackgroundScheduler()

    scheduler.add_job(run_store_agent, 'interval', minutes=10, id='store_agent')
    scheduler.add_job(run_warehouse_agent, 'interval', minutes=15, id='warehouse_agent')
    scheduler.add_job(run_demand_forecaster, 'interval', minutes=5, id='forecast_agent')
    scheduler.add_job(run_pricing_optimizer, 'interval', minutes=5, id='pricing_agent')
    scheduler.add_job(run_orchestrator_agent, 'interval', minutes=30, id='orchestrator_agent')

    scheduler.start()
    print("Scheduler started with all agent jobs.")