const { sleep, clearDatabase, messageFromBackend, writeToBackend } = require('../utils');

describe('Listing the available browsers', () => {
  beforeEach(async () => {
    //await clearDatabase();
  });

  it('returns the browsers available on the system', async () => {
    writeToBackend({'command': 'listAvailableClientTypes'});

    const result = await messageFromBackend('clientsAvailable');

    const availableClients = result.clients;
    console.log(availableClients)

    const clientTypes = availableClients.map(c => c.name).sort();
    expect(clientTypes).to.include('chrome');
    expect(clientTypes).to.include('firefox');
    expect(clientTypes).to.include('anything');
  });
});

