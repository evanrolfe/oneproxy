const url = require('url');

const { parseHost, parseHostAndPort } = require('../utils');

class Request {
  constructor({method, url, host, port, httpVersion, path, ext, headers, requestPayload}) {
    this.method = method;
    this.url = url;
    this.host = host;
    this.port = port;
    this.httpVersion = httpVersion;
    this.path = path;
    this.ext = ext;
    this.headers = headers;
    this.requestPayload = requestPayload;
  }

  static createFromIncomingMessage(incomingMessage, requestPayload) {
    const isEncrypted = incomingMessage.socket.encrypted;
    const defaultPort = isEncrypted ? 443 : 80;
    const {host, port} = parseHostAndPort(incomingMessage, defaultPort);
    const protocol = isEncrypted ? 'https' : 'http';

    // NOTE: clientToProxyRequest.path is undefined
    // NOTE: clientToProxyRequest.url = path in HTTP, but not in HTTPS
    const path = url.parse(incomingMessage.url).path;
    let urlStart = `${protocol}://${host}`;

    if (port !== 80) {
      urlStart += `:${port}`;
    }

    let requestUrl = new URL(path, urlStart);

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
      url: requestUrl.toString(),
      path: path,
      host: host,
      port: port,
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

    const defaultPort = isEncrypted ? 443 : 80;
    const {host, port} = parseHost(headers.host, defaultPort);

    // Rebuild the url from the host, path & protocol
    const protocol = isEncrypted ? 'https' : 'http';
    const requestUrl = new URL(
      path,
      `${protocol}://${headers.host}`
    );
    const url = requestUrl.toString();

    // Parse the extension:
    const splitPath = path.split('.');
    let ext;
    if (splitPath.length > 1) ext = splitPath[splitPath.length - 1];

    return new Request({method, url, host, port, httpVersion, path, ext, headers, requestPayload});
  }

  toDatabaseParams() {
    return {
      method: this.method,
      url: this.url,
      host: this.host,
      port: this.port,
      http_version: this.httpVersion,
      path: this.path,
      ext: this.ext,
      request_headers: JSON.stringify(this.headers),
      request_payload: this.requestPayload,
    };
  }

  // If this is a modified request, then we save the same values in columns prefixed with "modified_"
  toDatabaseParamsModified() {
    return {
      modified_method: this.method,
      modified_url: this.url,
      modified_host: this.host,
      modified_port: this.port,
      modified_http_version: this.httpVersion,
      modified_path: this.path,
      modified_ext: this.ext,
      modified_request_headers: JSON.stringify(this.headers),
      modified_request_payload: this.requestPayload,
    };
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
    const options = {
      method: this.method,
      path: this.path,
      host: this.host,
      port: this.port,
      headers: this.headers
    };

    if (this.requestPayload !== undefined) {
      options.payload = this.requestPayload;
    }

    return options;
  }

  toInterceptParams() {
    return {
      id: this.id,
      method: this.method,
      url: this.url,
      rawRequest: this.toRaw()
    };
  }
}

module.exports = Request;
