const { ClientData } = require('../shared/models/client-data');
const { generateCertsIfNotExists } = require('../shared/cert-utils');
const frontend = require('../shared/notify_frontend');
const { Browser } = require('./browser');
const { Proxy } = require('./proxy');
const { PORTS_AVAILABLE } = require('../shared/constants');

class Client {
  constructor(clientData, paths) {
    this.clientData = clientData;
    this.paths = paths;
  }

  static async create(type, paths) {
    const ports = await _getNextPortsAvailable(PORTS_AVAILABLE);
    const clientData = await ClientData.create({type: type, browserPort: ports.browser, proxyPort: ports.proxy});

    return new Client(clientData, paths)
  }

  static async load(id, paths) {
    const clientData = await ClientData.load(id);

    return new Client(clientData, paths)
  }

  async start() {
    await generateCertsIfNotExists(this.paths.keyPath, this.paths.certPath);

    await this._startProxy();

    if (this.clientData.type !== 'anything') {
      await this._startBrowser();
    }

    await this.clientData.update({open: true})
    frontend.notifyClientsChanged();
    frontend.notifyClientStarted(this.clientData);
  }

  // Private Methods:
  async _startProxy() {
    this.proxy = new Proxy(this.clientData, this.paths);
    await this.proxy.start();

    // TODO: Move this outside of this class:
    global.childrenPIds.push(this.proxy.pid);
  }

  async _startBrowser() {
    const browser = new Browser(this.clientData, this.paths, this.proxy);
    await browser.start();
    // TODO: Move this outside of this class:
    global.childrenPIds.push(browser.pid);
  }
}

const _getUsedPorts = async () => {
  const result = await global.knex('clients');
  const proxyPorts = result.map(row => row.proxy_port);
  const browserPorts = result.map(row => row.browser_port);

  return { proxy: proxyPorts, browser: browserPorts };
};

const _getNextPortsAvailable = async (portsAvailable) => {
  const portsUsed = await _getUsedPorts();

  const browserPort = portsAvailable.browser.find((availablePort) => {
    return !portsUsed.browser.includes(availablePort);
  });

  const proxyPort = portsAvailable.proxy.find((availablePort) => {
    return !portsUsed.proxy.includes(availablePort);
  });

  console.log(`[Backend] found available browser port: ${browserPort}, proxy port: ${proxyPort}`)
  return { browser: browserPort, proxy: proxyPort };
};

module.exports = { Client };
