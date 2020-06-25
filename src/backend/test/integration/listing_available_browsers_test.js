const { sleep, clearDatabase, messageFromBackend, writeToBackend } = require('../utils');

describe('Listing the available browsers', () => {
  beforeEach(async () => {
    //await clearDatabase();
  });

  it('returns the browsers available on the system', async () => {
    writeToBackend({'command': 'listAvailableClientTypes'});

    const result = await messageFromBackend('clientsAvailable');

    const availableClients = result.clients;
    await sleep(5000);
    expect(availableClients.length).to.eql(4);
    console.log(availableClients)
    const clientTypes = availableClients.map(c => c.name).sort();
    console.log(clientTypes);
    expect(clientTypes).to.eql(['anything', 'chrome', 'chromium', 'firefox']);
  });
});

