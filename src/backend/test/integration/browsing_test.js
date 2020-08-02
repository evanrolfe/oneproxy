const { sleep, clearDatabase, writeToBackend, messageFromBackend, connectToBrowser } = require('../utils');

describe('Browsing', () => {
  let browser;

  // before(async () => {
  //   await clearDatabase();

  //   // Open a browser:
  //   writeToBackend({"command": "createClient", "type": "chrome"});
  //   const result = await messageFromBackend('clientStarted');
  //   const browserPort = result.clientInfo.browserPort;
  //   await sleep(1000);

  //   // NOTE: This test must be run first otherwise this port number might be different
  //   // TODO: Get the port number from the backend stdout
  //   browser = await connectToBrowser(9222);
  //   console.log(`[TEST] Connected to browser.`);
  // });

  // after(async () => {
  //   writeToBackend({"command": "closeAllClients"});
  //   await sleep(2000);
  // });

  // describe('navigating to http://localhost:3000/api/posts.json', () => {
  //   it('works', async () => {
  //     const pages = await browser.pages();
  //     const page = pages[0];
  //     await page.goto('http://localhost:3000/api/posts.json');

  //     const message = await messageFromBackend('newRequest');

  //     const requests = await global.knex('requests');

  //     // The HTTP request:
  //     expect(requests[0].id).to.eql(1);
  //     expect(requests[0].method).to.eql('GET');
  //     expect(requests[0].host).to.eql('localhost:3000');
  //     expect(requests[0].path).to.eql('/api/posts.json');
  //     expect(requests[0].ext).to.eql('json');
  //     expect(requests[0].response_status).to.eql(200);
  //   });
  // });

  // describe('navigating to http://localhost/posts', () => {
  //   it('works', async () => {
  //     const pages = await browser.pages();
  //     const page = pages[0];
  //     await page.goto('http://localhost:3000');
  //     await page.click('#posts_link');

  //     await sleep(2000);

  //     const requests = await global.knex('requests');
  //     const expectedUrls = [
  //     'http://localhost:3000/',
  //     'http://localhost:3000/posts',
  //     'http://localhost:3000/api/posts.json'
  //     ];

  //     const requestUrls = requests.map(r => r.url);
  //     console.log(requestUrls)
  //     expectedUrls.forEach(expectedUrl => {
  //       expect(requestUrls).to.include(expectedUrl);
  //     });
  //   });
  // });
});

