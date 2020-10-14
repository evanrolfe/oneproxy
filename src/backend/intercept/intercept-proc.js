const { fork } = require('child_process');

class InterceptProc {
  async start() {
    this.proc = fork(require.resolve('./index'));
    this.pid = this.proc.pid;

    console.log(`[Backend] Intercept started with PID: ${this.pid}`)
  }
}

module.exports = { InterceptProc };
