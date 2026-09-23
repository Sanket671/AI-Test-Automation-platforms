from __future__ import annotations

import json
import os
import re
from typing import Any, Dict, List


def _fallback(workflow: str) -> List[Dict[str, Any]]:
    """Small deterministic fallback so the demo works without an API key."""
    lower = workflow.lower()
    tests: List[Dict[str, Any]] = []

    route_match = re.search(r"(GET|POST|PUT|PATCH|DELETE)\s+(/[^\s]*)", workflow, re.I)
    if route_match:
        method = route_match.group(1).upper()
        path = route_match.group(2)
    else:
        method = "GET"
        path = "/health"

    tests.append(
        {
            "name": f"Happy path for {method} {path}",
            "method": method,
            "url": "http://127.0.0.1:5001" + path,
            "expected_status": 200 if method == "GET" else 201,
            "body": {"name": "Test User"} if method in {"POST", "PUT", "PATCH"} else None,
            "reason": "Fallback generated test because no Gemini key was supplied",
        }
    )

    if any(word in lower for word in ["invalid", "error", "negative", "missing"]):
        tests.append(
            {
                "name": "Validation / negative test",
                "method": "POST",
                "url": "http://127.0.0.1:5001/users",
                "expected_status": 400,
                "body": {},
                "reason": "Negative case requested by workflow",
            }
        )
    return tests


def generate_from_workflow(workflow: str) -> List[Dict[str, Any]]:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return _fallback(workflow)

    from google import genai
    from pydantic import BaseModel

    class GeneratedTest(BaseModel):
        name: str
        method: str
        url: str
        expected_status: int
        body: Dict[str, Any] | None = None
        reason: str

    class GeneratedTests(BaseModel):
        tests: List[GeneratedTest]

    model = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")
    client = genai.Client(api_key=api_key)
    prompt = f"""
You are an API test designer.
Convert the following workflow into 1-5 practical API test cases.
Return only structured test cases. Prefer happy-path and one useful negative case.
Use this exact base URL for sample APIs: http://127.0.0.1:5001

Workflow:
{workflow}
"""
    response = client.models.generate_content(
        model=model,
        contents=prompt,
        config={
            "response_mime_type": "application/json",
            "response_schema": GeneratedTests.model_json_schema(),
        },
    )
    parsed = GeneratedTests.model_validate_json(response.text)
    return [item.model_dump() for item in parsed.tests]
