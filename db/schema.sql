-- Table to store inventory levels per store and product
CREATE TABLE IF NOT EXISTS inventory (
    store_id TEXT,
    product_id TEXT,
    stock_level INTEGER,
    last_updated DATETIME DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (store_id, product_id)
);

-- Table to store demand forecasts
CREATE TABLE IF NOT EXISTS demand_forecast (
    product_id TEXT,
    store_id TEXT,
    forecast_qty INTEGER,
    timeframe TEXT,
    confidence REAL,
    generated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table to store orders between store ↔ warehouse ↔ supplier
CREATE TABLE IF NOT EXISTS orders (
    order_id TEXT PRIMARY KEY,
    source_id TEXT,
    dest_id TEXT,
    product_id TEXT,
    qty INTEGER,
    status TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table to track current prices and discounts
CREATE TABLE IF NOT EXISTS price_tracking (
    product_id TEXT,
    price REAL,
    discount REAL,
    effective_date DATE
);

-- Table to capture basic customer interaction data
CREATE TABLE IF NOT EXISTS customer_behavior (
    product_id TEXT,
    views INTEGER,
    clicks INTEGER,
    purchases INTEGER,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table to log agent actions for auditing and debugging
CREATE TABLE IF NOT EXISTS logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    agent_name TEXT,
    action TEXT,
    message TEXT,
    status TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Table to store past sales per store/product
CREATE TABLE IF NOT EXISTS sales_history (
    store_id TEXT,
    product_id TEXT,
    sale_date DATE,
    quantity INTEGER
);

CREATE TABLE IF NOT EXISTS memory (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    agent_name TEXT,
    embedding TEXT,
    content TEXT,
    metadata TEXT
);

CREATE TABLE IF NOT EXISTS product_embeddings (
    product_id TEXT PRIMARY KEY,
    embedding TEXT -- JSON stringified vector
);

CREATE TABLE IF NOT EXISTS pricing (
    product_id TEXT PRIMARY KEY,
    current_price REAL,
    suggested_price REAL,
    last_updated DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE  IF NOT EXISTS agent_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    agent_name TEXT,
    action TEXT,
    status TEXT,
    message TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS demand_predictions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id TEXT NOT NULL,
    store_id TEXT NOT NULL,
    predicted_quantity INTEGER NOT NULL,
    timestamp TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS model_versions (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  model_name TEXT NOT NULL,
  version TEXT NOT NULL,
  mse REAL,
  r_squared REAL,
  created_at TEXT DEFAULT CURRENT_TIMESTAMP
);