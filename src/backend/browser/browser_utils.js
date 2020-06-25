const puppeteer = require('puppeteer-core');
const { handleNewPage } = require('./browser_page_utils');

// Wait until we are able to connect to the browser on the given port
const remoteBrowserConnection = (debugPort) => {
  return new Promise((resolve) => {
    const interval = setInterval(async () => {
      try {
        const browser = await puppeteer.connect({
          browserURL: `http://localhost:${debugPort}`,
          defaultViewport: null
        });
        clearInterval(interval);
        resolve(browser);
      } catch(err) {
        return;
      }
    }, 500);
  });
};

const instrumentBrowser = async (browserId, debugPort) => {
  console.log(`[BrowserUtils-${browserId}] Connecting to the browser on port ${debugPort}...`)
  const browser = await remoteBrowserConnection(debugPort);
  console.log(`[BrowserUtils-${browserId}] Got a browser connection.!!!!!!!!!!!!!!!!!!`)
  browser.id = browserId;

  console.log(`[BrowserUtils-${browserId}] instrumenting browser...`);

  // Intercept any new tabs created in the browser:
  browser.on('targetcreated', async target => {
    console.log(`[BrowserUtils-${browserId}] Target created`);
    const newPage = await target.page();

    if (newPage !== null) {
      console.log(`[BrowserUtils-${browserId}] target page: ${newPage.url()}`);
      handleNewPage(newPage);
    }
  });

  // Load the browser from database:
  const result = await global.knex('clients').where({ id: browserId });
  const browserDb = result[0];

  // Load saved cookies if there are any:
  cookies = JSON.parse(browserDb.cookies);
  if (cookies !== null && cookies.length > 0) {

  const target = browser
    .targets()
    .find(targetEnum => targetEnum._targetInfo.type === 'page');

    const cdpSession = await target.createCDPSession();
    await cdpSession.send('Network.setCookies', {cookies: cookies});
  }

  pageUrls = JSON.parse(browserDb.pages);
  // Load saved pages if there are any:
  if (pageUrls !== null && pageUrls.length > 0) {
    await loadPagesForBrowser(browser, pageUrls);
  } else {
    // Close and re-open the page so its instrumented:
    const pages = await browser.pages();
    const page = pages[0];
    await browser.newPage();
    page.close();
  }

  //browser.on('disconnected', () => handleBrowserClosed(browser));
};

// {"command": "openClient", "id": 1}
const loadPagesForBrowser = async (browser, pageUrls) => {
  for (let i = 0; i < pageUrls.length; i++) {
    const pageUrl = pageUrls[i];
    console.log(`[BrowserUtils] opening page at ${pageUrl}`)
    // Chromium starts with an about:blank page open so use that for the first one:
    let page;
    if (i === 0) {
      // eslint-disable-next-line no-await-in-loop
      const pages = await browser.pages();
      page = pages[0];
    } else {
      // eslint-disable-next-line no-await-in-loop
      page = await browser.newPage();
    }
    page.goto(pageUrl);

    // NOTE: the targetcreated event does not seem to be triggered for these
    // pages so we have to instrument the page manually:
    handleNewPage(page);
  }
};

module.exports = { instrumentBrowser };
