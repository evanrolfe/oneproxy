const readline = require('readline');
const { fork } = require('child_process');
const winston = require('winston');
const { combine, timestamp, label, printf } = winston.format;

const { InterceptClient } = require('./intercept/intercept-client');
const { Client } = require('./client/client');
const { ClientStore } = require('./client/client-store');
const { getPaths } = require('./shared/paths');
const Settings = require('./shared/models/settings');
const CaptureFilters= require('./shared/models/capture-filters');
const { setupDatabaseStore } = require('./shared/database');

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

// Contains the PIds of all proxy & browser processes:
global.childrenPIds = [];
global.interceptPId;
const closeAllClients = () => {
  global.childrenPIds.forEach((pid) => {
    console.log(`[Backend] closing client with PID: ${pid}`)
    process.kill(pid);
    console.log(`[Backend] ${pid} closed`)
  });
};

const paths = getPaths();
const interceptClient = new InterceptClient();
const clientStore = new ClientStore();

// Handle std input from the frontend:
const handleLine = async (cmd) => {
  try {
    parsedCmd = JSON.parse(cmd);
    let client;

    switch (parsedCmd.command) {
      case 'createClient':
        client = await Client.create(parsedCmd.type, paths);
        await client.start();
        break;

      case 'openClient':
        client = await Client.load(parsedCmd.id, paths);
        await client.start();
        break;

      case 'closeAllClients':
        closeAllClients();
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
const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout
});

(async () => {
  const interceptProc = fork(require.resolve('./intercept/index'));
  console.log(`[Backend] Intercept started with PID: ${interceptProc.pid}`)
  global.interceptPId = interceptProc.pid;

  global.knex = await setupDatabaseStore(paths.dbFile);
  // Ensure the default capture filters are created if they dont exist:
  await CaptureFilters.getFilters();
  Settings.createDefaultIfNotExists();

  // Reset clients database table:
  await global.knex('clients').update({ open: false });

  await interceptClient.connect();
  rl.on('line', handleLine);

  console.log(`[JSON] ${JSON.stringify({type: 'backendLoaded'})}`);
})();

// Kill all sub-processes gracefully on exit:
const events = [
    `SIGINT`,
    `SIGUSR1`,
    `SIGUSR2`,
    `uncaughtException`,
    `SIGTERM`,
    `SIGHUP`
  ];

for (let i = 0; i < events.length; i++) {
  const eventType = events[i];
  process.on(eventType, () => {
    console.log(`[Backend] received event: ${eventType}`);
    process.exit(1);
  });
}

process.on('exit', async () => {
  // NOTE: loggging here doesn't work well see:
  // https://github.com/winstonjs/winston/issues/1629
  logger.info(`[Backend] Closing with client PIDS: ${JSON.stringify(global.childrenPIds)}`);

  global.childrenPIds.forEach((pid) => {
    try {
      process.kill(pid);
    } catch(err) {
      console.log(`[Backend] could not kill child process ${pid} - ${err.message}`)
    }
  });

  try {
    process.kill(global.interceptPId);
  } catch(err) {
    console.log(`[Backend] could not kill intercept process ${pid} - ${err.message}`)
  }

  global.knex.destroy();

  console.log(`[Backend] shutdown complete.`)
});
