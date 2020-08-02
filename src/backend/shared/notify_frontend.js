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

module.exports = { notifyNewRequest };
