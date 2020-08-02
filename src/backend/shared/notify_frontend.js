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
  const message = {
    type: 'updatedRequest',
    request: {
      id: reqResPair.id,
      client_id: reqResPair.clientId,
      method: reqResPair.request.method,
      host: reqResPair.request.host,
      path: reqResPair.request.path,
      status: reqResPair.response.statusCode,
      encrypted: reqResPair.request.encrypted,
    }
  }
  console.log(`[JSON] ${JSON.stringify(message)}`)
};

module.exports = { notifyNewRequest, notifyUpdatedRequest };
