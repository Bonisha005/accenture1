def forecast_demand(data):
    # Placeholder logic
    product_id = data.get('product_id', 'unknown')
    predicted_quantity = 120  # example static value
    return {
        'product_id': product_id,
        'predicted_quantity': predicted_quantity,
        'confidence': 0.92
    }