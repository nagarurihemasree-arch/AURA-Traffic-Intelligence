from flask import Flask, jsonify
from flask_cors import CORS
import pandas as pd
import os

app = Flask(__name__)
CORS(app)

# Path to analytics results
DATA_FILE = os.path.join(
    os.path.dirname(__file__),
    "..",
    "data",
    "traffic_analysis.csv"
)


@app.route("/")
def home():
    return "AURA Backend is Running"


@app.route("/api/traffic")
def traffic_data():
    df = pd.read_csv(DATA_FILE)

    return jsonify(df.to_dict(orient="records"))


if __name__ == "__main__":
    app.run(debug=True)