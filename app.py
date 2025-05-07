from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello, Production!"

# Don't run app.run() here in production
if __name__ == "__main__":
    app.run(debug=True)  # Only for development