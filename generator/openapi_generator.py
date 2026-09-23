from __future__ import annotations

from typing import Any, Dict, List
import re
import yaml

HTTP_METHODS = {"get", "post", "put", "patch", "delete"}


def _default_status(operation: Dict[str, Any], method: str) -> int:
    responses = operation.get("responses", {})
    if responses:
        for code in ("200", "201", "204"):
            if code in responses:
                return int(code)
    return 201 if method == "post" else 200


def _example_body(operation: Dict[str, Any]) -> Dict[str, Any] | None:
    request_body = operation.get("requestBody", {}) or {}
    content = request_body.get("content", {}) or {}
    app_json = content.get("application/json", {}) or {}
    if "example" in app_json:
        return app_json["example"]
    schema = app_json.get("schema", {}) or {}
    props = schema.get("properties", {}) or {}
    if not props:
        return None
    body: Dict[str, Any] = {}
    for name, spec in props.items():
        if "example" in spec:
            body[name] = spec["example"]
        elif spec.get("type") == "integer":
            body[name] = 1
        elif spec.get("type") == "number":
            body[name] = 1.0
        elif spec.get("type") == "boolean":
            body[name] = True
        else:
            body[name] = "test"
    return body


def _fill_path_params(path: str, path_item: Dict[str, Any]) -> str:
    """Replace simple OpenAPI {param} placeholders with demo values."""
    result = path
    for name in re.findall(r"\{([^}]+)\}", path):
        result = result.replace("{" + name + "}", "1")
    return result

def _negative_tests(
    operation: Dict[str, Any],
    method: str,
    url: str,
    body: Dict[str, Any] | None,
    summary: str,
) -> List[Dict[str, Any]]:
    """Generate simple negative tests from documented 4xx responses."""
    responses = operation.get("responses", {}) or {}
    tests: List[Dict[str, Any]] = []

    for code in responses:
        try:
            status = int(code)
        except (TypeError, ValueError):
            continue

        if 400 <= status < 500:
            negative_url = url

            if status == 404 and "{" not in negative_url:
                parts = negative_url.rstrip("/").split("/")
                if parts:
                    parts[-1] = "999999"
                    negative_url = "/".join(parts)

            tests.append(
                {
                    "name": f"{summary} - negative",
                    "method": method,
                    "url": negative_url,
                    "expected_status": status,
                    "body": body,
                    "reason": "Generated from documented OpenAPI 4xx response",
                }
            )

    return tests


def generate_from_openapi(text: str) -> List[Dict[str, Any]]:
    spec = yaml.safe_load(text) or {}
    base_url = "http://127.0.0.1:5001"
    servers = spec.get("servers") or []
    if servers and isinstance(servers[0], dict):
        base_url = servers[0].get("url") or base_url

    tests: List[Dict[str, Any]] = []
    paths = spec.get("paths", {}) or {}
    for path, path_item in paths.items():
        if not isinstance(path_item, dict):
            continue
        for method, operation in path_item.items():
            if method.lower() not in HTTP_METHODS or not isinstance(operation, dict):
                continue
            m = method.upper()
            concrete_path = _fill_path_params(path, path_item)
            expected = _default_status(operation, method.lower())
            body = _example_body(operation) if m in {"POST", "PUT", "PATCH"} else None

            summary = operation.get("summary") or f"{m} {path}"
            url = base_url.rstrip("/") + concrete_path

            tests.append(
                {
                    "name": summary,
                    "method": m,
                    "url": url,
                    "expected_status": expected,
                    "body": body,
                    "reason": "Generated from OpenAPI path/operation metadata",
                }
            )

            tests.extend(
                _negative_tests(
                    operation=operation,
                    method=m,
                    url=url,
                    body=body,
                    summary=summary,
                )
            )

    return tests
