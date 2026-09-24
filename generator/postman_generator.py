from pathlib import Path
import json


def generate_postman_collection(
    test_cases,
    output_file="collections/generated.collection.json",
):

    items = []

    for test in test_cases:

        request = {
            "method": test["method"],
            "header": [],
            "url": test["url"],
        }

        body = test.get("body")

        if body is not None:

            request["header"].append(
                {
                    "key": "Content-Type",
                    "value": "application/json",
                }
            )

            request["body"] = {
                "mode": "raw",
                "raw": json.dumps(body),
                "options": {
                    "raw": {
                        "language": "json"
                    }
                },
            }

        expected_status = test["expected_status"]

        item = {
            "name": test["name"],
            "request": request,
            "event": [
                {
                    "listen": "test",
                    "script": {
                        "type": "text/javascript",
                        "exec": [
                            f"pm.test('Status is {expected_status}', function () {{",
                            f"    pm.response.to.have.status({expected_status});",
                            "});",
                        ],
                    },
                }
            ],
        }

        items.append(item)

    collection = {
        "info": {
            "_postman_id": "ai-test-automation-generated",
            "name": "AI Test Automation Generated Collection",
            "schema": (
                "https://schema.getpostman.com/"
                "json/collection/v2.1.0/"
                "collection.json"
            ),
        },
        "item": items,
    }

    output = Path(output_file)
    output.parent.mkdir(parents=True, exist_ok=True)

    output.write_text(
        json.dumps(collection, indent=2),
        encoding="utf-8",
    )

    return str(output)