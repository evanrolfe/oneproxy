const { Crawler } = require('./crawler.js');
const { BaseConfig } = require('./config/base-config.js');

const configArgs = {
  "baseUrl": "http://localhost",
  "clickButtons": false,
  "buttonXPath": 'button',
  "maxDepth": 3,
  "xhrTimeout": 5,
  "pageTimeout": 30,
  "verboseOutput": true,
  "headless": false,
  "ignoreLink": function(url) {
    if(url.includes('/users/sign_out')) {
      return true;
    }

    return false;
  },
  "ignoreButton": function(outerHTML) {
    if(outerHTML.includes('Logout') || outerHTML.includes('submit') || outerHTML.includes('Save')) {
      return true;
    }

    return false;
  }
};

console.log('Starting crawler...');

(async () => {
  const config = new BaseConfig(configArgs);
  const crawler = await Crawler.init({config: config});

  await crawler.startCrawling();
  console.log('Crawling...')
  await crawler.onIdle();
  console.log('Done crawling.')
  //await crawler.close();
  //return;
})();

