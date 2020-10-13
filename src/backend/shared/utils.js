const { snakeCase } = require('lodash');

const parseHost = (hostString, defaultPort) => {
  const m = hostString.match(/^http:\/\/(.*)/);
  if (m) {
    const parsedUrl = url.parse(hostString);
    return {
      host: parsedUrl.hostname,
      port: parsedUrl.port
    };
  }

  const hostPort = hostString.split(':');
  const host = hostPort[0];
  const port = hostPort.length === 2 ? +hostPort[1] : defaultPort;

  return {
    host: host,
    port: port
  };
};

const parseHostAndPort = (request, defaultPort) => {
  // eslint-disable-next-line no-useless-escape
  const m = request.url.match(/^http:\/\/([^\/]+)(.*)/);
  if (m) {
    request.url = m[2] || '/';
    return parseHost(m[1], defaultPort);
  } else if (request.headers.host) {
    return parseHost(request.headers.host, defaultPort);
  } else {
    return null;
  }
};


const objToSnakeCase = (obj) => {
  const snakeCaseObj = {};

  for (const key of Object.keys(obj)){
    if (obj.hasOwnProperty(key)) {
      snakeCaseObj[snakeCase(key)] = obj[key];
    }
  }

  return snakeCaseObj;
};

module.exports = { parseHost, parseHostAndPort, objToSnakeCase };
