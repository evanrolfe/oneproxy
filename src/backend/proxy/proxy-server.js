const http = require('http');
const tls = require('tls');
const { argv } = require('yargs');
const httpolyglot = require('httpolyglot');

const { CA } = require('../shared/cert-utils');
const proxyRequestListener = require('./proxy-request-listener');

//import InterceptServer from './intercept-server';
const handleUpgrade = require('./websocket-handler');

const log = console;

const mightBeTLSHandshake = byte => byte === 22;

const peekFirstByte = socket =>
  new Promise(resolve => {
    socket.once('data', data => {
      socket.pause();
      socket.unshift(data);
      resolve(data[0]);
    });
  });

const startProxyServer = async (portNumber, browserId, interceptClient, paths) => {
  console.log(`[Proxy] Starting proxy server for browser ${browserId}...`);

  const ca = new CA(paths.keyPath, paths.certPath, 2048);
  const defaultCert = ca.generateCertificate('localhost');

  const server = httpolyglot.createServer(
    {
      key: defaultCert.key,
      cert: defaultCert.cert,
      ca: [defaultCert.ca],
      SNICallback: (domain, callback) => {
        try {
          const generatedCert = ca.generateCertificate(domain);
          callback(null, tls.createSecureContext({
            key: generatedCert.key,
            cert: generatedCert.cert,
            ca: generatedCert.ca
          }));
        } catch (e) {
          console.error('Cert generation error', e);
          callback(e);
        }
      }
    },
    proxyRequestListener.bind(null, browserId, interceptClient)
  );

  // Used in our oncertcb monkeypatch above, as a workaround for https://github.com/mscdex/httpolyglot/pull/11
  server.disableTlsHalfOpen = true;

  server.on('tlsClientError', (error, socket) => {
    // These only work because of oncertcb monkeypatch above
    tlsClientErrorListener({
      failureCause: error,
      hostname: socket.servername,
      remoteIpAddress: socket.initialRemoteAddress,
      tags: []
    });
  });

  server.on('secureConnection', (tlsSocket) =>
    ifTlsDropped(tlsSocket, () => {
      tlsClientErrorListener({
        failureCause: 'closed',
        hostname: tlsSocket.servername,
        remoteIpAddress: tlsSocket.remoteAddress,
        tags: []
      });
    })
  );

  server.addListener('connect', (req, socket) => {
    const [targetHost, port] = req.url.split(':');

    socket.once('error', e => console.log('[Proxy] Error on client socket', e));

    socket.write(
      `HTTP/${req.httpVersion} 200 OK\r\n\r\n`,
      'utf-8',
      async () => {
        const firstByte = await peekFirstByte(socket);

        // Tell later handlers whether the socket wants an insecure upstream
        socket.upstreamEncryption = mightBeTLSHandshake(firstByte);

        if (socket.upstreamEncryption) {
          //console.log(`[Proxy] Unwrapping TLS connection to ${targetHost}`);
          unwrapTLS(targetHost, port, socket);
        } else {
          // Non-TLS CONNECT, probably a plain HTTP websocket. Pass it through untouched.
          //console.log(`[Proxy] Passing through connection to ${targetHost}`);
          server.emit('connection', socket);
          socket.resume();
        }
      }
    );
  });

  server.on('upgrade', handleUpgrade);

  const unwrapTLS = (targetHost, port, socket) => {
    const generatedCert = ca.generateCertificate(targetHost);

    let tlsSocket = new tls.TLSSocket(socket, {
      isServer: true,
      server: server,
      secureContext: tls.createSecureContext({
        key: generatedCert.key,
        cert: generatedCert.cert,
        ca: generatedCert.ca
      })
    });

    // Wait for:
    // * connect, not dropped -> all good
    // * _tlsError before connect -> cert rejected
    // * sudden end before connect -> cert rejected
    new Promise((resolve, reject) => {
      tlsSocket.on('secure', () => {
        resolve();
      });

      tlsSocket.on('_tlsError', error => {
        reject(error);
      });

      tlsSocket.on('end', () => {
        // Delay, so that simultaneous specific errors reject first
        // eslint-disable-next-line prefer-promise-reject-errors
        setTimeout(() => reject('closed'), 1);
      });
    }).catch(cause => console.log(`[Proxy] tlsSocket FAILED: ${cause}`));

    const innerServer = http.createServer((req, res) => {
      // Request URIs are usually relative here, but can be * (OPTIONS) or absolute (odd people) in theory
      if (req.url !== '*' && req.url[0] === '/') {
        req.url = `https://${targetHost}:${port}${req.url}`;
      }
      return proxyRequestListener(browserId, interceptClient, req, res);
    });
    innerServer.addListener('upgrade', (req, innerSocket, head) => {
      req.url = `https://${targetHost}:${port}${req.url}`;
      server.emit('upgrade', req, innerSocket, head);
    });
    innerServer.addListener('connect', (req, res) =>
      server.emit('connect', req, res)
    );

    innerServer.emit('connection', tlsSocket);
  };

  server.listen(portNumber);
  console.log(`[Proxy] Server listening on ${portNumber}`);
};

module.exports = { startProxyServer };
