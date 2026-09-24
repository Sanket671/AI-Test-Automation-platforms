from pathlib import Path

from generator.openapi_generator import generate_from_openapi
from generator.validator import validate_test_cases
from generator.cypress_generator import generate_cypress_tests
from generator.postman_generator import generate_postman_collection


def main():

    openapi_text = Path(
        "specs/openapi.yaml"
    ).read_text(encoding="utf-8")

    test_cases = generate_from_openapi(
        openapi_text
    )

    validate_test_cases(test_cases)

    print(
        f"Generated and validated "
        f"{len(test_cases)} test cases"
    )

    cypress_file = generate_cypress_tests(
        test_cases
    )

    postman_file = generate_postman_collection(
        test_cases
    )

    print(f"Cypress file: {cypress_file}")
    print(f"Newman collection: {postman_file}")


if __name__ == "__main__":
    main()