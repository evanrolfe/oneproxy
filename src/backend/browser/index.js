const launcher = require('@httptoolkit/browser-launcher');
const fs = require('fs');
const { instrumentBrowser } = require('./browser_utils');
const { COPYFILE_EXCL } = fs.constants;

const { getSPKIFingerprint } = require('../shared/cert-utils');

const createBrowserDb = async (type, browserPort, proxyPort) => {
    const result = await global
        .knex('clients')
        .insert({
          type: type,
          proxy_port: proxyPort,
          browser_port: browserPort,
          created_at: Date.now()
        });

    const browserId = result[0];

    await global
        .knex('clients')
        .where({ id: browserId })
        .update({ title: `Browser #${browserId}` });

    return browserId;
};

const getUsedPorts = async () => {
  const result = await global.knex('clients');
  const proxyPorts = result.map(row => row.proxy_port);
  const browserPorts = result.map(row => row.browser_port);

  return { proxy: proxyPorts, browser: browserPorts };
};

const getNextPortsAvailable = async (portsAvailable) => {
  const portsUsed = await getUsedPorts();

  const browserPort = portsAvailable.browser.find((availablePort) => {
    return !portsUsed.browser.includes(availablePort);
  });

  const proxyPort = portsAvailable.proxy.find((availablePort) => {
    return !portsUsed.proxy.includes(availablePort);
  });

  console.log(`[Backend] found available browser port: ${browserPort}, proxy port: ${proxyPort}`)
  return { browser: browserPort, proxy: proxyPort };
};

const listAvailableBrowsers = async (portsAvailable) => {
  launcher.detect(async (browsers) => {
    const ports = await getNextPortsAvailable(portsAvailable);

    // Add ports to the response:
    browsers.forEach((browser) => {
      browser.proxyPort = ports.proxy;
      browser.browserPort = ports.browser;
    });

    // Add "anything" browser
    browsers.push({
      name: 'anything',
      type: 'anything',
      proxyPort: ports.proxy,
      browserPort: ports.browser
    });

    //browsers = browsers.filter(b => b.type != 'chromium')

    const message = {
      type: 'clientsAvailable',
      clients: browsers
    };
    console.log(`[JSON] ${JSON.stringify(message)}`);
  });
};

const startChrome = async (proxyPort, debugPort, browserId, paths, proxyPid) => {
  return startChromeChromium('chrome', proxyPort, debugPort, browserId, paths, proxyPid);
};

const startChromium = async (proxyPort, debugPort, browserId, paths, proxyPid) => {
  return startChromeChromium('chromium', proxyPort, debugPort, browserId, paths, proxyPid);
};

const startChromeChromium = async (browserType, proxyPort, debugPort, browserId, paths, proxyPid) => {
  const spki = getSPKIFingerprint(paths.keyPath, paths.certPath);
  const profilePath = `${paths.tmpPath}/${browserType}-profile${browserId}`;

  return new Promise((resolve, reject) => {
    launcher(function(err, launch) {
      if (err) {
        console.error(err);
        return;
      }

      const launchOptions = {
        browser: browserType,
        profile: profilePath,
        proxy: `127.0.0.1:${proxyPort}`,
        noProxy: '<-loopback>',
        detached: false,
        options: [
          `--ignore-certificate-errors-spki-list=${spki}`,
          //`--user-data-dir=${profilePath}`,
          '--disable-sync',
          '--no-default-browser-check',
          '--disable-restore-session-state',
          '--disable-web-security',
          '--disable-features=IsolateOrigins,site-per-process',
          '--disable-site-isolation-trials',
          '-test-type',
          `--remote-debugging-port=${debugPort}`,
          '--window-size=1280,1080'
        ],
      };

      if (process.env.NODE_ENV === 'test') {
        launchOptions.options.push('--headless');
      }

      launch('', launchOptions, async (err, browserInstance) => {
        if (err) {
          console.error(err);
          return;
        }

        instrumentBrowser(browserId, debugPort);

        browserInstance.on('stop', function(code) {
          console.log('[Backend] Browser instance stopped with exit code:', code);
          console.log(`[Backend] Killing proxy process PID: ${proxyPid}`);
          try {
            process.kill(proxyPid);
            global.childrenPIds = global.childrenPIds.filter(pid => pid !== proxyPid);
          } catch(err) {
            // This will occur if we have already closed the proxy process i.e. on exit
            console.log(err.message)
          }
        });

        resolve(browserInstance.pid);
      });
    });
  });
};

//https://stackoverflow.com/questions/1435000/programmatically-install-certificate-into-mozilla
//https://developer.mozilla.org/en-US/docs/Mozilla/Command_Line_Options#User_Profile
//https://support.mozilla.org/en-US/kb/setting-certificate-authorities-firefox
//https://sadique.io/blog/2012/06/05/managing-security-certificates-from-the-console-on-windows-mac-os-x-and-linux/

// https://medium.com/@leonardodna/the-ultimate-newbie-guide-for-self-signed-certificates-d81aa3b9987b
// Generate root CA:
// openssl genrsa -des3 -out rootCA.key 4096
// openssl req -x509 -new -nodes -extensions v3_ca -key rootCA.key -sha256 -days 3650 -out rootCA.pem

// Generate cert:
// openssl genrsa -out testCA.key 4096
// openssl req -new -key testCA.key -out testCA.csr
// openssl x509 -req -in testCA.csr -CA rootCA.crt -CAkey rootCA.key -CAcreateserial -days 3650 -sha256 -out testCA.pem
// https://stackoverflow.com/questions/12219639/is-it-possible-to-dynamically-return-an-ssl-certificate-in-nodejs
const startFirefox = async (proxyPort, browserId, paths, proxyPid) => {
    const profilePath = `${paths.tmpPath}/firefox-profile${browserId}`;

    launcher(function(err, launch) {
      if (err) {
        return console.error(err);
      }

      // Copy cert9.db to thew new profile:
      if (!fs.existsSync(profilePath)){
        fs.mkdirSync(profilePath);
      }

      try {
        fs.copyFileSync(paths.cert9Path, `${profilePath}/cert9.db`, COPYFILE_EXCL);
      } catch (error) {
        // The cert9.db file already exists
        console.log(error);
      }

      const launchOptions = {
        browser: 'firefox',
        profile: profilePath,
        proxy: `127.0.0.1:${proxyPort}`,
        noProxy: '<-loopback>',
        detached: false,
        options: [],
        prefs: {
          'network.proxy.ssl': '"127.0.0.1"',
          'network.proxy.ssl_port': proxyPort,
          'network.proxy.http': '"127.0.0.1"',
          'network.proxy.http_port': proxyPort,
        }
      };

      launch('https://linuxmint.com/', launchOptions, function(err, instance) {
        if (err) {
          return console.error(err);
        }

        console.log('Instance started with PID:', instance.pid);

        instance.on('stop', function(code) {
          console.log('Instance stopped with exit code:', code);
        });
      });
    });
};

const startBrowser = async (client, paths, proxyPid) => {
  const browserId = client['id'];
  const browserType = client['type'];
  const proxyPort = client['proxy_port'];
  const debugPort = client['browser_port'];
  let browserPid;

  switch (browserType) {
    case 'chromium':
      browserPid = await startChromium(proxyPort, debugPort, browserId, paths, proxyPid);
      break;

    case 'chrome':
      browserPid = await startChrome(proxyPort, debugPort, browserId, paths, proxyPid);
      break;

    case 'firefox':
      startFirefox(proxyPort, browserId, paths, proxyPid);
      break;

    default:
      console.error(`[ERROR] Browser Type not recognised`);
  }

  return browserPid;
};

const closeAllClients = () => {
  global.childrenPIds.forEach((pid) => {
    console.log(`[Backend] closing client with PID: ${pid}`)
    process.kill(pid);
    console.log(`[Backend] ${pid} closed`)
  });
};

module.exports = {
  startBrowser,
  createBrowserDb,
  listAvailableBrowsers,
  closeAllClients,
  getNextPortsAvailable
};
