from tools.memory_tool import search_memory
from tools.llm_tool import call_ollama
from db.db_utils import execute_query
from datetime import datetime, timedelta

def get_recent_logs(limit=20):
    return execute_query(f"""
        SELECT agent_name, action, message, timestamp 
        FROM logs 
        ORDER BY timestamp DESC 
        LIMIT {limit}
    """)

def generate_chat_response(user_query: str):
    logs = get_recent_logs()
    recent_activity = "\n".join([f"[{l[3]}] {l[0]}: {l[1]} – {l[2]}" for l in logs])

    memories = search_memory("StoreAgent", user_query) \
             + search_memory("WarehouseAgent", user_query) \
             + search_memory("PricingOptimizer", user_query)

    memory_snippets = "\n".join([f"- {m}" for m in memories])

    context = f"""
You are an AI assistant for a retail company.

Recent system activity:
{recent_activity}

Relevant memories:
{memory_snippets}

User question: "{user_query}"
Answer with helpful, clear info using the context above. If uncertain, say so.
"""

    response = call_ollama(context)
    return response
