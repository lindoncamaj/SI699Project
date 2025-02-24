from flask import Flask, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
cors = CORS(app, origins='*')

CAR_API = "https://carapi.app/api/makes"

@app.route("/api/makes", methods=["GET"])
def makes():
    try:
        response = requests.get(CAR_API)
        makes = response.json()
        return jsonify(makes)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=8080)
