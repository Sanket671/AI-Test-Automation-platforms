from __future__ import annotations

import json
from typing import Any, Dict, List


def _js_body(body: Dict[str, Any] | None) -> str:
    return "null" if body is None else json.dumps(body)


def build_cypress_spec(tests: List[Dict[str, Any]]) -> str:
    lines = [
        "describe('Generated API tests', () => {",
    ]
    for test in tests:
        body = _js_body(test.get("body"))
        lines.extend(
            [
                f"  it({json.dumps(test['name'])}, () => {{",
                "    cy.request({",
                f"      method: {json.dumps(test['method'])},",
                f"      url: {json.dumps(test['url'])},",
                f"      body: {body},",
                "      failOnStatusCode: false,",
                "    }).then((response) => {",
                f"      expect(response.status).to.eq({int(test['expected_status'])});",
                "    });",
                "  });",
            ]
        )
    lines.append("});")
    return "\n".join(lines) + "\n"
