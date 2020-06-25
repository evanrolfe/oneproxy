const { IPCServer } = require('./ipc-server');
const { InterceptQueue } = require('./intercept-queue');

class InterceptServer {
  constructor() {
    this.ipcServer = new IPCServer('oneproxy-intercept');
    this.interceptQueue = new InterceptQueue(this.ipcServer);
  }

  start() {
    console.log(`[Intercept] starting...`)

    this.ipcServer.start();
    this.ipcServer.onMessage(this._handleMessage.bind(this));
  }

  _handleMessage(message, reply) {
    console.log(`[Intercept] Received message type: ${message.type}`);

    try {
      switch (message.type) {
        case 'queueInterceptedRequest':
          this._queueInterceptedRequest(message, reply);
          break;

        case 'forward':
          this._forward(message, reply);
          break;

        case 'forwardAndIntercept':
          this._forwardAndIntercept(message, reply);
          break;

        case 'disable':
          this._disable(message, reply);
          break;

        default:
          console.error(`[ERROR] Intercept command ${message.type} not recognised`);
      }
    } catch(err) {
      console.error(`[ERROR] ${err.message}`);
      throw err;
    }
  }

  // Actions:
  _queueInterceptedRequest(message, reply) {
    this.interceptQueue.enqueue(message.request);
    reply({'status': 'queued'});
  }

  _forward(message, reply) {
    this.interceptQueue.forward(message.request);
    reply({'status': 'OK'});
  }

  _forwardAndIntercept(message, reply) {
    this.interceptQueue.forwardAndIntercept(message.request);
    reply({'status': 'OK'});
  }

  _disable(_message, reply) {
    this.interceptQueue.disable();
    reply({'status': 'OK'});
  }
}

module.exports = { InterceptServer };
