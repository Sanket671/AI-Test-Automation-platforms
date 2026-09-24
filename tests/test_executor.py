from generator.executor import execute_test


def test_executor_health_check():

    test_case = {
        "name": "Health check",
        "method": "GET",
        "url": "http://127.0.0.1:5001/health",
        "expected_status": 200,
        "body": None,
    }

    result = execute_test(test_case)

    assert result["status"] == "PASS"
    assert result["actual_status"] == 200


def test_executor_detects_wrong_status():

    test_case = {
        "name": "Intentional failure",
        "method": "GET",
        "url": "http://127.0.0.1:5001/health",
        "expected_status": 201,
        "body": None,
    }

    result = execute_test(test_case)

    assert result["status"] == "FAIL"
    assert result["actual_status"] == 200