import json
from pathlib import Path
from generator.openapi_generator import generate_from_openapi
from generator.postman import build_postman_collection
from generator.cypress import build_cypress_spec

ROOT = Path(__file__).resolve().parents[1]
spec = (ROOT / "specs/openapi.yaml").read_text(encoding="utf-8")
tests = generate_from_openapi(spec)
(ROOT / "reports/openapi-tests.json").write_text(json.dumps(tests, indent=2), encoding="utf-8")
(ROOT / "reports/openapi-generated.collection.json").write_text(json.dumps(build_postman_collection(tests), indent=2), encoding="utf-8")
(ROOT / "reports/openapi-generated.cy.js").write_text(build_cypress_spec(tests), encoding="utf-8")
print(f"Generated {len(tests)} tests")
