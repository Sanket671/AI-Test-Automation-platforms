describe('Sample API regression tests', () => {
  it('GET /health returns 200', () => {
    cy.request('/health').then((response) => {
      expect(response.status).to.eq(200);
      expect(response.body.status).to.eq('ok');
    });
  });

  it('GET /users returns an array', () => {
    cy.request('/users').then((response) => {
      expect(response.status).to.eq(200);
      expect(response.body).to.be.an('array');
    });
  });

  it('POST /users validates required name', () => {
    cy.request({
      method: 'POST',
      url: '/users',
      body: {},
      failOnStatusCode: false,
    }).then((response) => {
      expect(response.status).to.eq(400);
    });
  });
});
