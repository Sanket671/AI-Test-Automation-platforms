# AI-Powered Intelligent Test Automation Platform (MVP)

A deliberately small, interview-friendly implementation of a GenAI-assisted API testing platform.

## What it does

1. Accepts a workflow description or an OpenAPI specification.
2. Converts the input into a small set of API test cases.
3. Converts test cases into a Postman Collection / Cypress test file.
4. Executes the API tests with Newman and Cypress.
5. Produces a JSON test report.
6. Runs the checks in GitHub Actions.
7. Packages the Python platform service into a Docker image.

## Important scope decision

This is an MVP, not a production-scale SaaS. The design intentionally favors understandable components:

- Flask for the platform API/UI.
- PyYAML for the small OpenAPI parser.
- Optional Gemini integration for workflow-to-test generation.
- Newman for Postman Collection execution.
- Cypress for direct API tests with `cy.request()`.
- GitHub Actions for CI.
- Docker for packaging the Python application.

## Run locally

### 1. Python service

```bash
python -m venv .venv
.venv\Scripts\activate
# Windows PowerShell: .\.venv\Scripts\Activate.ps1
# Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

Platform UI: http://127.0.0.1:5000
Health: http://127.0.0.1:5000/api/health

### 2. Sample API under test

In another terminal:

```bash
python sample_api.py
```

Sample API: http://127.0.0.1:5001

### 3. Node test tooling

```bash
npm install
npx newman run collections/demo.collection.json \
  --env-var baseUrl=http://127.0.0.1:5001 \
  --reporters cli,json \
  --reporter-json-export reports/newman-report.json

npx cypress run
```

## Optional Gemini setup

The platform can use the current Google GenAI Python SDK when `GEMINI_API_KEY` is provided.

```bash
# Windows PowerShell
$env:GEMINI_API_KEY="your_key"

# Linux/macOS
export GEMINI_API_KEY="your_key"
```

Then use the workflow-generation API or UI.

## Interview mental model

```text
Workflow / OpenAPI
        |
        v
   Test generator
   /           \
  AI       OpenAPI parser
   \           /
    \         /
     v       v
    Test case JSON
          |
     +----+----+
     |         |
  Newman    Cypress
     |         |
     +----+----+
          |
       Reports
          |
      GitHub CI
```
