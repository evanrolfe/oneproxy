const { fork } = require('child_process');

class Proxy {
  constructor(clientData, paths) {
    this.clientData = clientData;
    this.paths = paths;
  }

  async start() {
    this.proxyProc = fork(require.resolve('../proxy/index'), [
      '--port', this.clientData.proxyPort,
      '--clientId', this.clientData.id,
      '--paths', JSON.stringify(this.paths)
    ]);
    this.pid = this.proxyProc.pid;

    console.log(`[Backend] Proxy started with PID: ${this.pid}`)
  }
}

module.exports = { Proxy };
