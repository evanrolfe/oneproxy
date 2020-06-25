const { argv } = require('yargs');
const path = require('path');

const getPaths = () => {
  let basePath;

  if(argv.basePath !== undefined) {
    basePath = argv.basePath;
  } else {
    basePath = path.join(__dirname, '../../../');
  }

  console.log(`[Backend] basePath: ${basePath}`);
  const paths = {
    dbFile: `${basePath}tmp/${process.env.NODE_ENV}.db`,
    keyPath: `${basePath}rootCA.key`,
    certPath: `${basePath}rootCA.csr`,
    cert9Path: `${basePath}cert9.db`,
    tmpPath: `${basePath}tmp`,
  };

  if (argv.db !== undefined) {
    paths.dbFile = argv.db;
  }

  return paths;
};

module.exports = { getPaths };
