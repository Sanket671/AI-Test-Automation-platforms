from __future__ import annotations

import json
import os
from pathlib import Path
from flask import Flask, jsonify, render_template, request

from generator.ai_generator import generate_from_workflow
from generator.openapi_generator import generate_from_openapi
from generator.postman import build_postman_collection
from generator.cypress import build_cypress_spec

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "reports"
OUTPUT_DIR.mkdir(exist_ok=True)

app = Flask(__name__)


@app.get("/")
def index():
    return render_template("index.html")


@app.get("/api/health")
def health():
    return jsonify({"status": "ok", "service": "test-automation-platform"})


@app.post("/api/generate")
def generate():
    payload = request.get_json(silent=True) or {}
    source = payload.get("source", "workflow")
    text = payload.get("input", "").strip()

    if not text:
        return jsonify({"error": "input is required"}), 400

    try:
        if source == "openapi":
            tests = generate_from_openapi(text)
        elif source == "workflow":
            tests = generate_from_workflow(text)
        else:
            return jsonify({"error": "source must be workflow or openapi"}), 400

        postman = build_postman_collection(tests)
        cypress = build_cypress_spec(tests)

        result = {
            "source": source,
            "tests": tests,
            "postman_collection": postman,
            "cypress_spec": cypress,
        }
        (OUTPUT_DIR / "latest-generation.json").write_text(
            json.dumps(result, indent=2), encoding="utf-8"
        )
        (OUTPUT_DIR / "generated.collection.json").write_text(
            json.dumps(postman, indent=2), encoding="utf-8"
        )
        (OUTPUT_DIR / "generated.cy.js").write_text(cypress, encoding="utf-8")

        return jsonify(result)
    except Exception as exc:
        return jsonify({"error": str(exc)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "5000")), debug=True)
