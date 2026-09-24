from pathlib import Path
import json

from generator.executor import execute_test
from generator.validator import validate_test_cases


TEST_FILE = Path("reports/ai-generated-tests.json")
REPORT_FILE = Path("reports/ai-test-report.json")


def main():
    test_cases = json.loads(
        TEST_FILE.read_text(encoding="utf-8")
    )

    validate_test_cases(test_cases)

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
        1 for result in results
        if result["status"] == "PASS"
    )
    failed = total - passed

    report = {
        "total": total,
        "passed": passed,
        "failed": failed,
        "results": results
    }

    REPORT_FILE.write_text(
        json.dumps(report, indent=2),
        encoding="utf-8"
    )

    print()
    print(f"Total : {total}")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    print(f"Report: {REPORT_FILE}")


if __name__ == "__main__":
    main()