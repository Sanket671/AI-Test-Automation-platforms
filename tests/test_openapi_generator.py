from generator.openapi_generator import generate_from_openapi


def test_openapi_generates_tests():
    spec = """
openapi: 3.0.3
info:
  title: Demo
  version: 1.0.0
servers:
  - url: http://127.0.0.1:5001
paths:
  /health:
    get:
      summary: Health check
      responses:
        '200':
          description: ok
"""
    tests = generate_from_openapi(spec)
    assert len(tests) == 1
    assert tests[0]["method"] == "GET"
    assert tests[0]["expected_status"] == 200
