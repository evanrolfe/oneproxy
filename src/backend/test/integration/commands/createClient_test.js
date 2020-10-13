const { sleep, clearDatabase, writeToBackend, messageFromBackend, clearDatabaseTable } = require('../../utils');

describe('createClient Command', () => {
  let result;

  before(async () => {
    await clearDatabase();
  });

  context('with type = "chrome"', () => {
    before(async () => {
      writeToBackend({ "command": "createClient", "type": 'chrome' });
      result = await messageFromBackend('clientStarted');
    });

    it('creates a row in the database', async () => {
      const dbResult = await global.knex('clients').where({ id: result.clientInfo.id });
      const client = dbResult[0];

      expect(client.type).to.eql('chrome');
      expect(client.open).to.eql(1);
      expect(client.browser_port).to.be.a('Number');
      expect(client.proxy_port).to.be.a('Number');
    });

    it('returns the client info', async () => {
      expect(result.clientInfo.id).to.be.a('Number');
      expect(result.clientInfo.browserPort).to.be.a('Number');
      expect(result.clientInfo.proxyPort).to.be.a('Number');
    });
  });

  context('with type = "anything"', () => {
    before(async () => {
      writeToBackend({ "command": "createClient", "type": 'anything' });
      result = await messageFromBackend('clientStarted');
    });

    it('creates a row in the database', async () => {
      const dbResult = await global.knex('clients').where({ id: result.clientInfo.id });
      const client = dbResult[0];

      expect(client.type).to.eql('anything');
      expect(client.open).to.eql(1);
      expect(client.browser_port).to.be.a('Number');
      expect(client.proxy_port).to.be.a('Number');
    });

    it('returns the client info', async () => {
      expect(result.clientInfo.id).to.be.a('Number');
      expect(result.clientInfo.browserPort).to.be.a('Number');
      expect(result.clientInfo.proxyPort).to.be.a('Number');
    });
  });
});

