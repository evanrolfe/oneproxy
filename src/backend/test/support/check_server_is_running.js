const http = require('http');


const checkServerIsRunning = () => new Promise((resolve, reject) => {
  http.get('http://localhost:3000', {}, (res) => {
    let rawData;

    res.on('data', (chunk) => { rawData += chunk; });

    res.on('end', () => {
      resolve();
    });

  }).on('error', (err) => {
    if (err.code === 'ECONNREFUSED') {
      throw new Error('You must be running the example app on port 3000, see README.md for more details!');
    } else {
      throw err;
    }
  });;
});

module.exports = { checkServerIsRunning };
