from tools.embedding_tool import get_embedding, cosine_similarity
from db.db_utils import execute_query
import json

def save_memory(agent, text, metadata=""):
    emb = get_embedding(text)
    emb_str = json.dumps(emb)
    execute_query("""
    INSERT INTO memory (agent_name, embedding, content, metadata)
    VALUES (?, ?, ?, ?)
    """, [agent, emb_str, text, metadata])
def search_memory(agent, query, top_k=3):
    query_vec = get_embedding(query)
    results = execute_query("""
    SELECT content, embedding FROM memory
    WHERE agent_name = ?
    """, [agent])

    ranked = []
    for content, emb_json in results:
        if not emb_json:
            continue  # skip empty/null embeddings
        try:
            emb = json.loads(emb_json)
        except json.JSONDecodeError:
            continue  # skip malformed embeddings
        sim = cosine_similarity(query_vec, emb)
        ranked.append((content, sim))

    ranked.sort(key=lambda x: -x[1])
    return [r[0] for r in ranked[:top_k]]
