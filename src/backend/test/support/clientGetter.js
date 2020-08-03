const { writeToBackend, messageFromBackend } = require('../utils');

class ClientGetter {
  constructor() {
    this.clients = {}
  }

  async get(clientType) {
    const existingClient = this.clients[clientType];

    if (existingClient !== undefined) return existingClient;

    writeToBackend({ "command": "createClient", "type": clientType });
    const result = await messageFromBackend('clientStarted');
    this.clients[clientType] = result.clientInfo;

    return result.clientInfo;
  }
}

module.exports = { ClientGetter };
