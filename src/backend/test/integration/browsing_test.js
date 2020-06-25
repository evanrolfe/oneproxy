const { sleep, clearDatabase, writeToBackend, messageFromBackend, connectToBrowser } = require('../utils');

describe('Browsing', () => {
  let browser;

  before(async () => {
    await clearDatabase();

    // Open a browser:
    writeToBackend({"command": "createClient", "type": "chromium"});
    const result = await messageFromBackend('clientStarted');
    const browserPort = result.clientInfo.browserPort;
    await sleep(1000);

    // NOTE: This test must be run first otherwise this port number might be different
    // TODO: Get the port number from the backend stdout
    browser = await connectToBrowser(9222);
    console.log(`[TEST] Connected to browser.`);
  });

  after(async () => {
    writeToBackend({"command": "closeAllClients"});
    await sleep(2000);
  });

  describe('navigating to http://localhost/api/posts.json', () => {
    it('works', async () => {
      const pages = await browser.pages();
      const page = pages[0];
      await page.goto('http://localhost/api/posts.json');
      await sleep(1000);

      const requests = await global.knex('requests');

      // The HTTP request:
      expect(requests[0].id).to.eql(1);
      expect(requests[0].method).to.eql('GET');
      expect(requests[0].url).to.eql('http://localhost/api/posts.json');
      expect(requests[0].host).to.eql('localhost');
      expect(requests[0].path).to.eql('/api/posts.json');
      expect(requests[0].ext).to.eql('json');
      expect(requests[0].response_status).to.eql(200);
    });
  });

  describe('navigating to http://localhost/posts', () => {
    it('works', async () => {
      const pages = await browser.pages();
      const page = pages[0];
      await page.goto('http://localhost/posts');
      await sleep(1000);

      const requests = await global.knex('requests');

      const expectedUrls = [
      'http://localhost/posts',
      'http://localhost/static/js/bundle.js',
      'http://localhost/static/js/0.chunk.js',
      'http://localhost/static/js/main.chunk.js',
      'http://localhost/api/posts.json'
      ];

      const requestUrls = requests.map(r => r.url);

      expectedUrls.forEach(expectedUrl => {
        expect(requestUrls).to.include(expectedUrl);
      });
    });
  });

  // describe('navigating to http://localhost/posts, clicking a link, then clicking back', () => {
  //   it('works', async () => {
  //     const pages = await browser.pages();
  //     const page = pages[0];
  //     await sleep(1000);

  //     // Click the link to view a post:
  //     await page.click('a[href="/posts/1"]');
  //     await sleep(2000);

  //     // Click the "Posts" link to go back to the first page:
  //     await page.click('#posts_link');
  //     await sleep(2000);

  //     const requests = await global.knex('requests');

  //     // // Request ID 1:
  //     // expect(requests[0].id).to.eql(1);
  //     // expect(requests[0].method).to.eql('GET');
  //     // expect(requests[0].url).to.eql('http://localhost/posts');
  //     // expect(requests[0].response_body.length).to.be.above(0)
  //     // expect(requests[0].response_body_rendered.length).to.be.above(0)

  //     // // Request ID 3:
  //     // expect(requests[2].id).to.eql(3);
  //     // expect(requests[2].method).to.eql(null);
  //     // expect(requests[2].url).to.eql('http://localhost/posts/1');
  //     // expect(requests[2].response_body).to.eql(null);
  //     // expect(requests[2].response_body_rendered.length).to.be.above(0)

  //     const requestUrls = requests.map(r => r.url);
  //     requests.forEach((r) => {
  //       console.log(`${r.id} - ${r.url}`);
  //     });
  //   });
  // });
});

