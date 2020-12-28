const { argv } = require('yargs');
const path = require('path');

const getPaths = () => {
  let appPath, dbPath;

  if(argv.appPath !== undefined) {
    appPath = argv.appPath;
  } else {
    appPath = path.join(__dirname, '../../../');
  }

  if(argv.dbPath !== undefined) {
    dbPath = argv.dbPath;
  } else {
    throw 'No dbPath option specified!';
  }

  console.log(`[Backend] appPath: ${appPath}`);
  console.log(`[Backend] dbPath: ${dbPath}`);

  const paths = {
    dbFile: dbPath,
    keyPath: `${appPath}rootCA.key`,
    certPath: `${appPath}rootCA.csr`,
    cert9Path: `${appPath}cert9.db`,
    tmpPath: `${appPath}tmp`,
  };

  return paths;
};

module.exports = { getPaths };
