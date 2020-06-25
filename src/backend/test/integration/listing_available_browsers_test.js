const { sleep, clearDatabase, messageFromBackend, writeToBackend } = require('../utils');

describe('Listing the available browsers', () => {
  beforeEach(async () => {
    //await clearDatabase();
  });

  it('returns the browsers available on the system', async () => {
    writeToBackend({'command': 'listAvailableClientTypes'});

    const result = await messageFromBackend('clientsAvailable');

    console.log(`[TEST] The following browsers are`)
    console.log(result)

    const availableClients = result.clients;
    await sleep(3000);
    const clientTypes = availableClients.map(c => c.name).sort();
    console.log(clientTypes);

    // NOTE: This is specific to the circleCI node-browsers docker image
    expect(clientTypes).to.include('firefox');
    expect(clientTypes).to.include('chrome');
    expect(clientTypes).to.include('anything');
  });
});

