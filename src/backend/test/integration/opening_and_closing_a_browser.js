const { sleep, clearDatabase, writeToBackend, messageFromBackend, connectToBrowser } = require('../utils');

describe('Opening and closing a browser', () => {
  let browser;

  before(async () => {
    await clearDatabase();

    // Open a browser:
    writeToBackend({ "command": "createClient", "type": 'chrome' });
    result = await messageFromBackend('clientStarted');

    const browserPort = result.clientInfo.browserPort;
    await sleep(500);

    browser = await connectToBrowser(browserPort);
    console.log(`[TEST] Connected to browser on port ${browserPort}.`);
  });

  it('kills the proxy too', async () => {
    await browser.close();
    console.log(`[TEST] the browser has been closed.`)
    await sleep(2000);
  });
});

