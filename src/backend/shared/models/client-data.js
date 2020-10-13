//const frontend = require('../notify_frontend');
const { objToSnakeCase, objToCamelCase } = require('../utils');

class ClientData {
  constructor({id, title, cookies, pages, type, open, proxyPort, browserPort, createdAt, launchedAt}) {
    this.id = id;
    this.title = title;
    this.cookies = cookies;
    this.pages = pages;
    this.type = type;
    this.open = open;
    this.proxyPort = proxyPort;
    this.browserPort = browserPort;
    this.createdAt = createdAt;
    this.launchedAt = launchedAt;
  }

  static async create(params) {
    params.createdAt = Date.now();
    params.open = 0;
    const result = await global.knex('clients').insert(objToSnakeCase(params));

    params.id = result[0];
    params.title = `Browser #${params.id}`;
    await global.knex('clients').where({ id: params.id }).update({ title: params.title });

    return new ClientData(params);
  }

  static async load(id) {
    const result = await global.knex('clients').where({ id: id });
    const params = objToCamelCase(result[0]);

    return new ClientData(params);
  }

  async update(params) {
    await global.knex('clients').where({ id: this.id }).update(objToSnakeCase(params));
    Object.assign(this, params);
  }
}

module.exports = { ClientData };
