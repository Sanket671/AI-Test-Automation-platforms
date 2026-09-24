import pytest

from generator.validator import validate_test_case


def test_valid_test_case():

    test_case = {
        "name": "Health check",
        "method": "GET",
        "url": "http://127.0.0.1:5001/health",
        "expected_status": 200,
        "body": None,
    }

    assert validate_test_case(test_case) is None


def test_invalid_http_method():

    test_case = {
        "name": "Invalid",
        "method": "INVALID",
        "url": "http://127.0.0.1:5001/test",
        "expected_status": 200,
    }

    with pytest.raises(ValueError):
        validate_test_case(test_case)


def test_invalid_status_type():

    test_case = {
        "name": "Invalid",
        "method": "GET",
        "url": "http://127.0.0.1:5001/test",
        "expected_status": "200",
    }

    with pytest.raises(ValueError):
        validate_test_case(test_case)