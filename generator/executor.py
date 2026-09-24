import time
import requests


def execute_test(test_case):
    method = test_case["method"]
    url = test_case["url"]
    headers = test_case.get("headers", {})
    body = test_case.get("body")
    expected_status = test_case["expected_status"]

    start = time.perf_counter()

    try:
        response = requests.request(
            method=method,
            url=url,
            headers=headers,
            json=body,
            timeout=10,
        )

        duration_ms = round(
            (time.perf_counter() - start) * 1000,
            2,
        )

        passed = response.status_code == expected_status

        return {
            "name": test_case["name"],
            "method": method,
            "url": url,
            "expected_status": expected_status,
            "actual_status": response.status_code,
            "response_time_ms": duration_ms,
            "status": "PASS" if passed else "FAIL",
            "error": (
                None
                if passed
                else f"Expected {expected_status}, "
                     f"got {response.status_code}"
            ),
        }

    except requests.RequestException as exc:

        duration_ms = round(
            (time.perf_counter() - start) * 1000,
            2,
        )

        return {
            "name": test_case["name"],
            "method": method,
            "url": url,
            "expected_status": expected_status,
            "actual_status": None,
            "response_time_ms": duration_ms,
            "status": "FAIL",
            "error": str(exc),
        }