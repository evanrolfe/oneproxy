const { sleep, clearDatabase, writeToBackend, messageFromBackend, connectToBrowser } = require('../utils');

describe('Browsing', () => {
  let browser;

  before(async () => {
    await clearDatabase();

    // Open a browser:
    const clientInfo = await global.clientGetter.get('chrome');
    const browserPort = clientInfo.browserPort;
    await sleep(2000);

    browser = await connectToBrowser(browserPort);
    console.log(`[TEST] Connected to browser.`);
  });

  after(async () => {
    browser.disconnect()
    await sleep(2000);
  });

  describe('navigating to http://localhost:3000/api/posts.json', () => {
    it('works', async () => {
      const pages = await browser.pages();
      const page = pages[0];
      const navigation = page.goto('http://localhost:3000/api/posts.json');

      await messageFromBackend('newRequest');
      await messageFromBackend('updatedRequest');
      await navigation;

      const requests = await global.knex('requests');

      // The HTTP request:
      expect(requests[0].id).to.eql(1);
      expect(requests[0].method).to.eql('GET');
      expect(requests[0].host).to.eql('localhost:3000');
      expect(requests[0].path).to.eql('/api/posts.json');
      expect(requests[0].ext).to.eql('json');
      expect(requests[0].response_status).to.eql(200);
    });
  });

  // describe('navigating to http://localhost/posts', () => {
  //   it('works', async () => {
  //     const pages = await browser.pages();
  //     const page = pages[0];
  //     await page.goto('http://localhost:3000');
  //     await page.click('#posts_link');



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

