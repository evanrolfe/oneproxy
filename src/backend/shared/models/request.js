const url = require('url');
const  _ = require('lodash')

const { parseHost, parseHostAndPort } = require('../utils');

const parseHost2 = (host, isEncrypted) => {
  const defaultPort = isEncrypted ? 443 : undefined;

  const matches = host.match(/^(http|https):\/\/(.*)/);

  if (matches) {
    return {
      host: matches[2],
      // TODO:
      port: splitHost[1]
    }
  } else {
    return {
      host: host,
      port: defaultPort
    }
  }
};

class Request {
  constructor({method, host, path, encrypted, httpVersion, ext, headers, requestPayload}) {
    this.method = method;
    this.host = host;
    this.path = path;
    this.encrypted = encrypted;
    this.httpVersion = httpVersion;
    this.ext = ext;
    this.headers = headers;
    this.requestPayload = requestPayload;
  }

  static createFromIncomingMessage(incomingMessage, requestPayload) {
    // NOTE: incomingMessage.path is undefined
    const path = url.parse(incomingMessage.url).path;

    // Parse the extension:
    const splitPath = path.split('.');
    let ext;
    if (splitPath.length > 1) ext = splitPath[splitPath.length - 1];

    // Don't forward proxy- headers
    const headers = {};
    for (const h in incomingMessage.headers) {
      // eslint-disable-next-line no-useless-escape
      if (!/^proxy\-/i.test(h)) headers[h] = incomingMessage.headers[h];
    }

    const request = new Request({
      method: incomingMessage.method,
      path: path,
      host: incomingMessage.headers.host,
      encrypted: incomingMessage.socket.encrypted,
      httpVersion: incomingMessage.httpVersion,
      ext: ext,
      headers: headers
    });

    if (requestPayload !== undefined && requestPayload.length > 0)
      request.requestPayload = requestPayload;

    return request;
  }

  static fromRaw(rawRequest, isEncrypted) {
    const lines = rawRequest.split('\n');
    const startLineItems = lines[0].split(' ');

    const method = startLineItems[0].toUpperCase();
    const path = startLineItems[1];
    const httpVersion = startLineItems[2].split('/')[1];

    const headerLines = lines.slice(1, lines.length);

    // If there is a payload in the request, do not process it as a header:
    let requestPayload;
    if (headerLines[headerLines.length - 2] === '') {
      const payloadStr = headerLines.pop();
      requestPayload = Buffer.from(payloadStr);
    }

    const headers = {};
    headerLines.forEach(line => {
      if (line.length === 0) return;

      const splitLine = line.split(': ');
      headers[splitLine[0]] = splitLine[1];
    });

    // If the payload has been modified, set the content-length header:
    if (requestPayload !== undefined) {
      headers['content-length'] = requestPayload.length;
    }

    // Parse the extension:
    const splitPath = path.split('.');
    let ext;
    if (splitPath.length > 1) ext = splitPath[splitPath.length - 1];

    const host = headers.host;

    return new Request({method, host, path, httpVersion, path, ext, headers, requestPayload});
  }

  toDatabaseParams() {
    return {
      method: this.method,
      host: this.host,
      path: this.path,
      encrypted: this.encrypted,
      http_version: this.httpVersion,
      ext: this.ext,
      request_headers: JSON.stringify(this.headers),
      request_payload: this._payloadForDatabase(),
    };
  }

  // If this is a modified request, then we save the same values in columns prefixed with "modified_"
  toDatabaseParamsModified() {
    return {
      modified_method: this.method,
      modified_host: this.host,
      modified_path: this.path,
      modified_http_version: this.httpVersion,
      modified_ext: this.ext,
      modified_request_headers: JSON.stringify(this.headers),
      modified_request_payload: this._payloadForDatabase(),
    };
  }

  _payloadForDatabase() {
    if (this.requestPayload === undefined) return null;

    return this.requestPayload.toString()
  }

  toRaw() {
    let rawRequest = `${this.method.toUpperCase()} ${this.path} HTTP/${
      this.httpVersion
    }\n`;

    Object.keys(this.headers).forEach(header => {
      rawRequest += `${header}: ${this.headers[header]}\n`;
    });

    if (this.requestPayload !== undefined && this.requestPayload.length > 0) {
      rawRequest += '\n';
      rawRequest += this.requestPayload.toString();
    }

    return rawRequest;
  }

  toHttpOptions() {
    // NOTE: The nodejs http.request function requires the port to be defined seperately from the host
    const hostArr = this.host.split(':');
    const host = hostArr[0];

    const options = {
      method: this.method,
      path: this.path,
      host: host,
      headers: _.omit(this.headers, ['host'])
    };

    // Only set the port if its been explicitely set in the host with a semi-colon
    if (hostArr.length === 2) {
      options.port = parseInt(hostArr[1]);
    }

    if (this.requestPayload !== undefined) {
      options.payload = this.requestPayload;
    }

    return options;
  }

  toInterceptParams() {
    return {
      id: this.id,
      method: this.method,
      host: this.host,
      path: this.path,
      rawRequest: this.toRaw()
    };
  }
}

module.exports = Request;
