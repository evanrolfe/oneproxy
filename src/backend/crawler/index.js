const { Crawler } = require('./crawler');
const { BaseConfig } = require('./config/base-config.js');

const startCrawler = async () => {
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

  const config = new BaseConfig(configArgs);
  const crawler = await Crawler.init({config: config});

  console.log(`======================> Crawling`)
  // await crawler.startCrawling();
  // console.log('Crawling...')
  // await crawler.onIdle();
  // console.log('Done crawling.')
  //await crawler.close();
  //return;
};

module.exports = { startCrawler };
