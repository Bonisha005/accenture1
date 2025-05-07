from waitress import serve
from api_main import app
try:
    from api_main import app
    print("Successfully imported app from api_main.py")
except Exception as e:
    print("Failed to import app from api_main.py")
    print("Error: ", e)
    raise

if __name__ == "__main__":
    print("Starting Waitress production server...")
    serve(app, host="0.0.0.0", port=5000)