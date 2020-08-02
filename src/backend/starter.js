const { fork } = require('child_process');

const { startProxyServer } = require('./proxy/proxy-server');
const { startBrowser, createBrowserDb, listAvailableBrowsers, getNextPortsAvailable } = require('./browser/index');
const { setupDatabaseStore } = require('./shared/database');
const { generateCertsIfNotExists } = require('./shared/cert-utils');

const loadDatabase = async (paths) => {
  global.knex = await setupDatabaseStore(paths.dbFile);
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

const logClientsChanged = () => {
  const message = {type: 'clientsChanged'};
  console.log(`[JSON] ${JSON.stringify(message)}`);
};

const createClient = async (paths, portsAvailable, browserType) => {
  const ports = await getNextPortsAvailable(portsAvailable);
  const clientId = await createBrowserDb(browserType, ports.browser, ports.proxy);
  const client = await getClientDb(clientId);

  logClientsChanged();
  startProxyAndBrowser(client, paths);
};

const openClient = async (paths, clientId) => {
  console.log(`Opening client ${clientId}`);
  const client = await getClientDb(clientId);

  if (client === undefined) {
    console.error(`[Backend] could not find client with id ${clientId}`)
    return;
  }

  logClientsChanged();
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

  const message = {
    type: 'clientStarted',
    clientInfo: {
      browserPid: browserPid,
      proxyPid: proxyProc.pid,
      browserPort: client['browser_port'],
      proxyPort: client['proxy_port']
    }
  };
  console.log(`[JSON] ${JSON.stringify(message)}`);
};

module.exports = { loadDatabase, createClient, openClient, startIntercept };
