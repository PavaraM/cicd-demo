from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "not found"}), 404


@app.errorhandler(500)
def server_error(e):
    return jsonify({"error": "internal server error"}), 500


@app.route("/")
def home():
    return jsonify({"status": "ok", "message": "hello from cicd-demo", "version": "2.0"})


@app.route("/health")
def health():
    return jsonify({"healthy": True})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)