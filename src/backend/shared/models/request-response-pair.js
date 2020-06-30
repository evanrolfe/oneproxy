const http = require('http');
const https = require('https');
const url = require('url');
const  _ = require('lodash')

const CaptureFilters = require('./capture-filters');
const Request = require('./request');
const Response = require('./response');
const { parseHost, parseHostAndPort } = require('../utils');

class RequestResponsePair {
  // Create a ReqResPair from the incomingMessage given to use by the http.server request callback
  static createFromIncomingMessage(incomingMessage, requestPayload, clientId) {
    const request = Request.createFromIncomingMessage(incomingMessage, requestPayload);

    // If the request cannot be parsed:
    if (request === null) return null;

    const reqResPair = new RequestResponsePair();
    reqResPair.request = request;
    reqResPair.clientId = clientId;
    reqResPair.isEncrypted = incomingMessage.socket.encrypted;

    return reqResPair;
  }

  addHttpServerResponse(httpServerResponse) {
    const response = new Response(httpServerResponse);
    response.id = this.id;
    this.response = response;
  }

  async saveToDatabase() {
    const requestParams = this.toDatabaseParams();

    // Create the request:
    if (this.id === undefined) {
      // const shouldRequestBeCaptured = await CaptureFilters.shouldRequestBeCaptured(
      //   this
      // );

      // if (shouldRequestBeCaptured === false) return;

      const dbResult = await global.knex('requests').insert(requestParams);
      this.id = dbResult[0];
      this.request.id = dbResult[0];

      // Update the request:
    } else {
      await global
        .knex('requests')
        .where({ id: this.id })
        .update(requestParams);
    }
  }

  toDatabaseParams() {
    const dbParams = {};

    // Request:
    Object.assign(dbParams, this.request.toDatabaseParams());

    if (this.requestModified()) {
      Object.assign(dbParams, this.modifiedRequest.toDatabaseParamsModified());
    }

    // Response:
    if (this.response !== undefined) {
      Object.assign(dbParams, this.response.toDatabaseParams());
    }

    if (this.responseModified()) {
      Object.assign(dbParams, this.modifiedResponse.toDatabaseParamsModified());
    }

    dbParams.client_id = this.clientId;
    dbParams.request_modified = this.requestModified();
    dbParams.response_modified = this.responseModified();

    return dbParams;
  }

  // Called when a (potentially) modified request value is received from the intercept:
  addModifiedRequest(rawRequest) {
    if (rawRequest !== this.request.toRaw()) {
      this.modifiedRequest = Request.fromRaw(rawRequest, this.isEncrypted);
    }
  }

  addModifiedResponse(rawResponse, rawResponseBody) {
    if (rawResponse !== this.response.toRaw()) {
      this.modifiedResponse = Response.fromRaw(rawResponse, rawResponseBody)
    }
  }

  toHttpRequestOptions() {
    if (this.requestModified()) {
      return this.modifiedRequest.toHttpOptions();
    } else {
      return this.request.toHttpOptions();
    }
  }

  toHttpResponseOptions() {
    // TODO: ALso return modified if necessary
    return this.response.toHttpOptions();
  }

  requestModified() {
    return (this.modifiedRequest !== undefined);
  }

  responseModified() {
    return (this.modifiedResponse !== undefined);
  }

  toInterceptParams() {
    const params = this.request.toInterceptParams();

    if (this.response !== undefined) {
      params.rawResponse = this.response.toRaw();
      params.responseBody = this.response.body.toString();
    }

    return params;
  }
}

module.exports = RequestResponsePair;
