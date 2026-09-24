from typing import Any, Dict


ALLOWED_METHODS = {
    "GET",
    "POST",
    "PUT",
    "PATCH",
    "DELETE",
}


def validate_test_case(test_case: Dict[str, Any]) -> None:

    required_fields = {
        "name",
        "method",
        "url",
        "expected_status",
    }

    missing = required_fields - test_case.keys()

    if missing:
        raise ValueError(
            f"Missing required fields: {sorted(missing)}"
        )

    method = test_case["method"].upper()

    if method not in ALLOWED_METHODS:
        raise ValueError(
            f"Unsupported HTTP method: {method}"
        )

    if not isinstance(test_case["url"], str) or not test_case["url"]:
        raise ValueError("URL must be a non-empty string")

    if not isinstance(test_case["expected_status"], int):
        raise ValueError(
            "expected_status must be an integer"
        )

    body = test_case.get("body")

    if body is not None and not isinstance(body, dict):
        raise ValueError(
            "body must be an object or null"
        )


def validate_test_cases(test_cases):
    for test_case in test_cases:
        validate_test_case(test_case)

    return True