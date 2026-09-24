from pathlib import Path
import json

from generator.openapi_generator import generate_from_openapi
from generator.executor import execute_test
from generator.validator import validate_test_cases

OPENAPI_FILE = Path("specs/openapi.yaml")
REPORT_FILE = Path("reports/generated-test-report.json")


def main():

    openapi_text = OPENAPI_FILE.read_text(
        encoding="utf-8"
    )

    test_cases = generate_from_openapi(
        openapi_text
    )

    validate_test_cases(test_cases)
    print(f"Validated {len(test_cases)} test cases")

    results = []

    for test_case in test_cases:

        result = execute_test(test_case)

        results.append(result)

        print(
            f"[{result['status']}] "
            f"{result['method']} "
            f"{result['url']} "
            f"(expected={result['expected_status']}, "
            f"actual={result['actual_status']})"
        )

    total = len(results)

    passed = sum(
        1
        for result in results
        if result["status"] == "PASS"
    )

    failed = total - passed

    report = {
        "total": total,
        "passed": passed,
        "failed": failed,
        "results": results,
    }

    REPORT_FILE.parent.mkdir(
        exist_ok=True
    )

    REPORT_FILE.write_text(
        json.dumps(report, indent=2),
        encoding="utf-8",
    )

    print()
    print(f"Total : {total}")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    print(f"Report: {REPORT_FILE}")


if __name__ == "__main__":
    main()