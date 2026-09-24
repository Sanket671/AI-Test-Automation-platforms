describe('Generated API Tests', () => {
  it("Health check", () => {
    cy.request({
      method: 'GET',
      url: "http://127.0.0.1:5001/health",
      failOnStatusCode: false
    }).then((response) => {
      expect(response.status).to.eq(200);
    });
  });
  it("List users", () => {
    cy.request({
      method: 'GET',
      url: "http://127.0.0.1:5001/users",
      failOnStatusCode: false
    }).then((response) => {
      expect(response.status).to.eq(200);
    });
  });
  it("Create user", () => {
    cy.request({
      method: 'POST',
      url: "http://127.0.0.1:5001/users",
      body: {"name": "Test User"},
      failOnStatusCode: false
    }).then((response) => {
      expect(response.status).to.eq(201);
    });
  });
  it("Get user", () => {
    cy.request({
      method: 'GET',
      url: "http://127.0.0.1:5001/users/1",
      failOnStatusCode: false
    }).then((response) => {
      expect(response.status).to.eq(200);
    });
  });
  it("Get user - negative", () => {
    cy.request({
      method: 'GET',
      url: "http://127.0.0.1:5001/users/999999",
      failOnStatusCode: false
    }).then((response) => {
      expect(response.status).to.eq(404);
    });
  });
});