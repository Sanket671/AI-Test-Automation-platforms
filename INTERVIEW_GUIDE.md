# Interview Guide — What Each Resume Phrase Means

## 1. API testing
An API is an interface that lets one program talk to another over HTTP. Testing an API means sending requests and checking that the response is correct.

Example:

GET /users -> expect HTTP 200 and a JSON array.
POST /users -> send JSON -> expect HTTP 201 and a new id.

## 2. Test case
A test case is a small, explicit check:

- Input: HTTP method, URL, headers/body
- Expected result: status code/body/headers/behavior

## 3. Assertion
An assertion is the statement that decides pass/fail.

Example:

expect(response.status).to.eq(200)

## 4. Cypress
Cypress is a JavaScript test runner. It can call REST APIs directly with `cy.request()` and assert on the response. See the official Cypress API testing documentation.

## 5. Newman
Newman is the command-line runner for Postman Collections. A collection can contain requests plus JavaScript assertions. Newman can be run locally or in CI.

## 6. OpenAPI
OpenAPI is a machine-readable description of an HTTP API: paths, operations, parameters, request bodies, responses, and schemas. The platform reads that description and turns it into candidate tests.

## 7. GenAI-assisted generation
The user provides a workflow in natural language. An LLM converts that description into structured test cases. Structured JSON is safer than asking the model to emit arbitrary JavaScript.

Example input:

"Create a user with a name, verify the API returns 201, then request the created user and verify 200. Also test missing-name validation."

Example output shape:

```json
{
  "tests": [
    {
      "name": "Create user",
      "method": "POST",
      "url": "http://127.0.0.1:5001/users",
      "expected_status": 201,
      "body": {"name": "Test User"}
    }
  ]
}
```

## 8. Regression testing
A regression suite is a set of previously-defined tests that are run again after changes to make sure existing behavior still works.

## 9. Docker
Docker packages the application and its dependencies into an image. A container is a running instance of that image. This MVP containerizes the Python platform service; CI installs the test runners separately.

## 10. GitHub Actions / CI/CD
GitHub Actions runs a workflow automatically on events such as a push or pull request. This project uses CI to install dependencies, run unit tests, start the sample API, run Newman, and run Cypress.

## 11. Why both Newman and Cypress?
They overlap for API checks but serve different purposes.

- Newman is a convenient CLI runner for a Postman Collection and is easy to run as a regression command in CI.
- Cypress gives JavaScript-based API tests and can use the same framework for future UI tests.

In a larger product I would choose a clearer testing strategy; for a small portfolio MVP, both demonstrate two common ways of automating API tests.

## 12. Honest scope
This is an MVP. It is not a full enterprise SaaS with authentication, multi-tenancy, billing, queues, distributed workers, secrets management, and observability.

The interview-safe description is: "I built a working prototype that converts workflow/OpenAPI input into executable API tests and runs them through automated test runners and CI."
