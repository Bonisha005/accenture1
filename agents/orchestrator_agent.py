from tools.memory_tool import save_memory
from tools.llm_tool import call_ollama
from agents.base_agent import BaseAgent
from agents.store_agent import StoreAgent
from agents.warehouse_agent import WarehouseAgent
from agents.demand_forecaster import DemandForecaster
from agents.pricing_optimizer import PricingOptimizer


class OrchestratorAgent(BaseAgent):
    def __init__(self):
        super().__init__(name="OrchestratorAgent")

    def decide_what_to_run(self):
        prompt = """
        You're an orchestrator for a retail AI system. 
        Agents: StoreAgent, WarehouseAgent, DemandForecaster, PricingOptimizer.
        Decide which should run right now and why. Output as a list like:

        RUN: [StoreAgent, PricingOptimizer]
        REASON: It's end of day, we should check inventory and optimize pricing.
        """
        response = call_ollama(prompt)
        return response

    def parse_decision(self, decision_text):
        try:
            lines = decision_text.strip().splitlines()
            run_line = next(line for line in lines if line.startswith("RUN"))
            reason_line = next(line for line in lines if line.startswith("REASON"))
            agents = run_line.split("[")[1].split("]")[0].replace(" ", "").split(",")
            reason = reason_line.split(":", 1)[1].strip()
            return agents, reason
        except Exception as e:
            self.log("error", f"Failed to parse LLM output: {decision_text}")
            return [], "default"

    def run(self):
        self.log("run_start", "Orchestrator thinking...")

        decision_text = self.decide_what_to_run()
        agents_to_run, reason = self.parse_decision(decision_text)

        self.log("llm_decision", f"Running: {agents_to_run} . {reason}")
        save_memory(self.name, f"Ran agents: {agents_to_run}. Reason: {reason}")

        for agent_name in agents_to_run:
            if agent_name == "StoreAgent":
                StoreAgent("store_1", "001").run()
            elif agent_name == "WarehouseAgent":
                WarehouseAgent().run()
            elif agent_name == "DemandForecaster":
                DemandForecaster().run()
            elif agent_name == "PricingOptimizer":
                PricingOptimizer("store_1").run()
            else:
                self.log("error", f"Unknown agent: {agent_name}")
def main():
    print("Running orchestrator agent...")
    return "Orchestrator agent finished"

def run():
    return main()

if __name__ == "__main__":
    main()