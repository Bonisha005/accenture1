from agents.base_agent import BaseAgent
from db.db_utils import execute_query
from tools.memory_tool import save_memory, search_memory


class WarehouseAgent(BaseAgent):
    def __init__(self, warehouse_id="warehouse_1"):
        super().__init__(name=f"WarehouseAgent_{warehouse_id}")
        self.warehouse_id = warehouse_id

    def perceive(self):
        # Get all pending orders to be fulfilled
        query = """
        SELECT order_id, dest_id, product_id, qty
        FROM orders
        WHERE source_id = ? AND status = 'requested'
        """
        return execute_query(query, [self.warehouse_id])

    def check_stock(self, product_id):
        query = """
        SELECT stock_level FROM inventory
        WHERE store_id = ? AND product_id = ?
        """
        result = execute_query(query, [self.warehouse_id, product_id])
        return result[0][0] if result else 0

    def ship_order(self, order_id, product_id, qty, dest_id):
        # 1. Deduct from warehouse
        update_warehouse = """
        UPDATE inventory
        SET stock_level = stock_level - ?
        WHERE store_id = ? AND product_id = ?
        """
        execute_query(update_warehouse, [qty, self.warehouse_id, product_id])

        # 2. Add to destination store
        upsert_store = """
        INSERT INTO inventory (store_id, product_id, stock_level)
        VALUES (?, ?, ?)
        ON CONFLICT(store_id, product_id)
        DO UPDATE SET stock_level = stock_level + ?
        """
        execute_query(upsert_store, [dest_id, product_id, qty, qty])

        # 3. Mark order as shipped
        mark_shipped = """
        UPDATE orders SET status = 'shipped'
        WHERE order_id = ?
        """
        execute_query(mark_shipped, [order_id])

        # 4. Log it
        self.log("order_shipped", f"Order {order_id}: Shipped {qty} of {product_id} to {dest_id}")

    def act(self, orders):
        for order_id, dest_id, product_id, qty in orders:
            stock = self.check_stock(product_id)
            if stock >= qty:
                self.ship_order(order_id, product_id, qty, dest_id)
            else:
                self.log("insufficient_stock", f"Not enough {product_id} to ship order {order_id}")

    def run(self):
        requests = self.perceive()

        for request_id, product_id, qty in requests:
            available_qty = self.get_stock(product_id)

            note = f"Fulfilled request for {product_id} with {min(qty, available_qty)} units (requested {qty})"
            save_memory(self.name, note)

            similar = search_memory(self.name, note)
            self.log("memory_recall", f"Similar past fulfillments: {similar}")

            if available_qty >= qty:
                self.fulfill_request(request_id, qty)
            else:
                self.log("stock_warning", f"Not enough {product_id} in warehouse.")
def main():
    print("Running warehouse agent...")
    return "Warehouse agent finished"

def run():
    return main()

if __name__ == "__main__":
    main()