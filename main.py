from agents.base_agent import BaseAgent
from agents.store_agent import StoreAgent
from agents.warehouse_agent import WarehouseAgent
from agents.demand_forecaster import DemandForecaster
from agents.pricing_optimizer import PricingOptimizer
from agents.orchestrator_agent import OrchestratorAgent

# Log test
print("📝 Logging test with BaseAgent...")
test_agent = BaseAgent("TestAgent")
test_agent.log("test_action", "This is a log test.")
print("✅ Log written successfully.\n")

# StoreAgent
print("🚀 Running StoreAgent...")
store_agent = StoreAgent("StoreAgent1", store_id=1)
store_agent.run()
print("✅ StoreAgent run complete.\n")

# WarehouseAgent
print("🚚 Running WarehouseAgent...")
warehouse_agent = WarehouseAgent()
warehouse_agent.run()
print("✅ WarehouseAgent run complete.\n")

# Demand Forecaster
print("📈 Running DemandForecaster...")
forecaster = DemandForecaster("store_1")
forecaster.run()
print("✅ DemandForecaster run complete.\n")

# Pricing Optimizer
print("💰 Running PricingOptimizer...")
optimizer = PricingOptimizer(store_id="store_1")
optimizer.run()
print("✅ PricingOptimizer run complete.\n")

# Orchestrator
print("🤖 Running OrchestratorAgent...")
orch = OrchestratorAgent()
orch.run()
print("✅ OrchestratorAgent run complete.\n")

print("🎉 All agents executed successfully.")
