//const exec = util.promisify(require('child_process').exec);

const util = require('util');
const { exec } = require('child_process');

const { sleep, clearDatabase, writeToBackend, messageFromBackend } = require('../utils');

const makeRequest = (url, proxyPort) => new Promise((resolve, reject) => {
  console.log(`[TEST] Making curl request...`)

  const curlCommand = `curl ${url} --proxy http://127.0.0.1:${proxyPort}`;

  exec(curlCommand, (error, stdout, stderr) => {
    console.log(`[TEST] Curl response:`)
    if(error) reject(error);

    resolve(stdout);
  });
});

const RAW_RESPONSE = '';

// describe('Making a request through the proxy', () => {
//   let proxyPort;

//   before(async () => {
//     await clearDatabase();

//     // Open a client:
//     writeToBackend({"command": "createClient", "type": "anything"});
//     const result = await messageFromBackend('clientStarted');
//     proxyPort = result.clientInfo.proxyPort;
//     await sleep(2000);
//   });

//   after(async () => {
//     writeToBackend({"command": "closeAllClients"});
//     await sleep(200);
//   });

//   it('works', async () => {
//     const url = 'http://localhost:3000/api/posts/1.json';
//     const curlRequestFinished = makeRequest(url, proxyPort);

//     const response = await curlRequestFinished;
//     console.log(response);
//   });
// });

