const { IPCClient } = require('../intercept/ipc-client');

class InterceptClient {
  constructor() {
    this.ipcClient = new IPCClient('oneproxy-intercept');
  }

  async connect() {
    await this.ipcClient.connect();
  }

  async decision(request) {
    const requestParams = request.toInterceptParams();
    this.ipcClient.send({type: 'queueInterceptedRequest', request: requestParams});

    const decision = await this._decisionForRequest(request.id);
    console.log(`[Proxy] received a decision from intercept for request ${request.id} - ${decision}`)

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
/*
const decisionFromIntercept = async (parsedRequest, ipcClient) => {
  const requestForIntercept = parsedRequest.toInterceptParams();

  //ipcClient.send({type: 'requestIntercepted', request: requestForIntercept});
  return 'forward';

  global.interceptServer.queueRequest(requestForIntercept);
  const result = await global.interceptServer.decisionFromClient(
    requestForIntercept
  );

  // If you press "disable intercept", then there will be no result.request
  if (result.request === undefined) return result.action;

  if (result.action === 'forward' && result.request.rawRequest !== undefined) {
    parsedRequest.setRawRequest(result.request.rawRequest);
  }

  if (result.action === 'respond' && result.request.rawResponse !== undefined) {
    parsedRequest.setRawResponse(
      result.request.rawResponse,
      result.request.rawResponseBody
    );
  }

  return result.action;
};
*/
module.exports = { InterceptClient };
