//const exec = util.promisify(require('child_process').exec);

const util = require('util');
const { exec } = require('child_process');

const { sleep, clearDatabase, writeToBackend, messageFromBackend } = require('../utils');

const makeRequest = (proxyPort) => new Promise((resolve, reject) => {
  console.log(`[TEST] Making curl request...`)

  const curlCommand = `curl http://localhost --proxy http://127.0.0.1:${proxyPort}`;

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

    // Open a client:
    writeToBackend({"command": "createClient", "type": "anything"});
    const result = await messageFromBackend('clientStarted');
    proxyPort = result.clientInfo.proxyPort;
    await sleep(2000);

    // Enable the intercept:
    writeToBackend({"command": "changeSetting", "key": "interceptEnabled", "value": true});
  });

  after(async () => {
    writeToBackend({"command": "closeAllClients"});
    await sleep(200);
  });

  describe('Intercepting a request and its response', () => {
    it('works', async () => {
      const curlRequestFinished = makeRequest(proxyPort);
      const message = await messageFromBackend('requestIntercepted');

      console.log(`[TEST] sending forwardAndIntercept to backend (1)...`)
      writeToBackend({
        "command": "forwardAndIntercept",
        "request": {
          "id": message.request.id,
          "rawRequest": 'GET /api/posts.json HTTP/1.1\nhost: localhost\nuser-agent: curl/7.58.0\naccept: */*\n'
        }
      });

      const message2 = await messageFromBackend('responseIntercepted');
      writeToBackend({
        "command": "forward",
        "request": {
          "id": message2.request.id,
          "rawResponse": `HTTP/1.1 200 OK\n` +
            `server: nginx/1.17.2\n` +
            `date: Thu, 18 Jun 2020 13:05:52 GMT\n` +
            `content-type: application/json; charset=UTF-8\n` +
            `content-length: 1882\n` +
            `connection: close\n` +
            `x-powered-by: Express\n` +
            `accept-ranges: bytes\n` +
            `etag: W/"75a-1XYlKVpg4cBDuqMmYgY2/saFRQs"\n` +
            `vary: Accept-Encoding\n` +
            `x-oneproxy-id: 123\n`,
          "rawResponseBody": '{"hello": "OK"}'
        }
      });

      const response = await curlRequestFinished;

      const result = await global.knex('requests').where({ id: message2.request.id });
      const request = result[0];

      expect(request.url).to.eql('http://localhost/')
      expect(request.modified_url).to.eql('http://localhost/api/posts.json')

       // The original response
      expect(request.response_body.length).to.eql(705)

      // The modified response:
      expect(request.modified_response_body).to.eql('{"hello": "OK"}')
    });
  });

  describe('Intercepting a request', () => {
    it('works', async () => {
      const curlRequestFinished = makeRequest(proxyPort);
      const message = await messageFromBackend('requestIntercepted');

      console.log(`[TEST] sending forward to backend...`)
      writeToBackend({
        "command": "forward",
        "request": {
          "id": message.request.id,
          "rawRequest": 'GET /api/posts.json HTTP/1.1\nhost: localhost\nuser-agent: curl/7.58.0\naccept: */*\n'
        }
      });

      const response = await curlRequestFinished;
      console.log(response);

      const result = await global.knex('requests').where({ id: message.request.id });
      const request = result[0];

      expect(request.url).to.eql('http://localhost/')
      expect(request.modified_url).to.eql('http://localhost/api/posts.json')
    });
  });
});

