const nodifyFrontend = () => {

};

const notifyNewRequest = (reqResPair) => {
  const message = {
    type: 'newRequest',
    request: {
      id: reqResPair.id,
      client_id: reqResPair.clientId,
      method: reqResPair.request.method,
      url: reqResPair.request.url
    }
  }
  console.log(`[JSON] ${JSON.stringify(message)}`)
};

module.exports = { notifyNewRequest };
