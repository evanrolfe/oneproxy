const notifyNewRequest = (reqResPair) => {
  const message = {
    type: 'newRequest',
    request: {
      id: reqResPair.id,
      client_id: reqResPair.clientId,
      method: reqResPair.request.method,
      host: reqResPair.request.host,
      path: reqResPair.request.path,
      encrypted: reqResPair.request.encrypted,
      request_type: reqResPair.request.requestType,
    }
  }
  console.log(`[JSON] ${JSON.stringify(message)}`)
};

const notifyUpdatedRequest = (reqResPair) => {
  const request = {
    id: reqResPair.id,
    client_id: reqResPair.clientId,
    method: reqResPair.request.method,
    host: reqResPair.request.host,
    path: reqResPair.request.path,
    encrypted: reqResPair.request.encrypted,
    request_type: reqResPair.request.requestType,
  };

  if (reqResPair.response !== undefined) {
    request.response_status = reqResPair.response.statusCode;
    request.encrypted = reqResPair.request.encrypted;
    request.request_modified = reqResPair.requestModified() ? 1 : 0;
    request.response_modified = reqResPair.responseModified() ? 1 : 0;
  }

  const message = { type: 'updatedRequest', request: request };
  console.log(`[JSON] ${JSON.stringify(message)}`)
};

const notifyClientsChanged = () => {
  const message = { type: 'clientsChanged' }
  console.log(`[JSON] ${JSON.stringify(message)}`)
};

const notifyClientStarted = (clientInfo) => {
  const message = { type: 'clientStarted', clientInfo: clientInfo }
  console.log(`[JSON] ${JSON.stringify(message)}`)
};

const notifyClientsClosed = () => {
  const message = { type: 'clientsClosed' }
  console.log(`[JSON] ${JSON.stringify(message)}`)
};

const notifyBackendLoaded = () => {
  const message = { type: 'backendLoaded' }
  console.log(`[JSON] ${JSON.stringify(message)}`)
};

const notifyCrawlStarted = () => {
  const message = { type: 'crawlStarted' }
  console.log(`[JSON] ${JSON.stringify(message)}`)
};

const notifyCrawlFinished = () => {
  const message = { type: 'crawlFinished' }
  console.log(`[JSON] ${JSON.stringify(message)}`)
};

module.exports = {
  notifyNewRequest,
  notifyUpdatedRequest,
  notifyClientsChanged,
  notifyClientStarted,
  notifyClientsClosed,
  notifyBackendLoaded,
  notifyCrawlStarted,
  notifyCrawlFinished
};
