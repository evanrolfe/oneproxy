//import CaptureFilters from '../../shared/models/capture-filters';

/*
 * NOTE: For each response intercepted
 * If that request is a navigation request (i.e. a page displayed in the browser), then we start
 * the DOMListener, which saves the page's rendered DOM to request.response_body_rendered every
 * 100ms.
 *
 * For every page, we also listen for the framenavigated event, which creates a navigation request
 * and saves the rendered DOM to that request in the database, cancels the DOMListener and starts
 * a new one.
 *
 * Race Condition - this happens if you don't check the database inside the DOMListener callback:
 *
 * BrowserUtils: DOMListener 16 running...
 * BrowserUtils: saved content for page: http://localhost/ to request 1, (DOMListener 16)
 * BrowserUtils: DOMListener 16 running...
 * BrowserUtils: frameNavigated to http://localhost/posts
 * BrowserUtils: killed DomListener #16
 * BrowserUtils: saved content for page: http://localhost/posts to request 1, (DOMListener 16)
 * BrowserUtils: create new request 9 and starting DOMListener...
 * BrowserUtils: started domListener id 64
 * BrowserUtils: DOMListener 64 running...
 * BrowserUtils: saved content for page: http://localhost/posts to request 9, (DOMListener 64)
 */

const handleNewPage = async (page) => {
  if (page === null) return;
  console.log(`[BrowserUtils] handleNewPage`);

  // TODO: Make this a configurable option:
  page.setCacheEnabled(false);

  page.on('response', async response => handleResponse(page, response));

  // Capture websocket HTTP requests
  const cdp = await page.target().createCDPSession();
  await cdp.send('Network.enable');
  await cdp.send('Page.enable');

  cdp.on('Network.webSocketWillSendHandshakeRequest', async params => {
    // Save the websocket HTTP handshake request to the DB
    const requestParams = {
      client_id: page.browser().id,
      websocket_request_id: params.requestId
    };

    await global
      .knex('requests')
      .where({ websocket_sec_key: params.request.headers['Sec-WebSocket-Key'] })
      .update(requestParams);
  });

  // cdp.on('Network.webSocketHandshakeResponseReceived', (params) => {
  //   console.log(`RequestTo (request headers): ${JSON.stringify(params.response.requestHeaders)}`)
  //   console.log(`RequestTo (response headers): ${JSON.stringify(params.response.headers)}`)
  // });
};

const handleResponse = async (page, response) => {
  const headers = response.headers();
  const requestId = headers['x-oneproxy-id'];
  //console.log(`[BrowserUtils] response received from ${response.url()} (x-oneproxy-id: ${requestId})`)

  // Save the cookies & pages:
  const { cookies } = await page._client.send('Network.getAllCookies');
  const pages = await page.browser().pages();
  const pageUrls = pages.map(pageEnum => pageEnum.url());
  await global
    .knex('clients')
    .where({ id: page.browser().id })
    .update({
      cookies: JSON.stringify(cookies),
      pages: JSON.stringify(pageUrls)
    });
  // This does not work when you open a link in a new tab:
  // https://github.com/puppeteer/puppeteer/issues/3667
  const isNavigation =
    response.request().isNavigationRequest() || page.url() === response.url();

  if (isNavigation && requestId !== undefined) {
    // Prevent navigation requests from iframes
    if (
      response.request().frame() !== null &&
      response
        .request()
        .frame()
        .url() !== page.url()
    )
      return;

    console.log(`*--------------------------------------*`);
    console.log(`* Response received on page: ${page.url()}`);
    console.log(`* Response URL: ${response.url()}`);
    console.log(`* x-oneproxy-id: ${headers['x-oneproxy-id']}`);
    console.log(`* Is Navigation? ${response.request().isNavigationRequest()}`);
    console.log(`* client_id: ${page.browser().id}`);
    console.log(`*--------------------------------------*\n\n`);

    page.domListenerId = await startDOMListener(page, requestId);

    const origURL = ` ${response.url()}`.slice(1); // Clone the url string
    if (page.listenerCount('framenavigated') === 0) {
      console.log(
        `[BrowserUtils] starting framenavigated for request ${requestId}`
      );
      page.on('framenavigated', frame =>
        handleFramenavigated(page, frame, origURL)
      );
    }
  }
};

const handleFramenavigated = async (page, frame, origURL) => {
  // See: https://stackoverflow.com/questions/49237774/using-devtools-protocol-event-page-framenavigated-to-get-client-side-navigation
  // See: https://github.com/GoogleChrome/puppeteer/issues/1489
  if (frame !== page.mainFrame()) return; //  || origURL === 'about:blank'

  // NOTE 1: a framenavigated event gets triggered even if we have already intercepted the requests,
  // so we don't want to create a new request for these ones
  // NOTE 2: (2020-06-25) I commented out this line because this meant that if you open a browser to a
  // page, navigate to a different page, then navigate back to the original page, then a navigation
  // request will not be record for the last change
  // if (frame.url() === origURL) return;

  console.log(`[BrowserUtils] FrameNavigation:`);
  console.log(`[BrowserUtils] page.url() ${page.url()}`);
  console.log(`[BrowserUtils] frame.url() ${frame.url()}`);
  console.log(`[BrowserUtils] origURL ${origURL}`);

  clearInterval(page.domListenerId);
  console.log(`BrowserUtils: killed DomListener #${page.domListenerId}`);

  // Create a navigation request (not a real HTTP request - just a change in URL)
  const parsedUrl = new URL(page.url());
  const requestParams = {
    client_id: page.browser().id,
    url: page.url(),
    host: parsedUrl.hostname,
    path: parsedUrl.pathname,
    request_type: 'navigation',
    created_at: Date.now()
  };

  const result = await global.knex('requests').insert(requestParams);
  const requestId = result[0];

  const message = {
      type: 'newRequest',
      request: {
        id: requestId,
        method: '',
        url: requestParams.url,
        client_id: requestParams.client_id
      }
  }
  console.log(`[JSON] ${JSON.stringify(message)}`)

  console.log(
    `[BrowserUtils] frameNavigated to ${frame.url()}, origURL: ${origURL}`
  );
  console.log(`[BrowserUtils] created navigation request ${requestId}`);
  page.domListenerId = await startDOMListener(page, requestId);
};

const startDOMListener = async (page, requestId) => {
  const domListenerId = await setInterval(async () => {
    //console.log(`[BrowserUtils] DOMListener ${domListenerId} running...`);
    console.log(`[BrowserUtils] DOMListener for requestId: ${requestId} on page: ${page.url()}`);

    // UGLY WORKAROUND: Prevent the race condition described at the top of page:
    // Check that the page url has not changed while this callback has been running
    const result = await global
      .knex('requests')
      .select('url')
      .where({ id: requestId });
    if (result[0].url !== page.url()) {
      clearInterval(domListenerId); // Stop this listener because it is out of date
      return;
    }

    // Fetch the page's current content
    let body;
    try {
      body = await page.content();
    } catch (e) {
      clearInterval(domListenerId); // This will run if you close the browser.
      return;
    }

    // Update the request in the database
    await global
      .knex('requests')
      .where({ id: requestId })
      .update({ response_body_rendered: body });

    // console.log(
    //   `[BrowserUtils] saved content for page: ${page.url()} (length: ${
    //     body.length
    //   }) to request ${requestId}, (DOMListener ${domListenerId})`
    // );
  }, 1000);

  return domListenerId;
};

module.exports = { handleNewPage };
