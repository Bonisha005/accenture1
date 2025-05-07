import json
import numpy as np
from db.db_utils import execute_query
from sentence_transformers import SentenceTransformer
import numpy as np
import sqlite3
try:
    model = SentenceTransformer('all-MiniLM-L6-v2')
except Exception as e:
    print("Failed to load Transformer model:", e)
    raise

def get_embedding(text):
    if not isinstance(text, str):
        text = str(text)
    
    embedding =  model.encode(text).tolist()
    return embedding

def cosine_similarity(a, b):
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))
def store_embedding(product_id, embedding):
    conn = sqlite3.connect('db/retail_agents.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT OR REPLACE INTO product_embeddings (product_id, embedding)
        VALUES (?, ?)
    ''', (product_id, json.dumps(embedding)))  # Make sure you're saving as JSON string
    conn.commit()
    conn.close()