# routes.py

from flask import request, jsonify
from datetime import datetime
import pandas as pd
from db.db_utils import execute_non_query

def register_routes(app, model):
    @app.route('/predict/demand', methods=['POST'])
    def predict_demand():
        data = request.get_json()
        product_id = data.get("product_id", "")

        features = pd.DataFrame([{
            "Price": 50,
            "Promotions": 1,
            "Seasonality Factors": 0,
            "External Factors": 0,
            "Demand Trend": 1
        }])

        prediction = model.predict(features)[0]
        confidence = 0.85
        timestamp = datetime.utcnow().isoformat()

        log_entry = f"[{timestamp}] Demand prediction for Product {product_id}: {prediction} (Confidence: {confidence})"
        execute_non_query("INSERT INTO logs (agent_name, log_message) VALUES (?, ?)", ("DemandPredictor", log_entry))

        return jsonify({
            'predicted_quantity': int(prediction),
            'confidence': round(confidence, 2),
            'timestamp': timestamp
        })

    # Add other prediction routes here as needed