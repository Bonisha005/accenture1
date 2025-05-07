from db.logger import insert_log  # Now safely imported from refactored module

class BaseAgent:
    def __init__(self, name):
        self.name = name

    def perceive(self, context):
        pass

    def reason(self, prompt):
        pass

    def act(self, action_plan):
        pass

    def log(self, action, message, status="INFO"):
        from db.logger import insert_log
        insert_log(self.name, action, status, message)