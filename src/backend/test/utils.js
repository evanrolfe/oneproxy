const puppeteer = require('puppeteer-core');

const { DEFAULT_FILTERS } = require('../shared/constants');

const clearDatabase = async () => {
  // Clear capture_filters table:
  await global.knex.raw('DELETE FROM capture_filters;');
  await global.knex.raw('DELETE FROM SQLITE_SEQUENCE WHERE name="capture_filters";');

  // Clear requests table:
  await global.knex.raw('DELETE FROM requests;');
  await global.knex.raw('DELETE FROM SQLITE_SEQUENCE WHERE name="requests";');

  // Clear settings table:
  await global.knex.raw('DELETE FROM settings;');
  await global.knex.raw('DELETE FROM SQLITE_SEQUENCE WHERE name="settings";');

  // Create default capture filters:
  const filters = Object.assign({}, DEFAULT_FILTERS);
  filters.hostList = ['localhost:3000'];
  filters.hostSetting = 'include';

  await global
    .knex('capture_filters')
    .insert({ id: 1, filters: JSON.stringify(filters) });
};

const sleep = ms => new Promise(resolve => setTimeout(resolve, ms));

const writeToBackend = (line) => {
  global.backendProc.stdin.write(`${JSON.stringify(line)}\n`);
};

const messageFromBackend = (messageType) => new Promise((resolve) => {
  global.backendProc.stdout.on('data', (data) => {
    data.split('\n').forEach((line) => {
      if (line.substring(0,6) == '[JSON]') {
        let message;
        message = JSON.parse(line.substring(6).trim());

        if (message.type == messageType) {
          resolve(message);
        }
      }
    });
  });
});

const connectToBrowser = async (debugPort) => {
  return puppeteer.connect({
      browserURL: `http://localhost:${debugPort}`,
      defaultViewport: null
  });
};

module.exports = { clearDatabase, sleep, messageFromBackend, writeToBackend, connectToBrowser };
