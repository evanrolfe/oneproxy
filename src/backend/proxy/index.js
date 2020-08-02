const { argv } = require('yargs');

const { InterceptClient } = require('../intercept/intercept-client');
const { setupDatabaseStore } = require('../shared/database');
const { startProxyServer } = require('./proxy-server');

const paths = JSON.parse(argv.paths);
const clientId = argv.clientId;
const port = argv.port;
const interceptClient = new InterceptClient();

(async () => {
  console.log(`[Proxy] starting`)
  await interceptClient.connect();
  global.knex = await setupDatabaseStore(paths.dbFile);
  startProxyServer(port, clientId, interceptClient, paths);
})();
