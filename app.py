from flask import Flask, render_template, request, jsonify
import pandas as pd

app = Flask(__name__)

CSV_FILE = "Centrify_Computers_Zone_Domain.csv"

def load_data():
    return pd.read_csv(CSV_FILE)

@app.route("/")
def index():
    search = request.args.get("search", "").lower()
    df = load_data()
    if search:
        df = df[df.apply(lambda row: row.astype(str).str.lower().str.contains(search).any(), axis=1)]
    records = df.to_dict(orient="records")
    return render_template("index.html", computers=records, search=search)

@app.route("/api/computer/<name>")
def get_computer(name):
    df = load_data()
    matches = df[df['ComputerName'].str.lower() == name.lower()]
    if matches.empty:
        return jsonify({"error": "Computer not found"}), 404
    return jsonify(matches.to_dict(orient="records")[0])

if __name__ == "__main__":
    app.run(debug=True)
