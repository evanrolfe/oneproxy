const { fork } = require('child_process');

class ProxyProc {
  constructor(clientData, paths) {
    this.clientData = clientData;
    this.paths = paths;
  }

  async start() {
    this.proc = fork(require.resolve('./index'), [
      '--port', this.clientData.proxyPort,
      '--clientId', this.clientData.id,
      '--paths', JSON.stringify(this.paths)
    ]);
    this.pid = this.proc.pid;

    console.log(`[Backend] Proxy started with PID: ${this.pid}`)
  }
}

module.exports = { ProxyProc };
