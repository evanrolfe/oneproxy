const { fork } = require('child_process');

const { Crawler } = require('./crawler/crawler');
const { BaseConfig } = require('./crawler/config/base-config.js');

const { setupDatabaseStore } = require('./shared/database');
const CaptureFilters = require('./shared/models/capture-filters');
const frontend = require('./shared/notify_frontend');

// TODO: Use classes to organise this mess of functions in here and in browser/index.js
const loadDatabase = async (paths) => {
  global.knex = await setupDatabaseStore(paths.dbFile);
  // Ensure the default capture filters are created if they dont exist:
  await CaptureFilters.getFilters();
};

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

module.exports = { loadDatabase, startCrawler };
