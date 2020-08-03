//const exec = util.promisify(require('child_process').exec);

const util = require('util');
const { exec } = require('child_process');

const { sleep, clearDatabase, writeToBackend, messageFromBackend } = require('../utils');

const makeRequest = (proxyPort, curlCommand) => new Promise((resolve, reject) => {
  console.log(`[TEST] Making curl request...`)

  if (curlCommand === undefined) {
    curlCommand = `curl http://localhost:3000 --proxy http://127.0.0.1:${proxyPort}`;
  }

  exec(curlCommand, (error, stdout, stderr) => {
    console.log(`[TEST] Curl response:`)
    if(error) reject(error);

    resolve(stdout);
  });
});

const RAW_RESPONSE = '';

describe('The Intercept', () => {
  let proxyPort;

  before(async () => {
    await clearDatabase();

    // Get a client:
    const clientInfo = await global.clientGetter.get('anything');
    proxyPort = clientInfo.proxyPort;
    await sleep(2000);

    // Enable the intercept:
    writeToBackend({"command": "changeSetting", "key": "interceptEnabled", "value": true});
    await messageFromBackend('settingChanged');
  });

  describe('Intercepting a request and its response and modifying the response and body', () => {
    it('works', async () => {
      const curlRequestFinished = makeRequest(proxyPort);
      const message = await messageFromBackend('requestIntercepted');

      writeToBackend({
        "command": "forwardAndIntercept",
        "request": {
          "id": message.request.id,
          "rawRequest": message.request.rawRequest
        }
      });

      const message2 = await messageFromBackend('responseIntercepted');

      writeToBackend({
        "command": "forward",
        "request": {
          "id": message2.request.id,
          "rawResponse": message2.request.rawResponse,
          "rawResponseBody": '{"hello": "OK"}'
        }
      });

      const response = await curlRequestFinished;

      const result = await global.knex('requests').where({ id: message2.request.id });
      const request = result[0];

      // Original Request:
      expect(request.method).to.eql('GET');
      expect(request.host).to.eql('localhost:3000');
      expect(request.path).to.eql('/');
      expect(request.http_version).to.eql('1.1');
      expect(request.path).to.eql('/');
      expect(request.ext).to.eql(null);
      expect(request.request_headers).to.include('curl');

      // Modified Request:
      expect(request.modified_url).to.eql(null);
      expect(request.modified_method).to.eql(null);
      expect(request.modified_host).to.eql(null);
      expect(request.modified_path).to.eql(null);
      expect(request.modified_http_version).to.eql(null);
      expect(request.modified_path).to.eql(null);
      expect(request.modified_ext).to.eql(null);
      expect(request.modified_request_headers).to.eql(null);

      // Response:
      expect(request.response_status).to.eql(200);
      expect(request.response_status_message).to.eql('OK');
      expect(request.response_http_version).to.eql('1.1');
      expect(request.response_headers).to.include('text/html');
      expect(request.response_body).to.include('<html');

      // Modified response:
      expect(request.modified_response_status).to.eql(200);
      expect(request.modified_response_status_message).to.eql('OK');
      expect(request.modified_response_http_version).to.eql('1.1');
      expect(request.modified_response_body).to.eql('{"hello": "OK"}');

      // General:
      //expect(request.client_id).to.eql(1);
      expect(request.request_modified).to.eql(0);
      expect(request.response_modified).to.eql(1);

      expect(response).to.eql('{"hello": "OK"}')
    });
  });

  describe('Intercepting a request and modifying its request', () => {
    it('works', async () => {
      const curlRequestFinished = makeRequest(proxyPort);
      const message = await messageFromBackend('requestIntercepted');

      writeToBackend({
        "command": "forward",
        "request": {
          "id": message.request.id,
          "rawRequest": 'GET /api/posts.json HTTP/1.1\nhost: localhost:3000\nuser-agent: curl/1.2.3\naccept: */*\n'
        }
      });
      const response = await curlRequestFinished;

      const result = await global.knex('requests').where({ id: message.request.id });
      const request = result[0];

      // Original Request:
      expect(request.method).to.eql('GET');
      expect(request.host).to.eql('localhost:3000');
      expect(request.path).to.eql('/');
      expect(request.http_version).to.eql('1.1');
      expect(request.path).to.eql('/');
      expect(request.ext).to.eql(null);
      expect(request.request_headers).to.include('curl');

      // Modified Request:

      expect(request.modified_method).to.eql('GET');
      expect(request.modified_host).to.eql('localhost:3000');
      expect(request.modified_path).to.eql('/api/posts.json');
      expect(request.modified_http_version).to.eql('1.1');
      expect(request.modified_ext).to.eql('json');
      expect(request.modified_request_headers).to.include('curl');

      // Response:
      expect(request.response_status).to.eql(200);
      expect(request.response_status_message).to.eql('OK');
      expect(request.response_http_version).to.eql('1.1');
      expect(request.response_headers).to.include('application/json');
      expect(request.response_body).to.include('[{"id":1,');
    });
  });

  describe('Intercepting a request and modifying its headers', () => {
    it('works', async () => {
      const curlRequestFinished = makeRequest(proxyPort);
      const message = await messageFromBackend('requestIntercepted');

      writeToBackend({
        "command": "forward",
        "request": {
          "id": message.request.id,
          "rawRequest": message.request.rawRequest.replace('3000', '3001')
        }
      });
      const response = await curlRequestFinished;

      const result = await global.knex('requests').where({ id: message.request.id });
      const request = result[0];

      // Original Request:
      expect(request.method).to.eql('GET');
      expect(request.host).to.eql('localhost:3000');
      expect(request.path).to.eql('/');
      expect(request.http_version).to.eql('1.1');
      expect(request.path).to.eql('/');
      expect(request.ext).to.eql(null);
      expect(request.request_headers).to.include('curl');

      // // Modified Request:
      expect(request.modified_method).to.eql('GET');
      expect(request.modified_host).to.eql('localhost:3001');
      expect(request.modified_path).to.eql('/');
      expect(request.modified_http_version).to.eql('1.1');
      expect(request.modified_ext).to.eql(null);
      expect(request.modified_request_headers).to.include('curl');

      // General:
      expect(request.request_modified).to.eql(1);
      expect(request.response_modified).to.eql(0);
    });
  });

  describe('Intercepting a POST request', () => {
    it('works', async () => {
      const curlCommand = `curl --request POST http://localhost:3000/api/posts.json --header 'Content-Type: application/json' --data-raw '{"name": "intercept_test"}'  --proxy http://127.0.0.1:${proxyPort}`
      const curlRequestFinished = makeRequest(proxyPort, curlCommand);
      const message = await messageFromBackend('requestIntercepted');

      const rawRequest = `POST /api/posts.json HTTP/1.1
host: localhost:3000
user-agent: curl/7.58.0
accept: */*
content-type: application/json
content-length: 26

{"name": "evan"}`;

      writeToBackend({
        "command": "forward",
        "request": {
          "id": message.request.id,
          "rawRequest": rawRequest
        }
      });
      const response = await curlRequestFinished;

      const result = await global.knex('requests').where({ id: message.request.id });
      const request = result[0];

      // Original Request:
      expect(request.host).to.eql('localhost:3000');
      expect(request.path).to.eql('/api/posts.json');
      expect(request.method).to.eql('POST');
      expect(request.request_payload).to.eql('{"name": "intercept_test"}');

      // Modified Request:
      expect(request.modified_host).to.eql('localhost:3000');
      expect(request.modified_path).to.eql('/api/posts.json');
      expect(request.modified_method).to.eql('POST');
      expect(request.modified_request_payload).to.eql('{"name": "evan"}');

      // Response:
      expect(response).to.eql('{"message":"Hello, you told us your name is: evan"}')
    });
  });
});

