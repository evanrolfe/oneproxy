const { expect } = require('chai');
const fs = require('fs');
const { spawn } = require('child_process');
const path = require('path');

const { setupDatabaseStore } = require('../shared/database');
const { messageFromBackend, clearDatabaseTable } = require('./utils');
const { ensureBackendIsKilled } = require('./support/ensure_backend_is_killed');
const { checkServerIsRunning } = require('./support/check_server_is_running');
const { ClientGetter } = require('./support/clientGetter')

global.expect = expect;

const DATABASE_TABLES = [
  'capture_filters',
  'clients',
  'crawls',
  'intercept_filters',
  'requests',
  'settings',
  'websocket_messages',
];

const dbPath = path.join(__dirname, './test.db');

const spawnBackend = async () => {
  console.log('[TEST] Spawning backend process...');

  const backendProc = spawn('npm', ['run', 'backend-test', '--', `--dbPath=${dbPath}`], {
      shell: true,
      env: process.env,
      detached: true
  })
    .on('close', code => process.exit(code))
    .on('error', spawnError => console.error(spawnError));

  backendProc.stdout.pipe(process.stdout);
  backendProc.stderr.pipe(process.stderr);

  backendProc.stdout.setEncoding('utf-8');
  backendProc.stdin.setEncoding('utf-8');

  global.backendProc = backendProc;
  global.clientGetter = new ClientGetter();
  await messageFromBackend('backendLoaded')

  // Ensure the backend is killed when the test exits:
  ensureBackendIsKilled(backendProc.pid);

  return backendProc;
};

before(async () => {
  await checkServerIsRunning();
  await spawnBackend();
  console.log(`[TEST] Backend process spawned.`);

  global.knex = await setupDatabaseStore(dbPath);
  console.log(`[TEST] Connected to database.`);
});

after(async () => {
  for(let i =0; i< DATABASE_TABLES.length; i++) {
    const tableName = DATABASE_TABLES[i];
    await clearDatabaseTable(tableName);
  }

  // See this: https://azimi.me/2014/12/31/kill-child_process-node-js.html
  process.kill(-global.backendProc.pid);
  global.knex.destroy();
});
