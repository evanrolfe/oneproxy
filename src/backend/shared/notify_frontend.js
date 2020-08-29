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
    path: reqResPair.request.path
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

module.exports = { notifyNewRequest, notifyUpdatedRequest, notifyClientsChanged };
