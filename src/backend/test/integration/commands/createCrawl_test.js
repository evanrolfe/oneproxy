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
      let dbParams = {title: 'Test Client', type: 'chrome', proxy_port: proxyPort, browser_port: browserPort, open: 0};
      let dbResult = await global.knex('clients').insert(dbParams);
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

      // Create a crawl:
      const crawlConfig = {
        "baseUrl": "http://localhost:3000",
        "clickButtons": false,
        "buttonXPath": 'button',
        "maxConcurrency": 10,
        "maxDepth": 2,
        "xhrTimeout": 5,
        "pageTimeout": 30,
        "waitOnEachPage": 3000,
        "verboseOutput": false,
        "headless": false,
        "ignoreLinksIncluding": ["/users/sign_out"],
        "ignoreButtonsIncluding": ['Logout', 'submit', 'Save'],
      };
      dbParams = { config: JSON.stringify(crawlConfig), status: 'created', client_id: clientId };
      dbResult = await global.knex('crawls').insert(dbParams);
      const crawlId = dbResult[0];

      writeToBackend({ "command": "createCrawl", "crawlId": crawlId, "clientId": clientId });

      result = await messageFromBackend('crawlStarted');
      await messageFromBackend('crawlFinished');

      console.log(`[Test] Crawl finished.`)
    });

    it('works', async () => {
      expect(1).to.eql(1);
    });
  });
});

