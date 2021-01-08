const DEFAULT_SETTINGS = {
  interceptEnabled: false
};

class Settings {
  static async createDefaultIfNotExists() {
    Object.keys(DEFAULT_SETTINGS).forEach((key) => {
      this.getSetting(key);
    });
  }

  static async getSetting(key) {
    let result = await global.knex('settings').where({ key: key });

    if (result.length === 0) {
      try {
        await this.createDefault(key);
      } catch(err) {
        console.log(`Could not create default setting for ${key}: ${err.message}`)
      }

      result = await global
        .knex('settings')
        .where({ key: key })
        .select();
    }

    return result[0];
  }

  static async changeSetting({key, value}) {
    const setting = await this.getSetting(key);

    await global
        .knex('settings')
        .where({ id: setting.id })
        .update({ value: value });

      const message = {
        type: 'settingChanged',
        setting: {id: setting.id, key: key, value: value}
      };
      console.log(`[JSON] ${JSON.stringify(message)}`);
  }

  static async createDefault(key) {
    console.log(`[Backend] Creating default setting for ${key}...`);
    return global
      .knex('settings')
      .insert({ key: key, value: DEFAULT_SETTINGS[key] });
  }
}

module.exports = Settings;
