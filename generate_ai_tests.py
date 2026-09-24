from pathlib import Path
import json

from generator.openapi_generator import generate_from_openapi
from generator.ai_generator import generate_ai_tests
from generator.validator import validate_test_cases


OPENAPI_FILE = Path("specs/openapi.yaml")
OUTPUT_FILE = Path("reports/ai-generated-tests.json")


def main():
    openapi_text = OPENAPI_FILE.read_text(encoding="utf-8")

    base_tests = generate_from_openapi(openapi_text)

    ai_tests = generate_ai_tests(base_tests)

    validate_test_cases(ai_tests)

    OUTPUT_FILE.parent.mkdir(exist_ok=True)

    OUTPUT_FILE.write_text(
        json.dumps(ai_tests, indent=2),
        encoding="utf-8"
    )

    print(f"Base tests : {len(base_tests)}")
    print(f"AI tests   : {len(ai_tests)}")
    print(f"Output     : {OUTPUT_FILE}")


if __name__ == "__main__":
    main()