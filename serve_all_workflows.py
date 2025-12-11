# serve_all_workflows.py
from flask import Flask, jsonify, request
import json, os
from pathlib import Path

APP_PORT = int(os.getenv("FLASK_PORT", "5000"))
DATA_FILE = "workflows_final.json"

app = Flask(__name__)

if not Path(DATA_FILE).exists():
    raise SystemExit(f"{DATA_FILE} not found. Run merge_datasets.py to create it.")
with open(DATA_FILE, "r", encoding="utf-8") as f:
    WORKFLOWS = json.load(f)

@app.route("/health")
def health():
    return jsonify({"status":"ok","count": len(WORKFLOWS)})

@app.route("/workflows")
def workflows():
    platform = request.args.get("platform")
    country = request.args.get("country")
    q = request.args.get("q", "").strip().lower()
    try:
        limit = min(1000, int(request.args.get("limit", 100)))
    except:
        limit = 100
    try:
        offset = max(0, int(request.args.get("offset", 0)))
    except:
        offset = 0

    results = WORKFLOWS

    if platform:
        results = [r for r in results if r.get("platform","").lower() == platform.lower()]
    if country:
        results = [r for r in results if (r.get("country","").lower() == country.lower())]
    if q:
        results = [r for r in results if q in r.get("workflow","").lower()]

    total = len(results)
    page = results[offset: offset + limit]
    return jsonify({
        "count": total,
        "limit": limit,
        "offset": offset,
        "results": page
    })

if __name__ == "__main__":
    print(f"Serving {len(WORKFLOWS)} workflows on port {APP_PORT} ...")
    app.run(host="0.0.0.0", port=APP_PORT)
