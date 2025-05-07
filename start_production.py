from waitress import serve
from app import app  # Make sure this matches your filename and Flask instance
from scheduler import start_scheduler
if __name__=="__main__":
    print("Starting production mode...")
    start_scheduler()

    try:
        while True:
            import time
            time.sleep(60)
    except KeyboardInterrupt:
        print("Production stopped")

serve(app, host='0.0.0.0', port=5000)