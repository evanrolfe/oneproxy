const { sleep, clearDatabase, writeToBackend, messageFromBackend, clearDatabaseTable } = require('../../utils');

describe('closeAllClients Command', () => {
  let result;

  before(async () => {
    await clearDatabase();
  });

  context('with a chrome client and anything client started', () => {
    before(async () => {
      writeToBackend({ "command": "createClient", "type": 'chrome' });
      await messageFromBackend('clientStarted');
      writeToBackend({ "command": "createClient", "type": 'anything' });
      await messageFromBackend('clientStarted');

      writeToBackend({ "command": "closeAllClients"});
      result = await messageFromBackend('clientsClosed');
    });


    it('closes the clients', async () => {
      expect(result.type).to.eq('clientsClosed');
    });
  });
});

