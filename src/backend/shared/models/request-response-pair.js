const http = require('http');
const https = require('https');
const url = require('url');
const  _ = require('lodash')

const frontend = require('../../shared/notify_frontend');
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
    reqResPair.encrypted = (incomingMessage.socket.encrypted === true);

    return reqResPair;
  }

  async addHttpServerResponse(httpServerResponse) {
    const response = new Response(httpServerResponse);
    response.id = this.id;
    this.response = response;
    await this.saveToDatabaseIfAlreadySaved();
  }

  async saveToDatabaseIfAlreadySaved() {
    if (this.id !== undefined) {
      await this.saveToDatabase();
    }
  }

  async saveToDatabase() {
    const requestParams = this.toDatabaseParams();

    // Create the request:
    if (this.id === undefined) {
      const shouldRequestBeCaptured = await CaptureFilters.shouldRequestBeCaptured(this.request);

      if (shouldRequestBeCaptured === false) return;

      const dbResult = await global.knex('requests').insert(requestParams);
      this.id = dbResult[0];
      this.request.id = dbResult[0];

      // Notify the frontend of the request:
      frontend.notifyNewRequest(this);

      // Update the request:
    } else {
      await global
        .knex('requests')
        .where({ id: this.id })
        .update(requestParams);

      // Notify the frontend of the request:
      frontend.notifyUpdatedRequest(this);
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
    dbParams.encrypted = this.encrypted;

    return dbParams;
  }

  // Called when a (potentially) modified request value is received from the intercept:
  async addModifiedRequest(rawRequest) {
    if (rawRequest !== this.request.toRaw()) {
      this.modifiedRequest = Request.fromRaw(rawRequest, this.encrypted);
      await this.saveToDatabaseIfAlreadySaved();
    }
  }

  async addModifiedResponse(rawResponse, rawResponseBody) {
    if (rawResponse !== this.response.toRaw() || rawResponseBody !== this.response.body.toString()) {
      this.modifiedResponse = Response.fromRaw(rawResponse, rawResponseBody);
      await this.saveToDatabaseIfAlreadySaved();
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
    if (this.responseModified()) {
      return this.modifiedResponse.toHttpOptions();
    } else {
      return this.response.toHttpOptions();
    }
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
