const { Client } = require('./client');
const frontend = require('../shared/notify_frontend');

class ClientStore {
  constructor() {
    this.clients = [];
  }

  async createClient(type, paths) {
    const client = await Client.create(type, paths);

    client.onBrowserClosed(() => {
      this.closeClient(client);
    });

    this.clients.push(client);
    return client;
  }

  async loadClient(id, paths) {
    const client = await Client.load(id, paths);

    this.clients.push(client);
    return client;
  }

  closeClient(client) {
    console.log(`[Backend] ClientStore: closing client ${client.clientData.id}`)

    client.close();
    this.clients = this.clients.filter(c => c !== client);
  }

  closeAll() {
    console.log(`[Backend] ClientStore: closing ${this.clients.length} clients`)

    this.clients.forEach((client) => {
      client.close();
    });

    frontend.notifyClientsClosed();
  }
}

module.exports = { ClientStore };
