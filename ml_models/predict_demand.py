import pandas as pd
import pickle

# Load your model
with open('demand_model.pkl', 'rb') as f:
    model = pickle.load(f)

# Load your CSV data
df = pd.read_csv('demand_forecasting.csv')  # change this to your actual file name

# STEP 1: Handle promotions as a binary variable
df['Promotions'] = df['Promotions'].map({'Yes': 1, 'No': 0})

# STEP 2: Check the columns used during training
# Remove 'Customer Segments' and other irrelevant columns if needed
df = df.drop(columns=['Customer Segments'])  # Remove if not relevant

# STEP 3: Encode features like 'Demand Trend' and 'Seasonality Encoded'
df['Demand Trend'] = df['Demand Trend'].map({'Increasing': 1, 'Stable': 0, 'Decreasing': -1})  # Example mapping
df['Seasonality Encoded'] = df['Seasonality Factors'].map({'Festival': 1, 'Holiday': 2, 'None': 0})  # Example mapping

# STEP 4: Select only the features that the model expects
# Example: assuming these are the correct features
features = df[['Price', 'Promotions', 'Demand Trend', 'Seasonality Encoded']]

# STEP 5: Make the prediction
df['Predicted Demand'] = model.predict(features)

# STEP 6: Output the results
print(df[['Product ID', 'Store ID', 'Predicted Demand']])