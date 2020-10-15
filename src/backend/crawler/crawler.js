const { LinkQueue } = require('./link-queue.js');
const { Browser } = require('./browser.js');
const { PageExplorer } = require('./page-explorer.js');
const { PageEventsHandler } = require('./page-events-handler.js');

const EventEmitter = require('events');
const { parse, resolve } = require('url');
const trim = require('lodash/trim');
const startsWith = require('lodash/startsWith');
const includes = require('lodash/includes');
const noop = require('lodash/noop');
const uuid = require('uuid');

class Crawler {
  constructor(browser, options) {
    this.browser = browser;
    this.events = new EventEmitter();
    this.linkQueue = new LinkQueue();
    this.visitedUrls = [];
    this._resolveIdle = noop;
    this.currentUser = 'Public';

    //this.apiEndpointData = options.apiEndpointData;
    this.config = options.config;
    this.processEvents = (options.processEvents === undefined) ? true : options.processEvents;

    if(this.processEvents === true) {
      this.events.on('url queued', (urlObj) => {

        if(this.browser.tabsAvailable()) {
          this.linkQueue.dequeue(urlObj.url);
          this.crawlPage(urlObj.url, urlObj.depth);

        } else {
          setTimeout(() => {
            this.events.emit('url queued', urlObj);
          }, 100);
        }

      });
    }
  }

  static async init(options={}) {
    const browser = await Browser.init(options.config);
    const crawler = new Crawler(browser, options);
    return crawler;
  }

  async close() {
    await this.browser.disconnect();
  }

  onIdle() {
    return new Promise(resolve => {
      this._resolveIdle = resolve;
    });
  }

  async login(username, password) {
    this.currentUser = username;

    const tab = await this.browser.getTab();
    console.log(`Logging in as ${username}...`);
    await this.config.loginFunction(tab, username, password);
    console.log('Logged in.');

    // Hack: request.headers() does not include Cookies so we have to manually save them from the login request
    //       and then send them back to apiEndpointData
    const cookies = await tab.cookies();
    this.cookiesStr = cookies.map((cookie) => { return `${cookie.name}=${cookie.value}`; }).join('; ');

    await tab.close();
  }

  async logout() {
    const tab = await this.browser.getTab();
    return this.config.logoutFunction(tab);
  }

  handleDialog(pageUrl, currentUser, dialog) {
    dialog.accept();
  }

  async startCrawling() {
    this.crawlPage(this.config.baseUrl, 0);
  }

  async crawlPage(url, depth) {
    if(depth > this.config.maxDepth) {
      return;
    }

    this.browser.pendingRequests++;
    this.visitedUrls.push(url);
    const id = uuid.v4();

    // Start a monitor process so we can identify pages which are stuck
    let seconds = 0;
    const monitorProcess = setInterval(() => {
      if(seconds >= 10 && (seconds % 5) == 0) {
        console.log(`WARN: Been crawling ${url} for ${seconds} seconds`);
      }

      seconds++;
    }, 1000);

    this._verboseLog(`${depth}. Crawling ${url}`);

    // Open a new tab at this url with Network request interception enabled
    const tab = await this.browser.getTab();
    this._verboseLog(`${url} - Got a tab.`);

    tab.on('dialog', (dialog) => this.handleDialog(url, this.currentUser, dialog));
    this._verboseLog(`${url} - Going to url...`);

    const pageEvents = new PageEventsHandler(tab);

    try {
      const pageResponse = await tab.goto(url);
      this._verboseLog(`${url} - Got a response.`);

      // Wait until timeout limit for XHR
      await pageEvents.waitForRequestsToFinish(this.config.xhrTimeout);

      this._verboseLog(`${url} - Finished waiting for XHR requests or they have all completed.`);
      await tab.waitFor(this.config.waitOnEachPage);

      // Gather & process links from the page
      this._verboseLog(`${url} - Launching PageExplorer...`);
      const pageExplorer = new PageExplorer(tab, url, this.config);
      const links = await pageExplorer.getLinks();

      if(this.config.clickButtons === true) {
        await pageEvents.waitForRequestsToFinish(this.config.xhrTimeout);
      }

      this._verboseLog(`${url} - Got ${links.length} links from PageExplorer...`);
      await tab.close();
      this._verboseLog(`${url} -Tab closed.`);

      this._verboseLog(`${url} - Processing links...`);
      this.processLink(links, depth);
      this._verboseLog(`${url} - Done Processing links.`);

    } catch(error) {
      console.log(`ERROR: ${url} - Could not process:`);
      console.log(error.message);

    } finally {
      this.browser.pendingRequests--;
      clearInterval(monitorProcess);

      this._log(`Crawled ${url}`);

      // Check if the crawler is complete
      if(this.complete()) {
        console.log(`[Backend] Crawler finished.`)
        this._resolveIdle();
      }
    }
  }

  processLink(links, depth) {
    links.forEach((link) => {
      link = this.resolveUrl(link, this.config.baseUrl);

      if(link == null) {
        return;
      }

      const notAlreadyVisted = !includes(this.visitedUrls, link);
      const notAlreadyQueued = !this.linkQueue.alreadyQueued(link);
      const ignoreLink = this.ignoreLink(link);

      if(link !== null && notAlreadyVisted && notAlreadyQueued && !ignoreLink) {
        this._verboseLog(`Queued link: ${link}`)
        this.linkQueue.enqueue(link);
        this.events.emit('url queued',{url: link, depth: depth+1});
      } else {
        this._verboseLog(`Ignoring link: ${link}`)
      }
    });
  }

  resolveUrl(url, baseUrl) {
    url = trim(url);
    if (!url) return null;
    if (startsWith(url, '#')) return null;
    const { protocol } = parse(url);
    if (includes(['http:', 'https:'], protocol)) {
      return url.split('#')[0];
    } else if (!protocol) { // eslint-disable-line no-else-return
      return resolve(baseUrl, url).split('#')[0];
    }
    return null;
  }

  ignoreLink(url) {
    if(typeof(this.config) == 'object' && typeof(this.config.ignoreLink) == 'function') {
      return this.config.ignoreLink(url);
    } else {
      return false;
    }
  }

  complete() {
    return !(this.linkQueue.length > 0 || this.browser.pendingRequests > 0 );
  }

  _log(message) {
    console.log(message);
  }

  _verboseLog(message) {
    if(this.config.verboseOutput === true) {
      console.log(message);
    }
  }
}

module.exports = { Crawler };
