from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# List of backend servers
backends = ["http://localhost:5001", "http://localhost:5002"]
current_server = 0  # To track the round-robin selection

@app.route("/", defaults={"path": ""}, methods=["GET", "POST"])
@app.route("/<path:path>", methods=["GET", "POST"])
def load_balance(path):
    global current_server
    server = backends[current_server]  # Pick the next server

    # Round-robin logic
    current_server = (current_server + 1) % len(backends)

    # Forward the request to the selected backend
    try:
        if request.method == "GET":
            response = requests.get(f"{server}/{path}", params=request.args)
        else:
            response = requests.post(f"{server}/{path}", json=request.json)

        return response.content, response.status_code
    except requests.exceptions.RequestException:
        return jsonify({"error": "Backend server unavailable"}), 500

if __name__ == "__main__":
    app.run(port=5000)