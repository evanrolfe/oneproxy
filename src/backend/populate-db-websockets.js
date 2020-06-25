import database from '../shared/database';
import { DATABASE_FILES } from '../shared/constants';

const populateDb = async () => {
  console.log(`Populating...`);
  const dbFile = DATABASE_FILES[process.env.NODE_ENV];
  console.log(`Loading database from ${dbFile}`);
  const knex = await database.setupDatabaseStore(dbFile);
  console.log(`Database loaded.`);

  const messageParams = {
    request_id: 683,
    direction: 'incoming',
    body: 'Hello world!',
    created_at: Date.now()
  };
  const limit = 10000;

  for (let i = 0; i < limit; i++) {
    // eslint-disable-next-line no-await-in-loop
    const result = await knex('websocket_messages').insert(messageParams);
    console.log(`Inserted websocket message ${result[0]}`);
  }

  console.log(`Done.`);
};

if (process.env.NODE_ENV === undefined) {
  throw new Error(
    `You must set the NODE_ENV var!\ni.e. NODE_ENV=development yarn populate-db`
  );
}

populateDb();
