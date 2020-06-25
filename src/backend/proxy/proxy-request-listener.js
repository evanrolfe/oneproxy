// eslint-disable-next-line no-unused-vars
const http = require('http');
// eslint-disable-next-line no-unused-vars
const https = require('https');
const zlib = require('zlib');

const Request = require('../shared/models/request');
const Settings = require('../shared/models/settings');

const interceptEnabled = async () => {
  const setting = await Settings.getSetting('interceptEnabled');
  return setting.value === '1';
};

const makeProxyToServerRequest = (parsedRequest) =>
  new Promise((resolve, reject) => {
    const protocol = parsedRequest.port === 443 ? https : http;
    const requestOptions = parsedRequest.toHttpRequestOptions();

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

  const parsedRequest = Request.fromHttpIncomingMessage(clientToProxyRequest);
  parsedRequest.client_id = browserId;

  if (requestPayload.length > 0)
    parsedRequest.setRequestPayload(requestPayload);

  if (parsedRequest === null) {
    clientToProxyRequest.resume();
    proxyToClientResponse.writeHeader(400, {
      'Content-Type': 'text/html; charset=utf-8'
    });
    proxyToClientResponse.end('Bad request: Host missing...', 'UTF-8');
  } else {
    await parsedRequest.saveToDatabase();

    // Notify the frontend of the request:
    if (parsedRequest.id !== undefined) {
      const message = {
        type: 'newRequest',
        request: {
          id: parsedRequest.id,
          method: parsedRequest.method,
          url: parsedRequest.url,
          client_id: parsedRequest.client_id
        }
      }
      console.log(`[JSON] ${JSON.stringify(message)}`)
    }

    // Intercept the request (if requried):
    const isInterceptEnabled = await interceptEnabled();
    const shouldInterceptRequest = isInterceptEnabled && parsedRequest.id !== undefined;
    let shouldInterceptResponse = false;

    if (shouldInterceptRequest) {
      const result = await interceptClient.decision(parsedRequest);

      if (['forward', 'forwardAndIntercept'].includes(result.decision) && result.request.rawRequest !== undefined) {
        parsedRequest.setRawRequest(result.request.rawRequest);
      }

      shouldInterceptResponse = result.decision === 'forwardAndIntercept';
    }

    // Make the actual request and save the response to the database:
    try {
      const serverToProxyResponse = await makeProxyToServerRequest(parsedRequest);
      parsedRequest.addHttpServerResponse(serverToProxyResponse);
    } catch(error) {
      if (error.code !== 'ECONNREFUSED' && error.code !== 'ENOTFOUND') {
        // We dont log connection refused as an error
        console.error(`[ERROR] ${parsedRequest.method} ${parsedRequest.url} ${error.code}`);
      }

      proxyToClientResponse.end(error.code, 'UTF-8');
      return;
    }

    // Intercept the response (if requried):
    if (shouldInterceptResponse) {
      const result = await interceptClient.decision(parsedRequest);
      parsedRequest.setRawResponse(
        result.request.rawResponse,
        result.request.rawResponseBody
      );
    }

    // Save the response to the database (if required):
    if (parsedRequest.id !== undefined) {
      await parsedRequest.saveToDatabase();
      // TODO: Notify the frontend:
    }

    // Return the response from the proxy to the client
    const responseOptions = parsedRequest.toHttpResponseOptions();

    const responseHeaders = Object.assign({}, responseOptions.headers);
    responseHeaders['content-length'] = Buffer.byteLength(responseOptions.body);

    if (parsedRequest.id !== undefined) {
      responseHeaders['X-Oneproxy-Id'] = parsedRequest.id;
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
