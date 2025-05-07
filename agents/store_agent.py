from agents.base_agent import BaseAgent
from db.db_utils import execute_query
from tools.llm_tool import call_ollama
from tools.embedding_tool import get_embedding, cosine_similarity
import uuid
import json

LOW_STOCK_THRESHOLD = 10  # customizable per product/store

class StoreAgent(BaseAgent):
    def __init__(self, name, store_id):
        super().__init__(name=f"StoreAgent{store_id}")
        self.store_id = store_id
        self.name = name

    def perceive(self):
        query = """
        SELECT product_id, stock_level
        FROM inventory
        WHERE store_id = ?
        """
        return execute_query(query, [self.store_id])

    def reason(self, inventory_data):
        low_stock_items = []
        for product_id, stock_level in inventory_data:
            if stock_level < LOW_STOCK_THRESHOLD:
                low_stock_items.append((product_id, stock_level))
        return low_stock_items

    def act(self, low_stock_items):
        for product_id, stock_level in low_stock_items:
            qty_to_order = 50
            order_id = str(uuid.uuid4())
            query = """
            INSERT INTO orders (order_id, source_id, dest_id, product_id, qty, status)
            VALUES (?, ?, ?, ?, ?, ?)
            """
            execute_query(query, [
                order_id,
                "warehouse_1",
                self.store_id,
                product_id,
                qty_to_order,
                "requested"
            ])
            self.log("restock_request", f"Ordered {qty_to_order} of {product_id}")

    def run(self):
        self.log("run_start", f"Checking stock for {self.store_id}")
        stock = self.perceive()
        low_stock = [item for item in stock if item[1] < LOW_STOCK_THRESHOLD]

        if not low_stock:
            self.log("status", "All inventory levels are healthy.")
            return

        summary = "\n".join([f"{item[0]} has {item[1]} in stock" for item in low_stock])
        prompt = f"""You're a smart retail AI. These items are low in stock:\n{summary}\n
        What actions should the store take? Respond in brief."""

        reasoning = call_ollama(prompt)
        self.log("llm_plan", reasoning)

        for product_id, stock_level in low_stock:
            request_qty = 20 - stock_level
            self.request_inventory(product_id, request_qty)

    def find_similar_products(self, target_desc, threshold=0.85):
        target_vec = get_embedding(target_desc)

        query = "SELECT product_id, embedding FROM product_embeddings"
        results = execute_query(query)

        similarities = []
        for pid, emb_json in results:
            emb = json.loads(emb_json)
            sim = cosine_similarity(target_vec, emb)
            if sim > threshold:
                similarities.append((pid, sim))

        return sorted(similarities, key=lambda x: -x[1])
        

def main():
        print("Running store agent....")
        return "Store agent finished"
def run():
        return main()
if __name__=="__main__":
        print("Running store agent....")

    