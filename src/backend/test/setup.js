const { expect } = require('chai');
const { spawn } = require('child_process');
const { getPaths } = require('../shared/paths');
const { setupDatabaseStore } = require('../shared/database');
const { sleep, writeToBackend } = require('./utils');
const { ensureBackendIsKilled } = require('./support/ensure_backend_is_killed');
const { checkServerIsRunning } = require('./support/check_server_is_running');

global.expect = expect;

const paths = getPaths();

const spawnBackend = async () => {
    console.log('[TEST] Spawning backend process...');

    const backendProc = spawn('npm', ['run', 'backend-test'], {
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

    // HACK: Currently backendProc does not know when the backend has finished
    // loading, so we just sleep and hope for the best. Adjust this as needed.
    // TODO: Find a better way, perhaps by checking stdout for the word "loaded",
    // or maybe have the backend send an IPC messsage "loaded"?
    // NOTE: This can cause intermittent failures if the backend doesn't finish
    // loading within 2secs
    await sleep(2000);

    // Ensure the backend is killed when the test exits:
    ensureBackendIsKilled(backendProc.pid);

    return backendProc;
};

before(async () => {
  await checkServerIsRunning();

  global.backendProc = await spawnBackend();
  console.log(`[TEST] Backend process spawned.`);

  global.knex = await setupDatabaseStore(paths.dbFile);
  console.log(`[TEST] Connected to database.`);
});

after(() => {
    // See this: https://azimi.me/2014/12/31/kill-child_process-node-js.html
    process.kill(-global.backendProc.pid);
    global.knex.destroy();
});
