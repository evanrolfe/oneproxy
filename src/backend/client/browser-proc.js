const launcher = require('@httptoolkit/browser-launcher');

const { instrumentBrowserWithPuppeteer } = require('./browser/instrument-with-puppeteer');
const { getSPKIFingerprint } = require('../shared/cert-utils');
const frontend = require('../shared/notify_frontend');

class BrowserProc {
  constructor(clientData, paths, options) {
    this.clientData = clientData;
    this.paths = paths;
    this.options = options;
  }

  async start() {
    switch (this.clientData.type) {
      case 'chromium':
        await this._startChromium();
        break;

      case 'chrome':
        await this._startChrome();
        break;

      case 'firefox':
        this.startFirefox();
        break;

      default:
        console.error(`[ERROR] Browser Type not recognised`);
    }
  }

  onClosed(callbackFunc) {
    this.onClosedCallback = callbackFunc;
  }

  // Private Methods:
  async _closeClient() {
    await this.clientData.update({open: false});
    frontend.notifyClientsChanged();
  }

  async _startChrome() {
    return this._startChromeChromium('chrome');
  };

  async _startChromium() {
    return this._startChromeChromium('chromium');
  };

  async _startChromeChromium(browserType) {
    const spki = getSPKIFingerprint(this.paths.keyPath, this.paths.certPath);
    const profilePath = `${this.paths.tmpPath}/${browserType}-profile`;

    const launchOptions = {
      browser: browserType,
      profile: profilePath,
      proxy: `127.0.0.1:${this.clientData.proxyPort}`,
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
        `--remote-debugging-port=${this.clientData.browserPort}`,
        '--window-size=1280,1080',
        `--no-sandbox`,
        `--disable-setuid-sandbox`,
      ],
    };

    if (process.env.NODE_ENV === 'test') {
      launchOptions.options.push('--headless');
      // To fix intermittend failures on circleCI:
      // https://discuss.circleci.com/t/navigation-failed-because-browser-has-disconnected/29087
      // https://github.com/puppeteer/puppeteer/issues/4911
      launchOptions.options.push('--single-process');
    } else if(this.options.headless === true) {
      launchOptions.options.push('--headless');
    }

    const browserInstance = await new Promise((resolve, reject) => {
      launcher(function(err, launch) {
        if (err) {
          console.error(err);
          return;
        }

        launch('', launchOptions, async (err, browserInstance) => {
          if (err) {
            console.log(`[Backend] Error: ${err}`);
            return;
          }

          resolve(browserInstance);
        });
      });
    });


    browserInstance.on('stop', async (code) => {
      console.log('[Backend] Browser instance stopped with exit code:', code);
      try {
        if(this.onClosedCallback) this.onClosedCallback();
      } catch(err) {
        // This will occur if we have already closed the proxy process i.e. on exit
        console.log(err.message)
      } finally {
        this._closeClient();
      }
    });

    this.puppeteerBrowser = await instrumentBrowserWithPuppeteer(this.clientData.id, this.clientData.browserPort);
    this.pid = browserInstance.pid;
  }

/*
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
          // TODO: Make this remove the PIDS from the global var just like startChromeChromium() does
          console.log('Instance stopped with exit code:', code);
        });
      });
    });
  };
*/
}

module.exports = { BrowserProc };
