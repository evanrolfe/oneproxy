const { Client } = require('./client');
const frontend = require('../shared/notify_frontend');

class ClientStore {
  constructor() {
    this.clients = [];
  }

  async createClient(type, paths) {
    const client = await Client.create(type, paths);

    client.onBrowserClosed(() => {
      this.closeClient(client.clientData.id);
    });

    this.clients.push(client);
    return client;
  }

  async loadClient(id, paths, options) {
    const client = await Client.load(id, paths, options);

    client.onBrowserClosed(() => {
      this.closeClient(client.clientData.id);
    });

    this.clients.push(client);
    return client;
  }

  closeClient(id) {
    console.log(`[Backend] ClientStore: closing client ${id}`)

    const client = this.clients.find(c => c.clientData.id === id);
    client.close();

    this.clients = this.clients.filter(c => c !== client);
  }

  bringToFrontClient(id) {
    console.log(`[Backend] ClientStore: bringToFront client ${id}`)

    const client = this.clients.find(c => c.clientData.id === id);
    client.bringToFront();
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
