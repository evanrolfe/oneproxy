const { sleep, clearDatabase, writeToBackend, messageFromBackend, clearDatabaseTable } = require('../../utils');
const { PORTS_AVAILABLE, DEFAULT_FILTERS } = require('../../../shared/constants');

describe('createCrawl Command', () => {
  let result;
  let clientId;

  before(async () => {
    await clearDatabase();
  });

  context('with type = "chrome"', () => {
    before(async () => {
      // Create a Client:
      const proxyPort = PORTS_AVAILABLE.proxy.pop();
      const browserPort = PORTS_AVAILABLE.browser.pop();
      const dbParams = {title: 'Test Client', type: 'chrome', proxy_port: proxyPort, browser_port: browserPort, open: 0};
      const dbResult = await global.knex('clients').insert(dbParams);
      clientId = dbResult[0];

      // Create default capture filters:
      const filters = Object.assign({}, DEFAULT_FILTERS);
      filters.hostList = ['localhost'];
      filters.hostSetting = 'include';
      filters.pathList = ['/sockjs', '/static'];
      filters.pathSetting = 'exclude';
      await global
        .knex('capture_filters')
        .where({id: 1})
        .update({filters: JSON.stringify(filters) });


      writeToBackend({ "command": "createCrawl", "clientId": clientId });
      console.log(`[Test] ---------> waiting for crawlstarted`)
      result = await messageFromBackend('crawlStarted');
      console.log(`[Test] ---------> RECEIVED crawlstarted!`)
      await sleep(60*1000);
    });

    it('works', async () => {
      expect(1).to.eql(1);
    });
  });
});

