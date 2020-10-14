const readline = require('readline');
const winston = require('winston');
const { combine, timestamp, label, printf } = winston.format;

const { InterceptProc } = require('./intercept/intercept-proc');
const { InterceptClient } = require('./intercept/intercept-client');
const { Client } = require('./client/client');
const { ClientStore } = require('./client/client-store');
const { ProcessStore } = require('./shared/process-store');
const { getPaths } = require('./shared/paths');
const Settings = require('./shared/models/settings');
const CaptureFilters= require('./shared/models/capture-filters');
const { setupDatabaseStore } = require('./shared/database');
const frontend = require('./shared/notify_frontend');

// To Test:
// curl https://linuxmint.com --proxy http://127.0.0.1:8080 --cacert tmp/testCA.pem  --insecure
//
// Example commands:
// {"command": "createClient", "type": "chromium"}
// {"command": "openClient", "id": 1}
// {"command": "listAvailableClientTypes"}
// {"command": "startCrawler"}

// Environment:
if (process.env.NODE_ENV == undefined) {
  process.env.NODE_ENV = 'production';
}

// Logging:
const myFormat = printf(({ level, message, label, timestamp }) => {
  return `[${timestamp}] ${level}: ${message}`;
});
const logger = winston.createLogger({
  level: 'info',
  format: combine(
    timestamp(),
    myFormat
  ),
  transports: [
    new winston.transports.File({ filename: `${process.env.NODE_ENV}.log` }),
  ]
});

// Start sub-processes:
const paths = getPaths();
const clientStore = new ClientStore();
const interceptProc = new InterceptProc();
interceptProc.start();

// Add them to the ProcessStore:
const processStore = new ProcessStore();
processStore.addClientStore(clientStore);
processStore.addProc(interceptProc);
processStore.ensureCleanupOnExit();

const interceptClient = new InterceptClient();

// Handle std input from the frontend:
const handleLine = async (cmd) => {
  try {
    parsedCmd = JSON.parse(cmd);
    let client;

    switch (parsedCmd.command) {
      case 'createClient':
        client = await clientStore.createClient(parsedCmd.type, paths);
        await client.start();
        break;

      case 'openClient':
        client = await clientStore.loadClient(parsedCmd.id, paths);
        await client.start();
        break;

      case 'closeAllClients':
        clientStore.closeAll();
        break;

      case 'listAvailableClientTypes':
        await Client.listTypesAvailable();
        break;

      case 'changeSetting':
        if (parsedCmd.key == 'interceptEnabled' && parsedCmd.value == false) {
          interceptClient.disable();
        }
        Settings.changeSetting(parsedCmd);
        break;

      case 'forward':
        interceptClient.forward(parsedCmd.request);
        break;

      case 'forwardAndIntercept':
        interceptClient.forwardAndIntercept(parsedCmd.request);
        break;

      case 'startCrawler':
        startCrawler();
      break;

      default:
        console.error(`[ERROR] command ${parsedCmd.command} not recognised`);
    }
  } catch (e) {
    console.error(`[ERROR] ${e.message}`);
    return;
  }
};

// Main event loop:
(async () => {
  // Connect to database and ensure the default values exist:
  global.knex = await setupDatabaseStore(paths.dbFile);
  await CaptureFilters.getFilters();
  Settings.createDefaultIfNotExists();

  // Reset clients database table:
  await global.knex('clients').update({ open: false });

  // Connect to the intercept process:
  await interceptClient.connect();

  // Handle input from stdin:
  const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
  });
  rl.on('line', handleLine);

  frontend.notifyBackendLoaded();
})();
