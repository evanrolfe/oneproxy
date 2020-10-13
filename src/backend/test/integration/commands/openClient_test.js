const { sleep, clearDatabase, writeToBackend, messageFromBackend, clearDatabaseTable } = require('../../utils');
const { PORTS_AVAILABLE } = require('../../../shared/constants');

describe('openClient Command', () => {
  let result;
  let clientId;

  before(async () => {
    await clearDatabase();
  });

  context('with type = "chrome"', () => {
    before(async () => {
      const proxyPort = PORTS_AVAILABLE.proxy.pop();
      const browserPort = PORTS_AVAILABLE.browser.pop();
      const dbParams = {title: 'Test Client', type: 'chrome', proxy_port: proxyPort, browser_port: browserPort, open: 0};

      const dbResult = await global.knex('clients').insert(dbParams);
      clientId = dbResult[0];

      writeToBackend({ "command": "openClient", "id": clientId });
      result = await messageFromBackend('clientStarted');
    });


    it('updates the row in the database', async () => {
      const dbResult = await global.knex('clients').where({ id: clientId });
      const client = dbResult[0];

      expect(client.open).to.eql(1);
    });


    it('returns the client info', async () => {
      expect(result.clientInfo.id).to.eql(clientId);
      expect(result.clientInfo.browserPort).to.be.a('Number');
      expect(result.clientInfo.proxyPort).to.be.a('Number');
    });
  });
});

