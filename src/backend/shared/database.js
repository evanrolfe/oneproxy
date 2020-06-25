const knex = require('knex');
const schemaSql = require('./schema');

const setupDatabaseStore = async (databaseFile) => {
  const dbConn = knex({
    client: 'sqlite3',
    connection: {filename: databaseFile},
    useNullAsDefault: true
  });

  console.log(`[Backend] Loaded database ${databaseFile}`);

  // Check if we need to import the database schema:
  const tables = await dbConn.raw("SELECT name FROM sqlite_master WHERE type='table'");
  const tableNames = tables.map(table => table.name);

  if (
    !tableNames.includes('clients') ||
    !tableNames.includes('capture_filters') ||
    !tableNames.includes('intercept_filters') ||
    !tableNames.includes('requests') ||
    !tableNames.includes('settings') ||
    !tableNames.includes('websocket_messages')
  ) {
    console.log(`[Backend] importing database schema...`);
    const queries = schemaSql
    .toString()
    .replace(/(\r\n|\n|\r)/gm, ' ') // remove newlines
    .replace(/\s+/g, ' ') // excess white space
    .split(';') // split into all statements
    .map(Function.prototype.call, String.prototype.trim)
    .filter(el => el.length !== 0); // remove any empty ones

  for (let i = 0; i < queries.length; i++) {
    // eslint-disable-next-line no-await-in-loop
    await dbConn.raw(queries[i]);
  }
    console.log(`[Backend] schema imported.`);
  }

  return dbConn;
};

const importDatabaseSchema = async (dbConn) => {
  const queries = schemaSql
    .toString()
    .replace(/(\r\n|\n|\r)/gm, ' ') // remove newlines
    .replace(/\s+/g, ' ') // excess white space
    .split(';') // split into all statements
    .map(Function.prototype.call, String.prototype.trim)
    .filter(el => el.length !== 0); // remove any empty ones

  for (let i = 0; i < queries.length; i++) {
    // eslint-disable-next-line no-await-in-loop
    await dbConn.raw(queries[i]);
  }
};


module.exports = { setupDatabaseStore };
