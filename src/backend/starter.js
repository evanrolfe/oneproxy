const { fork } = require('child_process');

const { Crawler } = require('./crawler/crawler');
const { BaseConfig } = require('./crawler/config/base-config.js');
const { startProxyServer } = require('./proxy/proxy-server');
const { startBrowser, createBrowserDb, listAvailableBrowsers, getNextPortsAvailable } = require('./browser/index');
const { setupDatabaseStore } = require('./shared/database');
const CaptureFilters = require('./shared/models/capture-filters');
const { generateCertsIfNotExists } = require('./shared/cert-utils');
const frontend = require('./shared/notify_frontend');

// TODO: Use classes to organise this mess of functions in here and in browser/index.js

const loadDatabase = async (paths) => {
  global.knex = await setupDatabaseStore(paths.dbFile);
  // Ensure the default capture filters are created if they dont exist:
  await CaptureFilters.getFilters();
};

const startIntercept = () => {
  const interceptProc = fork(require.resolve('./intercept/index'));

  console.log(`[Backend] Intercept started with PID: ${interceptProc.pid}`)
  return interceptProc;
};

const startProxy = (client, paths) => {
  const proxyProc = fork(require.resolve('./proxy/index'), [
    '--port', client['proxy_port'],
    '--clientId', client['id'],
    '--paths', JSON.stringify(paths)
  ]);
  console.log(`[Backend] Proxy started with PID: ${proxyProc.pid}`)
  return proxyProc;
};

const getClientDb = async (clientId) => {
  const result = await global.knex('clients').where({ id: clientId });
  const browser = result[0];

  return browser;
};

const createClient = async (paths, portsAvailable, browserType) => {
  const ports = await getNextPortsAvailable(portsAvailable);
  const clientId = await createBrowserDb(browserType, ports.browser, ports.proxy);
  const client = await getClientDb(clientId);

  startProxyAndBrowser(client, paths);
};

const openClient = async (paths, clientId) => {
  console.log(`Opening client ${clientId}`);
  const client = await getClientDb(clientId);

  if (client === undefined) {
    console.error(`[Backend] could not find client with id ${clientId}`)
    return;
  }

  startProxyAndBrowser(client, paths);
};

const startProxyAndBrowser = async (client, paths) => {
  await generateCertsIfNotExists(paths.keyPath, paths.certPath);

  const proxyProc = startProxy(client, paths);
  global.childrenPIds.push(proxyProc.pid);
  let browserPid;

  if (client['type'] !== 'anything') {
    browserPid = await startBrowser(client, paths, proxyProc.pid);
    global.childrenPIds.push(browserPid);
  }

  await global.knex('clients').where({ id: client.id }).update({ open: true });

  frontend.notifyClientsChanged();
  frontend.notifyClientStarted({browserPort: client.browser_port, proxyPort: client.proxy_port});
};

const startCrawler = async () => {
  const configArgs = {
    "baseUrl": "http://localhost",
    "clickButtons": false,
    "buttonXPath": 'button',
    "maxDepth": 3,
    "xhrTimeout": 5,
    "pageTimeout": 30,
    "verboseOutput": true,
    "headless": false,
    "ignoreLink": function(url) {
      if(url.includes('/users/sign_out')) {
        return true;
      }

      return false;
    },
    "ignoreButton": function(outerHTML) {
      if(outerHTML.includes('Logout') || outerHTML.includes('submit') || outerHTML.includes('Save')) {
        return true;
      }

      return false;
    }
  };

  const config = new BaseConfig(configArgs);
  const crawler = await Crawler.init({config: config});

  console.log(`======================> Crawling`)
  // await crawler.startCrawling();
  // console.log('Crawling...')
  // await crawler.onIdle();
  // console.log('Done crawling.')
  //await crawler.close();
  //return;
};

module.exports = { loadDatabase, createClient, openClient, startIntercept, startCrawler };
