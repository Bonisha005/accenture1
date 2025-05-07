from flask import Flask
from waitress import serve
app = Flask(__name__)
@app.route("/")
def hello():
    return "Flask is working!"

if __name__ == "__main__":
    print("Running test server ...")
    serve(app, host="0.0.0.0", port=5000)