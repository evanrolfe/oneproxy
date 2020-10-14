const { killProcGracefully } = require('./utils');

// Stores all the sub-processes spawned by the backend (proxies, browsers, intercept etc.)
class ProcessStore {
  constructor() {
    this.procs = [];
  }

  addClientStore(clientStore) {
    this.clientStore = clientStore;
  }

  addProc(proc) {
    this.procs.push(proc);
  }

  killAll() {
    console.log(`[Backend] ProcessStore.killAll()`)

    this.clientStore.closeAll();

    this.procs.forEach((proc) => {
      killProcGracefully(proc.pid);
    })
  }

  // Ensure that the process on exit callback is always ran when the backend proc is closed
  ensureCleanupOnExit() {
    const events = [
        `SIGINT`,
        `SIGUSR1`,
        `SIGUSR2`,
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
      //logger.info(`[Backend] shutting down...`);

      this.killAll();
      if(global.knex) global.knex.destroy();

      console.log(`[Backend] shutdown complete.`)
    });
  }
}

module.exports = { ProcessStore };
