const url = require('url');

const { parseHost, parseHostAndPort } = require('../utils');

class Response {
  constructor({statusCode, statusMessage, httpVersion, headers, body}) {
    this.statusCode = statusCode;
    this.statusMessage = statusMessage;
    this.httpVersion = httpVersion;
    this.headers = headers;
    this.body = body;
  }

  static fromRaw(rawResponse, rawResponseBody) {
    const body = rawResponseBody;

    const lines = rawResponse.split('\n');
    const statusLineArr = lines[0].split(' ');

    const statusCode = statusLineArr[1];
    const httpVersion = statusLineArr[0].split('/')[1];
    const statusMessage = statusLineArr
      .slice(2, statusLineArr.length)
      .join(' ');

    const headerLines = lines.slice(1, lines.length);
    const headers = {};
    headerLines.forEach(line => {
      if (line.length === 0) return;

      const splitLine = line.split(': ');
      headers[splitLine[0]] = splitLine[1];
    });

    return new Response({statusCode, statusMessage, httpVersion, headers, body});
  }

  toDatabaseParams() {
    return {
      response_status: this.statusCode,
      response_status_message: this.statusMessage,
      response_http_version: this.httpVersion,
      response_headers: JSON.stringify(this.headers),
      response_body: this.body.toString()
    };
  }

  // If this is a modified response, then we save the same values in columns prefixed with "modified_"
  toDatabaseParamsModified() {
    return {
      modified_response_status: this.statusCode,
      modified_response_status_message: this.statusMessage,
      modified_response_http_version: this.httpVersion,
      modified_response_headers: JSON.stringify(this.headers),
      modified_response_body: this.body.toString()
    };
  }

  toRaw() {
    let rawResponse = `HTTP/${this.httpVersion} ${this.statusCode} ${this.statusMessage}\n`;

    Object.keys(this.headers).forEach(header => {
      rawResponse += `${header}: ${this.headers[header]}\n`;
    });

    return rawResponse;
  }

  toHttpOptions() {
    return {
      body: this.body,
      headers: this.headers,
      statusCode: this.statusCode,
      statusMessage: this.statusMessage
    };
  }
}

module.exports = Response;
