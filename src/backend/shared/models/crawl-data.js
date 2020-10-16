//const frontend = require('../notify_frontend');
const { objToSnakeCase, objToCamelCase } = require('../utils');

const STATUSES = ['created', 'running', 'finished'];

class CrawlData {
  constructor({ id, clientId, config, status, createdAt, startedAt, finishedAt }) {
    this.id = id;
    this.clientId = clientId;
    this.config = config;
    this.status = status;
    this.createdAt = createdAt;
    this.startedAt = startedAt;
    this.finishedAt = finishedAt;
  }

  static async create(params) {
    params.createdAt = Date.now();
    params.status = STATUSES[0];

    const result = await global.knex('crawls').insert(objToSnakeCase(params));
    params.id = result[0];

    return new CrawlData(params);
  }

  static async load(id) {
    const result = await global.knex('crawls').where({ id: id });
    const params = objToCamelCase(result[0]);

    return new CrawlData(params);
  }

  // async update(params) {
  //   await global.knex('clients').where({ id: this.id }).update(objToSnakeCase(params));
  //   Object.assign(this, params);
  // }

  configObj() {
    return JSON.parse(this.config);
  }
}

module.exports = { CrawlData };
