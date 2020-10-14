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
}

module.exports = { ProcessStore };
