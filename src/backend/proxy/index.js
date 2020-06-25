const { argv } = require('yargs');

const { InterceptClient } = require('../intercept/intercept-client');
const { setupDatabaseStore } = require('../shared/database');
const { startProxyServer } = require('./proxy-server');

const paths = JSON.parse(argv.paths);
const clientId = argv.clientId;
const port = argv.port;
const interceptClient = new InterceptClient();

(async () => {
  console.log(`[Proxy] ========================> starting`)
  await interceptClient.connect();
  console.log(`[Proxy] ========================> connected to intercept.`)
  global.knex = await setupDatabaseStore(paths.dbFile);
  console.log(`[Proxy] ========================> conntected to DB`)
  startProxyServer(port, clientId, interceptClient, paths);
})();
