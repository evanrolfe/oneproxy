const { IPC } = require('node-ipc');
const { EventEmitter } = require('events');

const interceptIPC = new IPC();

/*
 * InterceptQueue: communicates with the BrowserInterceptPage on the frontend.
 * It starts an ipc server on the channel "intercept".
 * When a request is intercepted it first sends a "requestIntercepted" message
 * to the client on the proxy IPC channel. It then waits until the a decision
 * message is received on the intercept channel and it will then either
 * forward the request or drop it depending on the message. If a new request is
 * queued while the first one is still waiting for the message from the client,
 * it will wait until that first request has completed to send a new
 * "requestIntercepted" message to the client. And the process repeats...
 */
class InterceptQueue {
  constructor(ipcServer) {
    this.events = new EventEmitter();
    this.requestQueue = [];
    this.awaitingReply = false;
    this.ipcServer = ipcServer;

    this.events.on('requestQueued', async request => {
      if (
        this.awaitingReply === false &&
        this.requestQueue.includes(request.id)
      ) {
        this.awaitingReply = true;

        // Notify the frontend that a request/response has been intercepted:
        let message;
        if (request.rawResponse !== undefined) {
          // A response was intercepted:
          message = {type: 'responseIntercepted', request: request}
        } else {
          // A requested was intercepted:
          message = {type: 'requestIntercepted', request: request}
        }

        console.log(`[JSON] ${JSON.stringify(message)}`)

      } else {
        setTimeout(() => {
          this.events.emit('requestQueued', request);
        }, 100);
      }
    });
  }

  forward(request) {
    console.log(`[InterceptQueue] forwading`);

    this.ipcServer.broadcast({name: 'requestDecisionReceived', args: { request: request, decision: 'forward'} });

    // DeQueue the request:
    this.awaitingReply = false;
    this.requestQueue = this.requestQueue.filter(id => id !== request.id);
  }

  forwardAndIntercept(request) {
    console.log(`[InterceptQueue] forwading and intercepting response`);

    this.ipcServer.broadcast({name: 'requestDecisionReceived', args: { request: request, decision: 'forwardAndIntercept'} });

    // Dequeue the request:
    this.awaitingReply = false;
    this.requestQueue = this.requestQueue.filter(id => id !== request.id);
  }

  disable() {
    console.log(`[InterceptQueue] disabling the request queue...`);
    this.clearQueue();
  }

  enqueue(request) {
    this.requestQueue.push(request.id);
    this.events.emit('requestQueued', request);
  }

  clearQueue() {
    // Forward all the requests and clear the queue:
    console.log(
      `[InterceptQueue] clearing queue of requests: ${JSON.stringify(
        this.requestQueue
      )}`
    );
    this.requestQueue.forEach(requestId => {
      this.forward({id: requestId});
    });
  }
}

module.exports = { InterceptQueue };
