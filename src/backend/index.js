const readline = require('readline');
const { exec } = require('child_process');
const winston = require('winston');
const { combine, timestamp, label, printf } = winston.format;

const { InterceptClient } = require('./intercept/intercept-client');
const { listAvailableBrowsers, closeAllClients } = require('./browser/index');
const { loadDatabase, createClient, openClient, startIntercept, startCrawler } = require('./starter');
const { getPaths } = require('./shared/paths');
const Settings = require('./shared/models/settings');

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

const paths = getPaths();
const portsAvailable = {
  proxy: [8080, 8081, 8082, 8083, 8084, 8085, 8086, 8087, 8088, 8089, 8090],
  browser: [9222, 9223, 9224, 9225, 9226, 9227, 9228, 9229, 9230, 9231, 9232]
};

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout
});

const interceptClient = new InterceptClient();

// Handle std input from the frontend:
const handleLine = (cmd) => {
  try {
    parsedCmd = JSON.parse(cmd);

    switch (parsedCmd.command) {
      case 'createClient':
        createClient(paths, portsAvailable, parsedCmd.type);
        break;

      case 'openClient':
        openClient(paths, parsedCmd.id);
        break;

      case 'closeAllClients':
        closeAllClients();
        break;

      case 'listAvailableClientTypes':
        listAvailableBrowsers(portsAvailable);
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

(async () => {
  const interceptProc = startIntercept();
  global.interceptPId = interceptProc.pid;

  await loadDatabase(paths);
  Settings.createDefaultIfNotExists();

  // Reset clients database table:
  await global.knex('clients').update({ open: false });

  await interceptClient.connect();
  rl.on('line', handleLine);

  console.log(`[JSON] ${JSON.stringify({type: 'backendLoaded'})}`);
})();

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
