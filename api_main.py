# api_main.py

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
import sqlite3
import pandas as pd
from datetime import datetime
import joblib

from db.db_utils import execute_query, execute_non_query, get_connection
from tools.chat_tool import generate_chat_response
from ml_models.model_loader import load_model
from ml_models.predict_utils import prepare_demand_features
from ml_models.predict_utils import prepare_inventory_features
from ml_models.predict_utils import prepare_pricing_features
from agents import store_agent, warehouse_agent, demand_forecaster, pricing_optimizer, orchestrator_agent

# Agent runners
from agents.store_agent import run as run_store_agent
from agents.warehouse_agent import run as run_warehouse_agent
from agents.demand_forecaster import run as run_demand_forecaster
from agents.pricing_optimizer import run as run_pricing_optimizer
from agents.orchestrator_agent import run as run_orchestrator_agent

# Flask setup
app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {"csv"}
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Load models
demand_model = load_model("ml_models/demand_model.pkl")
pricing_model = joblib.load("ml_models/pricing_model.pkl")

# Auto-run flag
auto_run_status = {"enabled": True}

# Helpers
def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Retail AI API is running!"})

@app.route("/routes", methods=["GET"])
def list_routes():
    return jsonify([str(rule) for rule in app.url_map.iter_rules()])

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    query = data.get("query", "")
    response = generate_chat_response(query)
    return jsonify({"response": response})

@app.route('/run/<agent_name>', methods=['GET'])
def run_agent(agent_name):
    try:
        runner = {
            'store': run_store_agent,
            'warehouse': run_warehouse_agent,
            'forecast': run_demand_forecaster,
            'pricing': run_pricing_optimizer,
            'orchestrator': run_orchestrator_agent
        }.get(agent_name)

        if not runner:
            return jsonify({'error': 'Unknown agent name'}), 400

        result = runner()
        return jsonify({'message': f'{agent_name} agent ran successfully', 'result': result})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Product/store pairs for dropdowns
@app.route("/api/products", methods=['GET'])
def get_product_store_ids():
    try:
        conn = get_connection()
        conn.row_factory = sqlite3.Row

        rows = conn.execute("SELECT DISTINCT [Product ID], [Store ID] FROM demand_forecasting").fetchall()
        conn.close()

        return jsonify({
            "products": [
                {
                    "product_id": row["Product ID"],
                    "store_id": row["Store ID"]
                } for row in rows
            ]
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Inventory, pricing, and demand data APIs
@app.route("/api/inventory", methods=["GET"])
def get_inventory_data():
    conn = get_connection()
    cursor = conn.execute("SELECT * FROM inventory_monitoring")
    columns = [column[0] for column in cursor.description]
    rows = cursor.fetchall()
    conn.close()
    return jsonify([dict(zip(columns, row)) for row in rows])

@app.route("/api/pricing", methods=["GET"])
def get_pricing_data():
    conn = get_connection()
    cursor = conn.execute("SELECT * FROM pricing_optimization")
    columns = [column[0] for column in cursor.description]
    rows = cursor.fetchall()
    conn.close()
    return jsonify([dict(zip(columns, row)) for row in rows])

@app.route("/api/demand", methods=["GET"])
def get_demand_data():
    try:
        conn = get_connection()
        cursor = conn.execute("SELECT * FROM demand_forecasting")
        columns = [column[0] for column in cursor.description]
        rows = cursor.fetchall()
        conn.close()
        return jsonify([dict(zip(columns, row)) for row in rows])
    except Exception as e:
        print(f"Error in /api/demand: {e}")
        return jsonify({"error": "Internal Server Error"}), 500

from flask import Flask, request, jsonify
import joblib
import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder
import os


# Correct paths to load models from scripts/ml_models/
pricing_model = joblib.load(os.path.join('scripts', 'ml_models', 'pricing_model.pkl'))
demand_model = joblib.load(os.path.join('scripts', 'ml_models', 'demand_model.pkl'))
inventory_model = joblib.load(os.path.join('scripts', 'ml_models', 'inventory_model.pkl'))

# ----- PREDICT PRICING -----
@app.route('/api/predict/pricing', methods=['POST'])
def predict_pricing():
    data = request.get_json()
    required = ['competitor_prices', 'discounts', 'sales_volume', 'reviews', 'return_rate', 'storage_cost', 'elasticity_index']

    try:
        features = [data[col] for col in required]
        prediction = pricing_model.predict([features])[0]
        return jsonify({'predicted_price': round(prediction, 2)})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# ----- PREDICT DEMAND -----
@app.route('/api/predict/demand', methods=['POST'])
def predict_demand():
    data = request.get_json()
    try:
        seasonality = data['seasonality_factors']
        trend = data['demand_trend'].lower()
        promotions = data['promotions'].lower()

        # Adjust these values based on your actual training set
        seasonality_encoder = LabelEncoder()
        seasonality_encoder.fit(["low", "medium", "high", "holiday"])
        seasonality_encoded = seasonality_encoder.transform([seasonality])[0]

        trend_map = {'increasing': 1, 'stable': 0, 'decreasing': -1}
        promo_map = {'yes': 1, 'no': 0}

        X = [[
            data['price'],
            promo_map[promotions],
            seasonality_encoded,
            trend_map[trend]
        ]]
        prediction = demand_model.predict(X)[0]
        return jsonify({'predicted_demand': round(prediction)})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# ----- PREDICT INVENTORY -----
@app.route('/api/predict/inventory', methods=['POST'])
def predict_inventory():
    data = request.get_json()
    required = ['lead_time', 'stockout_freq', 'reorder_point', 'warehouse_cap', 'fulfillment_time', 'days_until_expiry']

    try:
        features = [data[col] for col in required]
        prediction = inventory_model.predict([features])[0]
        return jsonify({'predicted_stock_level': round(prediction)})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# Prediction results fetch
@app.route("/api/predictions", methods=["GET"])
def get_predictions():
    conn = get_connection()
    rows = conn.execute("SELECT product_id, store_id, predicted_quantity, timestamp FROM demand_predictions ORDER BY timestamp DESC LIMIT 10").fetchall()
    conn.close()
    return jsonify([dict(row) for row in rows])

# CSV Upload
@app.route("/upload-csv", methods=["POST"])
def upload_csv():
    if "file" not in request.files: return jsonify({"error": "No file part"}), 400
    file = request.files["file"]
    if file.filename == "": return jsonify({"error": "No selected file"}), 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(filepath)
        try:
            df = pd.read_csv(filepath)
            table_map = {
                "demand": "demand_forecasting",
                "inventory": "inventory_monitoring",
                "pricing": "pricing_optimization"
            }
            for key, table in table_map.items():
                if key in filename:
                    conn = sqlite3.connect("db/retail_agents.db")
                    df.to_sql(table, conn, if_exists="replace", index=False)
                    conn.close()
                    return jsonify({"message": f"Data inserted into {table} successfully"}), 200
            return jsonify({"error": "Filename must contain 'demand', 'inventory', or 'pricing'"}), 400
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    return jsonify({"error": "Invalid file format"}), 400

# Auto-run endpoints
@app.route("/api/autorun_status", methods=["GET"])
def get_autorun_status():
    return jsonify({"auto_run": auto_run_status["enabled"]})

@app.route("/api/set_autorun", methods=["POST"])
def set_autorun():
    data = request.get_json()
    auto_run_status["enabled"] = data.get("auto_run", False)
    return jsonify({"success": True, "auto_run": auto_run_status["enabled"]})

# Logs and cleanup
@app.route('/api/logs', methods=['GET'])
def get_logs():
    try:
        conn = get_connection()
        conn.row_factory = sqlite3.Row
        logs = conn.execute('SELECT id, agent_name, action, message, timestamp FROM logs ORDER BY timestamp DESC LIMIT 100').fetchall()
        conn.close()
        return jsonify({"logs": [dict(row) for row in logs]})
    except Exception as e:
        print(f"Error fetching logs: {e}")
        return jsonify({"error": "Internal Server Error"}), 500

@app.route("/api/logs/cleanup", methods=["POST"])
def cleanup_logs():
    conn = get_connection()
    conn.execute("DELETE FROM logs")
    conn.commit()
    conn.close()
    return jsonify({"message": "All logs deleted successfully."})

# Model retraining
@app.route('/api/retrain_model', methods=['POST'])
def retrain_model():
    try:
        from ml_models.retrain_pricing_model import retrain_pricing_model
        mse, model_path = retrain_pricing_model()
        return jsonify({'message': 'Model retrained successfully', 'mse': mse, 'model_path': model_path})
    except Exception as e:
        app.logger.error(f"Retraining error: {e}")
        return jsonify({'error': str(e)}), 500

# Alerts
@app.route('/api/alerts', methods=['GET'])
def get_product_alerts():
    try:
        conn = get_connection()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        # Example alerts — customize thresholds or logic as needed
        low_stock_alerts = cursor.execute("""
            SELECT [Product ID],[Store ID], [Stock Levels]
            FROM inventory_monitoring
            WHERE [Stock Levels] <= 20
        """).fetchall()

        low_demand_alerts = cursor.execute("""
            SELECT [product_id], [store_id], [predicted_quantity]
            FROM demand_predictions
            WHERE [predicted_quantity] < 50
        """).fetchall()

        alerts = []

        for row in low_stock_alerts:
            alerts.append({
                "type": "Low Stock",
                "product_id": row["Product ID"],
                "store_id": row["Store ID"],
                "message": f"Stock is low ({row['Stock Levels']})"
            })

        for row in low_demand_alerts:
            alerts.append({
                "type": "Low Demand",
                "product_id": row["product_id"],
                "store_id": row["store_id"],
                "message": f"Predicted demand is low ({row['predicted_quantity']})"
            })

        return jsonify({"alerts": alerts})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Start app (optional for local debugging)
if __name__ == "__main__":
    app.run(debug=True)