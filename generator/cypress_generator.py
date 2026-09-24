from pathlib import Path
import json


def generate_cypress_tests(
    test_cases,
    output_file="cypress/e2e/generated_api.cy.js",
):

    lines = [
        "describe('Generated API Tests', () => {"
    ]

    for test in test_cases:

        name = json.dumps(test["name"])
        method = test["method"]
        url = json.dumps(test["url"])
        expected = test["expected_status"]

        body = test.get("body")

        if body is not None:

            body_json = json.dumps(body)

            lines.extend(
                [
                    f"  it({name}, () => {{",
                    "    cy.request({",
                    f"      method: '{method}',",
                    f"      url: {url},",
                    f"      body: {body_json},",
                    "      failOnStatusCode: false",
                    "    }).then((response) => {",
                    f"      expect(response.status).to.eq({expected});",
                    "    });",
                    "  });",
                ]
            )

        else:

            lines.extend(
                [
                    f"  it({name}, () => {{",
                    "    cy.request({",
                    f"      method: '{method}',",
                    f"      url: {url},",
                    "      failOnStatusCode: false",
                    "    }).then((response) => {",
                    f"      expect(response.status).to.eq({expected});",
                    "    });",
                    "  });",
                ]
            )

    lines.append("});")

    output = Path(output_file)
    output.parent.mkdir(parents=True, exist_ok=True)

    output.write_text(
        "\n".join(lines),
        encoding="utf-8",
    )

    return str(output)