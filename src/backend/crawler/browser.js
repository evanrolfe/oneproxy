const Puppeteer = require('puppeteer');

class Browser {
  constructor(puppeteerBrowser, maxConcurrency, browserLaunched) {
    this.puppeteerBrowser = puppeteerBrowser;
    this.maxConcurrency = maxConcurrency;
    this.pendingRequests = 0;
    this.browserLaunched = browserLaunched;
  }

  static async init(config) {
    const maxConcurrency = (config.maxConcurrency !== undefined) ? config.maxConcurrency : 10;

    const puppeteerBrowser = await Puppeteer.connect({
      browserWSEndpoint: config.browserWSEndpoint
    });
    const browserLaunched = false;

    const browser = new Browser(puppeteerBrowser, maxConcurrency, browserLaunched);
    return browser;
  }

  tabsAvailable() {
    return (this.pendingRequests < this.maxConcurrency);
  }

  async getTab() {
    const tab = this.puppeteerBrowser.newPage();
    return tab;
  }

  async disconnect() {
    if(this.browserLaunched === true) {
      await this.puppeteerBrowser.close();
    } else {
      await this.puppeteerBrowser.disconnect();
    }
  }
}

module.exports = { Browser };
