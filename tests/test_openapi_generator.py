from pathlib import Path

from generator.openapi_generator import generate_from_openapi


def test_openapi_generates_expected_number_of_tests():

    text = Path(
        "specs/openapi.yaml"
    ).read_text(encoding="utf-8")

    tests = generate_from_openapi(text)

    assert len(tests) == 5


def test_post_user_contains_example_body():

    text = Path(
        "specs/openapi.yaml"
    ).read_text(encoding="utf-8")

    tests = generate_from_openapi(text)

    create_user = next(
        test
        for test in tests
        if test["name"] == "Create user"
    )

    assert create_user["method"] == "POST"
    assert create_user["body"]["name"] == "Test User"
    assert create_user["expected_status"] == 201


def test_404_negative_test_is_generated():

    text = Path(
        "specs/openapi.yaml"
    ).read_text(encoding="utf-8")

    tests = generate_from_openapi(text)

    negative = next(
        test
        for test in tests
        if test["name"] == "Get user - negative"
    )

    assert negative["expected_status"] == 404
    assert negative["url"].endswith("/users/999999")
    