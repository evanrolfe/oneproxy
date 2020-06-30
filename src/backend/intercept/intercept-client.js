const { IPCClient } = require('../intercept/ipc-client');

class InterceptClient {
  constructor() {
    this.ipcClient = new IPCClient('oneproxy-intercept');
  }

  async connect() {
    await this.ipcClient.connect();
  }

  async decisionForRequest(request) {
    const params = request.toInterceptParams();
    this.ipcClient.send({type: 'queueInterceptedRequest', request: params});

    const decision = await this._decisionForRequest(request.id);
    console.log(`[Proxy] received a decision from intercept for request ${request.id} - ${decision}`)

    return decision;
  }

  async decisionForResponse(reqResPair) {
    const params = reqResPair.toInterceptParams();
    this.ipcClient.send({type: 'queueInterceptedRequest', request: params});

    const decision = await this._decisionForRequest(reqResPair.id);
    console.log(`[Proxy] received a decision from intercept for request ${reqResPair.id} - ${decision}`)

    return decision;
  }

  disable() {
    this.ipcClient.send({type: 'disable'});
  }

  forward(request) {
    this.ipcClient.send({type: 'forward', request: request});
  }

  forwardAndIntercept(request) {
    this.ipcClient.send({type: 'forwardAndIntercept', request: request});
  }

  _decisionForRequest(requestId) {
    console.log(`[Proxy] awaiting decision from intercept for request ID ${requestId}...`)
    return new Promise((resolve) => {
      this.ipcClient.listen('requestDecisionReceived', (args) => {
        console.log(`[Proxy] received requestDecisionReceived: ${JSON.stringify(args)}`)
        if (args.request.id == requestId) {
          resolve(args);
        }
      });
    });
  }
}

module.exports = { InterceptClient };
