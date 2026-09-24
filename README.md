# AI Test Automation Platform V2

An AI-assisted API test automation platform that takes an **OpenAPI specification**, automatically generates API test cases, validates and executes them, generates additional test scenarios using **Google Gemini**, and exposes the complete workflow through a **Flask backend and React dashboard**.



## Table of Contents

- [AI Test Automation Platform V2](#ai-test-automation-platform-v2)
  - [Table of Contents](#table-of-contents)
  - [1. Project Overview](#1-project-overview)
    - [OpenAPI-based test generation](#openapi-based-test-generation)
    - [AI-assisted test generation](#ai-assisted-test-generation)
- [2. Main Features](#2-main-features)
- [3. Technology Stack](#3-technology-stack)
- [4. Architecture](#4-architecture)
- [5. Complete Project Workflow](#5-complete-project-workflow)
  - [Step 1 — OpenAPI Specification](#step-1--openapi-specification)
  - [Step 2 — Parse OpenAPI](#step-2--parse-openapi)
- [6. Test Case Model](#6-test-case-model)
- [7. Automatic Test Generation](#7-automatic-test-generation)
- [8. Positive and Negative Tests](#8-positive-and-negative-tests)
  - [Positive tests](#positive-tests)
  - [Negative test](#negative-test)
- [9. Test Validation](#9-test-validation)
    - [Required fields](#required-fields)
    - [Supported methods](#supported-methods)
    - [Other validation](#other-validation)
- [10. HTTP Executor](#10-http-executor)
- [11. Generated Test Runner](#11-generated-test-runner)
- [12. Gemini AI Test Generation](#12-gemini-ai-test-generation)
  - [AI Test Generation Workflow](#ai-test-generation-workflow)
- [13. AI-Generated Test Examples](#13-ai-generated-test-examples)
- [14. AI Test Generation Script](#14-ai-test-generation-script)
- [15. AI Test Execution](#15-ai-test-execution)
- [16. AI Failure Detection](#16-ai-failure-detection)
- [17. AI Execution Example](#17-ai-execution-example)
- [18. Cypress Integration](#18-cypress-integration)
- [19. Newman / Postman Integration](#19-newman--postman-integration)
- [20. Reporting](#20-reporting)
- [21. Flask Backend](#21-flask-backend)
- [22. Flask API Endpoints](#22-flask-api-endpoints)
  - [Health](#health)
  - [Generate OpenAPI Tests](#generate-openapi-tests)
  - [Generate/Get AI Tests](#generateget-ai-tests)
  - [Run OpenAPI Tests](#run-openapi-tests)
  - [Run AI Tests](#run-ai-tests)
- [23. React Dashboard](#23-react-dashboard)
- [24. Dashboard Workflow](#24-dashboard-workflow)
- [25. CORS Integration](#25-cors-integration)
- [26. Unit Testing](#26-unit-testing)
- [27. Artifact Generation](#27-artifact-generation)
- [28. Docker](#28-docker)
- [29. GitHub Actions](#29-github-actions)
- [30. Project Structure](#30-project-structure)
- [31. Running the Project](#31-running-the-project)
  - [Terminal 1 — Start the API Under Test](#terminal-1--start-the-api-under-test)
  - [Terminal 2 — Start the Test Automation Backend](#terminal-2--start-the-test-automation-backend)
  - [Terminal 3 — Start the React Frontend](#terminal-3--start-the-react-frontend)
- [32. Complete Local Workflow](#32-complete-local-workflow)
- [33. CLI Verification Commands](#33-cli-verification-commands)
  - [Generate standard artifacts](#generate-standard-artifacts)
  - [Run standard generated tests](#run-standard-generated-tests)
  - [Generate AI tests](#generate-ai-tests)
  - [Run AI tests](#run-ai-tests-1)
  - [Run unit tests](#run-unit-tests)
  - [Run Cypress](#run-cypress)
  - [Run Newman](#run-newman)
- [34. Verified Project Results](#34-verified-project-results)
    - [Standard generated tests](#standard-generated-tests)
    - [Unit tests](#unit-tests)
    - [Cypress](#cypress)
    - [Newman](#newman)
    - [Gemini](#gemini)
    - [AI execution](#ai-execution)
- [35. Important Design Separation](#35-important-design-separation)
- [36. Future Extensions](#36-future-extensions)
- [37. Project Summary](#37-project-summary)

---

## 1. Project Overview

The platform is designed to automate API testing from API specifications instead of requiring every test case to be written manually.

The system supports two main test-generation approaches:

### OpenAPI-based test generation

```text
OpenAPI Specification
        ↓
OpenAPI Parser
        ↓
Test Case Generation
        ↓
Validation
        ↓
HTTP Execution
        ↓
Report
```

### AI-assisted test generation

```text
OpenAPI/Test Information
        ↓
Gemini AI
        ↓
Additional Test Scenarios
        ↓
Validation
        ↓
HTTP Execution
        ↓
AI Test Report
```

The project also integrates Cypress and Newman so that the generated API tests can be exported into commonly used automation tools.

---

# 2. Main Features

- OpenAPI YAML parsing
- Automatic API test generation
- Positive test generation
- Negative test generation
- Structured test-case model
- Test-case validation
- HTTP test execution
- Expected vs actual status comparison
- Response-time measurement
- JSON reporting
- Gemini-based AI test generation
- AI-generated negative and boundary scenarios
- AI-generated test execution
- Cypress test generation
- Postman/Newman collection generation
- Flask REST API
- React dashboard
- Docker support
- GitHub Actions CI configuration
- Unit tests using pytest

---

# 3. Technology Stack

| Layer | Technology |
|---|---|
| Programming Language | Python |
| API Specification | OpenAPI / YAML |
| AI | Google Gemini |
| AI SDK | `google-genai` |
| API Execution | Python `requests` |
| Backend | Flask |
| Frontend | React + Vite |
| API Testing | Cypress |
| API Collection Testing | Postman + Newman |
| Unit Testing | pytest |
| Containerization | Docker |
| CI/CD | GitHub Actions |
| Data Format | JSON |

---

# 4. Architecture

```text
                         OpenAPI YAML
                              │
                              ▼
                    ┌───────────────────┐
                    │ OpenAPI Generator │
                    └─────────┬─────────┘
                              │
                     Base Test Cases
                              │
                    ┌─────────┴─────────┐
                    │                   │
                    ▼                   ▼
             Normal Tests         Gemini AI
                                        │
                                        ▼
                              AI Test Scenarios
                    │                   │
                    └─────────┬─────────┘
                              ▼
                     ┌────────────────┐
                     │   Validator    │
                     └───────┬────────┘
                             ▼
                     ┌────────────────┐
                     │ HTTP Executor  │
                     └───────┬────────┘
                             ▼
                       API Under Test
                         Port 5001
                             │
                             ▼
                      Actual Response
                             │
                             ▼
                    Expected vs Actual
                             │
                             ▼
                       PASS / FAIL
                             │
              ┌──────────────┼──────────────┐
              ▼              ▼              ▼
           Reports        Cypress         Newman
                             │
                             ▼
                       Flask Backend
                         Port 5002
                             │
                             ▼
                       React Dashboard
```

---

# 5. Complete Project Workflow

## Step 1 — OpenAPI Specification

The project starts with:

```text
specs/openapi.yaml
```

The specification describes the API endpoints, methods, request information and documented responses.

The sample API contains endpoints such as:

```text
GET    /health
GET    /users
POST   /users
GET    /users/{id}
```

---

## Step 2 — Parse OpenAPI

`generator/openapi_generator.py` reads the OpenAPI YAML and extracts:

- server URL
- API paths
- HTTP methods
- request body information
- request examples/schema properties
- documented response status codes
- path parameters

The sample API base URL is:

```text
http://127.0.0.1:5001
```

---

# 6. Test Case Model

Test cases are created using:

```text
generator/models.py
```

Each test case contains:

```text
name
method
url
headers
body
expected_status
reason
```

Example:

```json
{
  "name": "Create user",
  "method": "POST",
  "url": "http://127.0.0.1:5001/users",
  "headers": {},
  "body": {
    "name": "Test User"
  },
  "expected_status": 201,
  "reason": "Generated from OpenAPI path/operation metadata"
}
```

This common structure allows the same test cases to be used by:

- validator
- HTTP executor
- reports
- Flask API
- React dashboard

---

# 7. Automatic Test Generation

The OpenAPI generator produced the following base tests during development:

| Test | Method | Endpoint | Expected |
|---|---|---|---:|
| Health check | GET | `/health` | 200 |
| List users | GET | `/users` | 200 |
| Create user | POST | `/users` | 201 |
| Get user | GET | `/users/1` | 200 |
| Get user - negative | GET | `/users/999999` | 404 |

The generated tests are validated before execution.

---

# 8. Positive and Negative Tests

## Positive tests

Examples:

```text
GET /health → 200
GET /users → 200
POST /users → 201
GET /users/1 → 200
```

## Negative test

The generator creates a non-existing user scenario:

```text
GET /users/999999
Expected: 404
```

This test successfully returned:

```text
Expected: 404
Actual: 404
PASS
```

---

# 9. Test Validation

`generator/validator.py` validates generated tests before they reach the executor.

It checks:

### Required fields

```text
name
method
url
expected_status
```

### Supported methods

```text
GET
POST
PUT
PATCH
DELETE
```

### Other validation

```text
URL must be a non-empty string
expected_status must be an integer
body must be an object or null
```

This prevents malformed generated test cases from being executed.

---

# 10. HTTP Executor

`generator/executor.py` executes the test cases using Python `requests`.

For each test it records:

```text
Test name
HTTP method
URL
Expected status
Actual status
Response time
PASS / FAIL
Error
```

Example:

```json
{
  "name": "Health check",
  "method": "GET",
  "url": "http://127.0.0.1:5001/health",
  "expected_status": 200,
  "actual_status": 200,
  "response_time_ms": 17.66,
  "status": "PASS",
  "error": null
}
```

---

# 11. Generated Test Runner

`run_generated_tests.py` performs the complete specification-driven execution:

```text
Read OpenAPI
      ↓
Generate tests
      ↓
Validate tests
      ↓
Execute tests
      ↓
Calculate PASS/FAIL
      ↓
Generate JSON report
```

Run:

```bat
python run_generated_tests.py
```

Verified result:

```text
Validated 5 test cases

[PASS] GET http://127.0.0.1:5001/health
[PASS] GET http://127.0.0.1:5001/users
[PASS] POST http://127.0.0.1:5001/users
[PASS] GET http://127.0.0.1:5001/users/1
[PASS] GET http://127.0.0.1:5001/users/999999

Total : 5
Passed: 5
Failed: 0
```

---

# 12. Gemini AI Test Generation

The project uses Google Gemini to generate additional API test scenarios.

The AI layer is implemented in:

```text
generator/ai_generator.py
```

The Gemini API key is provided through:

```text
GEMINI_API_KEY
```

The key is not stored in source code.

---

## AI Test Generation Workflow

```text
Base API Tests
      ↓
Gemini Prompt
      ↓
AI Analysis
      ↓
Additional Test Cases
      ↓
JSON
      ↓
Validation
      ↓
Execution
```

The AI is instructed to focus on scenarios such as:

- missing required fields
- invalid data types
- empty values
- invalid IDs
- incorrect HTTP methods
- boundary values
- other negative scenarios

---

# 13. AI-Generated Test Examples

During development, Gemini generated tests such as:

```text
Create user - missing required fields
POST /users
Expected: 400
```

```text
Create user - invalid input type
POST /users
Expected: 400
```

```text
Create user - empty body
POST /users
Expected: 400
```

```text
Get user - invalid ID format
GET /users/invalid-id
Expected: 400
```

```text
List users - incorrect HTTP method
POST /users
Expected: 405
```

The exact number and scenarios can vary because the tests are generated by an LLM.

---

# 14. AI Test Generation Script

`generate_ai_tests.py` performs:

```text
OpenAPI
  ↓
Base Tests
  ↓
Gemini
  ↓
AI Tests
  ↓
reports/ai-generated-tests.json
```

Run:

```bat
python generate_ai_tests.py
```

Example output:

```text
Base tests : 5
AI tests   : 5
Output     : reports\ai-generated-tests.json
```

---

# 15. AI Test Execution

`run_ai_tests.py` loads:

```text
reports/ai-generated-tests.json
```

and executes each AI-generated test using the same HTTP executor.

Run:

```bat
python run_ai_tests.py
```

The platform then compares:

```text
AI expected status
        vs
Actual API status
```

---

# 16. AI Failure Detection

An important part of the project is detecting behavior mismatches.

Example:

```text
Expected: 400
Actual:   201
FAIL
```

Another example:

```text
Expected: 405
Actual:   201
FAIL
```

Another:

```text
Expected: 400
Actual:   404
FAIL
```

These results indicate that the generated expectation and actual API behavior differ.

The platform reports the mismatch for investigation instead of silently ignoring it.

---

# 17. AI Execution Example

A verified AI execution produced:

```text
Total : 6
Passed: 3
Failed: 3
```

Another AI generation produced:

```text
Total: 5
Passed: 2
Failed: 3
```

The difference is expected because Gemini can generate different test scenarios between runs.

---

# 18. Cypress Integration

The project generates Cypress API tests through:

```text
generator/cypress_generator.py
```

Generated file:

```text
cypress/e2e/generated_api.cy.js
```

Run:

```bat
npx cypress run --spec cypress/e2e/generated_api.cy.js
```

Verified result:

```text
Generated API Tests

√ Health check
√ List users
√ Create user
√ Get user
√ Get user - negative

5 passing
All specs passed!
```

---

# 19. Newman / Postman Integration

The project generates a Postman-compatible collection through:

```text
generator/postman_generator.py
```

Generated collection:

```text
collections/generated.collection.json
```

Run:

```bat
npx newman run collections\generated.collection.json
```

Verified result:

```text
iterations: 1
requests: 5
failed: 0
assertions: 5
```

---

# 20. Reporting

The project generates JSON reports.

Important files:

```text
reports/generated-test-report.json
reports/ai-generated-tests.json
reports/ai-test-report.json
```

The reports contain information such as:

```text
total
passed
failed
test name
method
URL
expected status
actual status
response time
error
```

---

# 21. Flask Backend

The Flask backend is implemented in:

```text
app.py
```

The automation platform runs on:

```text
http://127.0.0.1:5002
```

The sample API being tested runs separately on:

```text
http://127.0.0.1:5001
```

This separation gives the project a clear architecture:

```text
Port 5001 → API Under Test
Port 5002 → Test Automation Platform
```

---

# 22. Flask API Endpoints

## Health

```http
GET /api/health
```

Response:

```json
{
  "status": "ok"
}
```

---

## Generate OpenAPI Tests

```http
POST /api/generate
```

Returns the OpenAPI-generated test cases.

---

## Generate/Get AI Tests

```http
POST /api/ai-generate
```

Returns the AI-generated test cases stored in:

```text
reports/ai-generated-tests.json
```

---

## Run OpenAPI Tests

```http
POST /api/run
```

Executes the standard OpenAPI-generated tests.

---

## Run AI Tests

```http
POST /api/ai-run
```

Executes the AI-generated tests and returns the execution report.

---

# 23. React Dashboard

The frontend is implemented using:

```text
React
Vite
```

Frontend location:

```text
frontend/
```

The dashboard provides:

```text
Generate OpenAPI Tests
Generate AI Tests
Run Tests
```

It displays:

- generation mode
- test count
- test name
- HTTP method
- URL
- reason
- expected status
- total tests
- passed tests
- failed tests
- actual status
- execution result

---

# 24. Dashboard Workflow

```text
Generate OpenAPI Tests
        ↓
Display base tests

Generate AI Tests
        ↓
Display Gemini-generated tests

Run Tests
        ↓
Execute selected test set
        ↓
Display execution report
```

The dashboard therefore provides a visual interface over the underlying Python automation engine.

---

# 25. CORS Integration

The React frontend and Flask backend run on different origins during development.

For example:

```text
React  → localhost:5174
Flask  → 127.0.0.1:5002
```

Flask-CORS is used to allow communication between them.

The backend uses:

```python
from flask_cors import CORS

CORS(app)
```

---

# 26. Unit Testing

Unit tests are located in:

```text
tests/
```

Files:

```text
tests/test_executor.py
tests/test_openapi_generator.py
tests/test_validator.py
```

Run:

```bat
pytest
```

or:

```bat
python -m pytest
```

Verified result:

```text
8 passed
```

Breakdown:

```text
test_executor.py             2 passed
test_openapi_generator.py    3 passed
test_validator.py            3 passed
```

---

# 27. Artifact Generation

`generate_artifacts.py` generates:

```text
Cypress test file
Newman collection
```

Run:

```bat
python generate_artifacts.py
```

Example:

```text
Generated and validated 5 test cases
Cypress file: cypress\e2e\generated_api.cy.js
Newman collection: collections\generated.collection.json
```

---

# 28. Docker

The project contains a Dockerfile for containerizing the API environment.

Example:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5001

CMD ["python", "sample_api.py"]
```

Build:

```bat
docker build -t ai-test-automation .
```

Run:

```bat
docker run --name ai-test-api -p 5001:5001 ai-test-automation
```

---

# 29. GitHub Actions

The project contains:

```text
.github/workflows/ci.yml
```

The CI workflow is intended to automate:

```text
Environment setup
      ↓
Dependency installation
      ↓
API startup
      ↓
Test generation
      ↓
Python tests
      ↓
pytest
      ↓
Cypress
      ↓
Newman
      ↓
Reports
```

---

# 30. Project Structure

```text
AI_test_Automation_platform_V2/
│
├── .github/
│   └── workflows/
│       └── ci.yml
│
├── generator/
│   ├── __init__.py
│   ├── models.py
│   ├── openapi_generator.py
│   ├── executor.py
│   ├── validator.py
│   ├── ai_generator.py
│   ├── cypress_generator.py
│   └── postman_generator.py
│
├── tests/
│   ├── __init__.py
│   ├── test_executor.py
│   ├── test_openapi_generator.py
│   └── test_validator.py
│
├── specs/
│   └── openapi.yaml
│
├── reports/
│   ├── generated-test-report.json
│   ├── ai-generated-tests.json
│   └── ai-test-report.json
│
├── cypress/
│   └── e2e/
│       └── generated_api.cy.js
│
├── collections/
│   └── generated.collection.json
│
├── frontend/
│   └── src/
│       └── App.jsx
│
├── sample_api.py
├── app.py
├── generate_artifacts.py
├── generate_ai_tests.py
├── run_generated_tests.py
├── run_ai_tests.py
├── Dockerfile
├── requirements.txt
└── README.md
```

---

# 31. Running the Project

The project uses three terminals for the complete local setup.

## Terminal 1 — Start the API Under Test

From the project root:

```bat
python sample_api.py
```

This starts the sample API on:

```text
http://127.0.0.1:5001
```

---

## Terminal 2 — Start the Test Automation Backend

From the project root:

```bat
python app.py
```

This starts Flask on:

```text
http://127.0.0.1:5002
```

---

## Terminal 3 — Start the React Frontend

Move into the frontend:

```bat
cd frontend
```

Then:

```bat
npm run dev
```

Open the Vite URL shown in the terminal, for example:

```text
http://localhost:5174
```

---

# 32. Complete Local Workflow

Once all three terminals are running:

```text
Terminal 1
python sample_api.py
        │
        ▼
API Under Test :5001


Terminal 2
python app.py
        │
        ▼
Automation Backend :5002


Terminal 3
cd frontend
npm run dev
        │
        ▼
React Dashboard
```

Then from the dashboard:

```text
Generate OpenAPI Tests
        ↓
Generate AI Tests
        ↓
Run Tests
        ↓
View PASS / FAIL Report
```

---

# 33. CLI Verification Commands

## Generate standard artifacts

```bat
python generate_artifacts.py
```

## Run standard generated tests

```bat
python run_generated_tests.py
```

## Generate AI tests

```bat
python generate_ai_tests.py
```

## Run AI tests

```bat
python run_ai_tests.py
```

## Run unit tests

```bat
python -m pytest
```

## Run Cypress

```bat
npx cypress run --spec cypress/e2e/generated_api.cy.js
```

## Run Newman

```bat
npx newman run collections\generated.collection.json
```

---

# 34. Verified Project Results

The project was successfully verified at multiple levels.

### Standard generated tests

```text
Total : 5
Passed: 5
Failed: 0
```

### Unit tests

```text
8 passed
```

### Cypress

```text
5 passing
All specs passed
```

### Newman

```text
5 requests
0 failed
5 assertions
```

### Gemini

Gemini successfully generated additional API test scenarios.

### AI execution

AI-generated tests successfully executed and produced both PASS and FAIL results, demonstrating expected-vs-actual behavior detection.

---

# 35. Important Design Separation

The project separates the system into distinct responsibilities:

```text
OpenAPI Generator
        ↓
Creates test cases

AI Generator
        ↓
Creates additional test cases

Validator
        ↓
Checks test structure

Executor
        ↓
Runs tests

Reporter
        ↓
Stores results

Flask
        ↓
Exposes automation services

React
        ↓
Provides user interface
```

This separation makes individual components easier to test, replace, and extend.

---

# 36. Future Extensions

The current architecture can be extended with:

- response-body assertions
- JSON schema validation
- authentication-aware testing
- API key/JWT handling
- response-header validation
- response-time assertions
- database validation
- test-history storage
- failure categorization
- automatic bug-report generation
- richer dashboard analytics
- endpoint coverage metrics
- CI/CD quality gates
- larger OpenAPI specifications

---

# 37. Project Summary

The project provides an end-to-end pipeline:

```text
OpenAPI Specification
        ↓
Automatic Test Generation
        ↓
Test Validation
        ↓
Gemini AI Test Expansion
        ↓
HTTP Test Execution
        ↓
Expected vs Actual Comparison
        ↓
PASS / FAIL Reporting
        ↓
Cypress / Newman Integration
        ↓
Flask API
        ↓
React Dashboard
```

The key idea is to combine **deterministic contract-based API testing** with **AI-assisted test scenario generation** while keeping validation and execution under the platform's control.

This allows the project to demonstrate not only AI integration, but also the complete engineering workflow required to turn generated test scenarios into executable, reportable API tests.