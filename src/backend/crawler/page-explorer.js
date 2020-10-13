
class PageExplorer {
  constructor(page, pageUrl, config) {
    this.page = page;

    // TODO: sometimes pageUrl != page.url() for example www.example.com vs www.example.com/
    this.pageUrl = pageUrl;
    this.config = config;
    this.buttonsClicked = [];
  }

  // TODO: Make this click buttons recursively until max depth reached or there are no more buttons to click
  async getLinks() {
    let links = await this._scrapeLinks();

    if(this.config.clickButtons !== true) {
      return links;
    }

    // TODO: Move these function definitions outside of getLinks()
    //this._verboseLog(`${this.pageUrl} PageExplorer: exposing functions...`);
    // await this.page.exposeFunction('doNotClickButton', async (outerHTML) => {
    //   if(this.buttonsClicked.includes(outerHTML)) {
    //     return true;
    //   }
    //   const ignoreButton = this.config.ignoreButton(outerHTML);

    //   return ignoreButton;
    // });

    // await this.page.exposeFunction('buttonClicked', (outerHTML) => {
    //   this.buttonsClicked.push(outerHTML);
    // });

    //this._verboseLog(`${this.pageUrl} PageExplorer: clicking buttons...`);
    //await this.page.$$eval(this.config.buttonXPath, this._pageClickButtons);
    //this._verboseLog(`${this.pageUrl} PageExplorer: done. Waiting...`);

    await this.page.waitFor(200); // NOTE: Increasing this to 1sec causes PageExplorer to hang
    const newLinks = []; //await this._scrapeLinks();

    links = links.concat(newLinks);
    const uniqueLinks = [...new Set(links)];

    return uniqueLinks;
  }

  async _scrapeLinks() {
    this._verboseLog(`${this.pageUrl} PageExplorer: scraping links...`);

    return this.page.evaluate(() => {
      const links = document.querySelectorAll("a");
      const urls = Array.from(links).map(link => link.href)
      return urls;
    });

    // TODO: WHy the f*** does this line not work? It raises this error when called in a react app:
    // "Protocol error (Runtime.callFunctionOn): Object reference chain is too long undefined"
    //return this.page.$$eval('a', links => links.map(link => link.href));
  }

  // Page functions only gets executed inside the browser window context
  async _pageClickButtons(buttons) {
    // for(let i = 0; i < buttons.length; i++) {
    //   let button = buttons[i];
    //   const doNotClick = await doNotClickButton(button.outerHTML);

    //   if(doNotClick===false) {
    //     await button.click();
    //     buttonClicked(button.outerHTML);
    //   }
    // }
  }

  _verboseLog(message) {
    if(this.config.verboseOutput === true) {
      console.log(message);
    }
  }
}

module.exports = { PageExplorer };
