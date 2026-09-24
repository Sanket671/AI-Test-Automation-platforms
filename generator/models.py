from typing import Any, Dict, Optional


def create_test_case(
    name: str,
    method: str,
    url: str,
    expected_status: int,
    body: Optional[Dict[str, Any]] = None,
    headers: Optional[Dict[str, str]] = None,
    reason: str = "",
) -> Dict[str, Any]:
    return {
        "name": name,
        "method": method.upper(),
        "url": url,
        "headers": headers or {},
        "body": body,
        "expected_status": expected_status,
        "reason": reason,
    }