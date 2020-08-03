//const exec = util.promisify(require('child_process').exec);

const util = require('util');
const { exec } = require('child_process');

const { DEFAULT_FILTERS } = require('../../shared/constants');
const { sleep, clearDatabase, writeToBackend, messageFromBackend } = require('../utils');

const makeRequest = (proxyPort, curlCommand) => new Promise((resolve, reject) => {
  exec(curlCommand, (error, stdout, stderr) => {
    console.log(`[TEST] Received curl response`)
    resolve(stdout);
  });
});

describe('HTTPS Request Test', () => {
  let proxyPort;

  before(async () => {
    await clearDatabase();

    // Create default capture filters:
    const filters = Object.assign({}, DEFAULT_FILTERS);
    filters.hostList = ['localhost:3000', 'maxcdn.bootstrapcdn.com'];
    filters.hostSetting = 'include';

    await global
      .knex('capture_filters')
      .where({id: 1})
      .update({filters: JSON.stringify(filters) });

    // Get a client:
    const clientInfo = await global.clientGetter.get('anything');
    proxyPort = clientInfo.proxyPort;
    await sleep(2000);
  });

  describe('Making an HTTP request', () => {
    it('works', async () => {
      const curlCommand = `curl http://maxcdn.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css --proxy http://127.0.0.1:${proxyPort}`;
      const curlRequestFinished = makeRequest(proxyPort, curlCommand);
      const message = await messageFromBackend('newRequest');

      await curlRequestFinished;

      const result = await global.knex('requests').where({ id: message.request.id });
      const request = result[0];

      expect(request.method).to.eql('GET');
      expect(request.host).to.eql('maxcdn.bootstrapcdn.com');
      expect(request.encrypted).to.eql(0);
      expect(request.http_version).to.eql('1.1');
      expect(request.path).to.eql('/bootstrap/4.3.1/css/bootstrap.min.css');
      expect(request.ext).to.eql('css');
      expect(request.request_headers).to.include('curl');
      expect(request.response_status).to.eql(200);
    });
  });

  describe('Making an HTTP request to the mock server', () => {
    it('works', async () => {
      const curlCommand = `curl http://localhost:3000 --proxy http://127.0.0.1:${proxyPort}`;
      const curlRequestFinished = makeRequest(proxyPort, curlCommand);
      console.log(`[TEST] curl request made, now waiting for message from backend... (1)`)
      const message = await messageFromBackend('newRequest');
      console.log(`[TEST] received message from the backend (2)`)
      const response = await curlRequestFinished;
      console.log(`[TEST] Curl request finished (3)`)
      const result = await global.knex('requests').where({ id: message.request.id });
      const request = result[0];

      expect(request.method).to.eql('GET');
      expect(request.host).to.eql('localhost:3000');
      expect(request.encrypted).to.eql(0);
      expect(request.http_version).to.eql('1.1');
      expect(request.path).to.eql('/');
      expect(request.ext).to.eql(null);
      expect(request.request_headers).to.include('curl');
      expect(request.response_status).to.eql(200);
    });
  });

  describe('Making an HTTPS request', () => {
    it('works', async () => {
      const curlCommand = `curl https://maxcdn.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css --proxy http://127.0.0.1:${proxyPort} --insecure`;
      const curlRequestFinished = makeRequest(proxyPort, curlCommand);
      const message = await messageFromBackend('newRequest');

      await curlRequestFinished;

      const result = await global.knex('requests').where({ id: message.request.id });
      const request = result[0];

      expect(request.method).to.eql('GET');
      expect(request.host).to.eql('maxcdn.bootstrapcdn.com');
      expect(request.encrypted).to.eql(1);
      expect(request.http_version).to.eql('1.1');
      expect(request.path).to.eql('/bootstrap/4.3.1/css/bootstrap.min.css');
      expect(request.ext).to.eql('css');
      expect(request.request_headers).to.include('curl');
      expect(request.response_status).to.eql(200);
    });
  });
});

