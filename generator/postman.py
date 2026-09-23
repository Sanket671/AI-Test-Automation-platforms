from __future__ import annotations

from typing import Any, Dict, List
import json


def build_postman_collection(tests: List[Dict[str, Any]]) -> Dict[str, Any]:
    items = []
    for test in tests:
        script = (
            "pm.test('status code matches', function () { "
            f"pm.response.to.have.status({int(test['expected_status'])}); "
            "});"
        )
        request = {
            "method": test["method"],
            "header": [{"key": "Content-Type", "value": "application/json"}],
            "url": {"raw": test["url"], "protocol": "http", "host": ["127.0.0.1:5001"], "path": []},
        }
        if test.get("body") is not None:
            request["body"] = {
                "mode": "raw",
                "raw": json.dumps(test["body"]),
                "options": {"raw": {"language": "json"}},
            }
        items.append(
            {
                "name": test["name"],
                "request": request,
                "event": [{"listen": "test", "script": {"exec": [script]}}],
            }
        )
    return {
        "info": {
            "name": "AI Generated API Tests",
            "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json",
        },
        "item": items,
    }
