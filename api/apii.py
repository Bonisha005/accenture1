from flask import Flask, jsonify
import subprocess

app = Flask(__name__)

@app.route('/api/run_agents', methods=['POST'])
def run_agents():
    try:
        result = subprocess.run(
            ["python", "main.py"],
            capture_output=True,
            text=True,
            check=True
        )
        return jsonify({"status": "success", "output": result.stdout})
    except subprocess.CalledProcessError as e:
        return jsonify({"status": "error", "error": e.stderr})

if __name__ == '__main__':
    app.run(debug=True)