const { DEFAULT_FILTERS } = require('../constants');

class CaptureFilters {
  static async getFilters() {
    let result = await global
      .knex('capture_filters')
      .where({ id: 1 })
      .select();

    if (result.length === 0) {
      console.log(`No capture_filters found, so creating default..`);

      try {
        await this.createDefault();
      } catch(err) {
        // Race condition: the default filters have already been created so we ignore this error
      }

      result = await global
        .knex('capture_filters')
        .where({ id: 1 })
        .select();
    }

    return JSON.parse(result[0].filters);
  }

  static async setFilters(newValuesObj) {
    let result = await global
      .knex('capture_filters')
      .where({ id: 1 })
      .select();

    if (result.length === 0) {
      console.log(`No capture_filters found, so creating default..`);
      try {
        await this.createDefault();
      } catch(err) {
        // Race condition: the default filters have already been created so we ignore this error
      }

      result = await global
        .knex('capture_filters')
        .where({ id: 1 })
        .select();
    }

    const filters = JSON.parse(result[0].filters);
    const newFilters = Object.assign({}, filters);

    Object.keys(newValuesObj).forEach(key => {
      newFilters[key] = newValuesObj[key];
    });

    await global
      .knex('capture_filters')
      .where({ id: 1 })
      .update({ filters: JSON.stringify(newFilters) });
  }

  static async createDefault() {
    console.log('Creating default CaptureFilters...');
    const defaultFilters = JSON.stringify(DEFAULT_FILTERS);
    return global
      .knex('capture_filters')
      .insert({ id: 1, filters: defaultFilters });
  }

  static async shouldRequestBeCaptured(request) {
    const filters = await this.getFilters();

    // Filter Host (include):
    if (
      filters.hostList.length > 0 &&
      filters.hostSetting === 'include' &&
      !filters.hostList.includes(request.host)
    ) {
      return false;
    }

    // Filter Host (exclude):
    if (
      filters.hostList.length > 0 &&
      filters.hostSetting === 'exclude' &&
      filters.hostList.includes(request.host)
    ) {
      return false;
    }

    // Filter Path (include):
    if (filters.pathList.length > 0 && filters.pathSetting === 'include') {
      const anyPathsMatch = filters.pathList
        .map(path => request.path.includes(path))
        .some(x => x === true);

      if (anyPathsMatch === false) return false;
    }

    // Filter Path (exclude):
    if (filters.pathList.length > 0 && filters.pathSetting === 'exclude') {
      const anyPathsMatch = filters.pathList
        .map(path => request.path.includes(path))
        .some(x => x === true);

      if (anyPathsMatch === true) return false;
    }

    // Filter Ext (include):
    if (
      filters.extList.length > 0 &&
      filters.extSetting === 'include' &&
      !filters.extList.includes(request.ext)
    ) {
      return false;
    }

    // Filter Ext (exclude):
    if (
      filters.extList.length > 0 &&
      filters.extSetting === 'exclude' &&
      filters.extList.includes(request.ext)
    ) {
      return false;
    }

    return true;
  }
}

module.exports = CaptureFilters;
