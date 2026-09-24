from flask import Flask, jsonify
from flask_cors import CORS
from pathlib import Path
import json

from generator.openapi_generator import generate_from_openapi
from generator.validator import validate_test_cases
from generator.executor import execute_test

app = Flask(__name__)
CORS(app)

OPENAPI_FILE = Path("specs/openapi.yaml")
AI_TEST_FILE = Path("reports/ai-generated-tests.json")


@app.get("/api/health")
def health():
    return jsonify({"status": "ok"})


@app.post("/api/generate")
def generate():
    text = OPENAPI_FILE.read_text(encoding="utf-8")

    tests = generate_from_openapi(text)
    validate_test_cases(tests)

    return jsonify({
        "type": "openapi",
        "total": len(tests),
        "tests": tests
    })


@app.post("/api/ai-generate")
def ai_generate():
    if not AI_TEST_FILE.exists():
        return jsonify({
            "error": "AI tests not generated yet. Run generate_ai_tests.py first."
        }), 404

    tests = json.loads(
        AI_TEST_FILE.read_text(encoding="utf-8")
    )

    validate_test_cases(tests)

    return jsonify({
        "type": "ai",
        "total": len(tests),
        "tests": tests
    })


@app.post("/api/run")
def run_tests():
    text = OPENAPI_FILE.read_text(encoding="utf-8")

    tests = generate_from_openapi(text)
    validate_test_cases(tests)

    results = [execute_test(test) for test in tests]

    passed = sum(
        1 for result in results
        if result["status"] == "PASS"
    )

    return jsonify({
        "total": len(results),
        "passed": passed,
        "failed": len(results) - passed,
        "results": results
    })


@app.post("/api/ai-run")
def ai_run():
    if not AI_TEST_FILE.exists():
        return jsonify({
            "error": "AI tests not generated yet."
        }), 404

    tests = json.loads(
        AI_TEST_FILE.read_text(encoding="utf-8")
    )

    validate_test_cases(tests)

    results = [execute_test(test) for test in tests]

    passed = sum(
        1 for result in results
        if result["status"] == "PASS"
    )

    return jsonify({
        "type": "ai",
        "total": len(results),
        "passed": passed,
        "failed": len(results) - passed,
        "results": results
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002)