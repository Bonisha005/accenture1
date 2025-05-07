import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from tools.embedding_tool import get_embedding, store_embedding

# Example product descriptions
products = {
    "item_101": "Men's running shoes with breathable mesh and foam sole",
    "item_102": "Women's leather boots with winter insulation",
    "item_103": "Kids sneakers with Velcro straps and flexible soles"
}

# Loop through products and process embeddings
for product_id, desc in products.items():
    if isinstance(desc, str):  # Ensure description is a string
        embedding = get_embedding(desc)  # Generate the embedding
        store_embedding(product_id, embedding)  # Store the embedding in the database
        print(f"✅ Embedded {product_id} with description: '{desc}'")
    else:
        print(f"❌ Error: Description for {product_id} is not a valid string!")