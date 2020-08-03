// eslint-disable-next-line no-unused-vars
const http = require('http');
// eslint-disable-next-line no-unused-vars
const https = require('https');
const zlib = require('zlib');

const RequestResponsePair = require('../shared/models/request-response-pair');
const Settings = require('../shared/models/settings');

const interceptEnabled = async () => {
  const setting = await Settings.getSetting('interceptEnabled');
  return setting.value === '1';
};

const makeProxyToServerRequest = (reqResPair) =>
  new Promise((resolve, reject) => {
    const protocol = reqResPair.encrypted ? https : http;
    const requestOptions = reqResPair.toHttpRequestOptions();

    const proxyToServerRequest = protocol.request(requestOptions, (response) => {
      const chunks = [];
      response.on('data', chunk => chunks.push(chunk));

      response.on('end', () => {
        const bodyRaw = Buffer.concat(chunks);
        let body;
        const contentEncoding = response.headers['content-encoding'];

        if (contentEncoding && contentEncoding.toLowerCase() === 'gzip') {
          delete response.headers['content-encoding'];
          try {
            body = zlib.gunzipSync(bodyRaw);
          } catch(err) {
            reject(err);
          }
        } else {
          body = bodyRaw;
        }

        const remoteAddress = `${response.socket.remoteAddress}:${response.socket.remotePort}`;
        resolve({
          body: body,
          headers: response.headers,
          statusCode: response.statusCode,
          statusMessage: response.statusMessage,
          httpVersion: response.httpVersion,
          remoteAddress: remoteAddress
        });
      });
    });

    if (
      requestOptions.payload !== undefined &&
      requestOptions.payload.length > 0
    ) {
      proxyToServerRequest.write(requestOptions.payload);
    }

    proxyToServerRequest.end();

    proxyToServerRequest.on('error', (err) => {
      reject(err);
    })
  });

const proxyRequestListener = async (
  browserId,
  interceptClient,
  clientToProxyRequest,
  proxyToClientResponse
) => {
  const chunks = [];
  clientToProxyRequest.on('data', chunk => chunks.push(chunk));

  const requestPayload = await new Promise(resolve => {
    clientToProxyRequest.on('end', () => {
      const data = Buffer.concat(chunks);
      resolve(data);
    });
  });

  const reqResPair = RequestResponsePair.createFromIncomingMessage(
    clientToProxyRequest,
    requestPayload,
    browserId
  );

  if (reqResPair === null) {
    clientToProxyRequest.resume();
    proxyToClientResponse.writeHeader(400, {
      'Content-Type': 'text/html; charset=utf-8'
    });
    proxyToClientResponse.end('Bad request: Host missing...', 'UTF-8');
  } else {
    await reqResPair.saveToDatabase();

    // Intercept the request (if requried):
    const isInterceptEnabled = await interceptEnabled();
    const shouldInterceptRequest = isInterceptEnabled && reqResPair.id !== undefined;
    let shouldInterceptResponse = false;

    if (shouldInterceptRequest) {
      const result = await interceptClient.decisionForRequest(reqResPair.request);

      if (['forward', 'forwardAndIntercept'].includes(result.decision) && result.request.rawRequest !== undefined) {
        await reqResPair.addModifiedRequest(result.request.rawRequest);
      }

      shouldInterceptResponse = (result.decision === 'forwardAndIntercept');
    }

    // Make the actual request and save the response to the database:
    try {
      const serverToProxyResponse = await makeProxyToServerRequest(reqResPair);
      await reqResPair.addHttpServerResponse(serverToProxyResponse);

    } catch(error) {
      if (error.code !== 'ECONNREFUSED' && error.code !== 'ENOTFOUND') {
        console.error(`[ERROR] ${reqResPair.request.method} ${reqResPair.request.url} ${error.code}`);
      }

      proxyToClientResponse.end(error.code, 'UTF-8');
      return;
    }

    // Intercept the response (if requried):
    if (shouldInterceptResponse) {
      const result = await interceptClient.decisionForResponse(reqResPair);
      await reqResPair.addModifiedResponse(result.request.rawResponse, result.request.rawResponseBody);
    }

    // Return the response from the proxy to the client
    const responseOptions = reqResPair.toHttpResponseOptions();

    const responseHeaders = Object.assign({}, responseOptions.headers);
    responseHeaders['content-length'] = Buffer.byteLength(responseOptions.body);

    if (reqResPair.id !== undefined) {
      responseHeaders['X-Oneproxy-Id'] = reqResPair.id;
    }

    proxyToClientResponse.writeHead(
      responseOptions.statusCode,
      responseOptions.statusMessage,
      responseHeaders
    );

    proxyToClientResponse.end(responseOptions.body);
  }
};

module.exports = proxyRequestListener;
