const launcher = require('@httptoolkit/browser-launcher');

const { instrumentBrowserWithPuppeteer } = require('./browser/instrument-with-puppeteer');
const { getSPKIFingerprint } = require('../shared/cert-utils');

class Browser {
  constructor(clientData, paths, proxy) {
    this.clientData = clientData;
    this.paths = paths;
    this.proxy = proxy;
  }

  async start() {
    switch (this.clientData.type) {
      case 'chromium':
        await this.startChromium();
        break;

      case 'chrome':
        await this.startChrome();
        break;

      case 'firefox':
        this.startFirefox();
        break;

      default:
        console.error(`[ERROR] Browser Type not recognised`);
    }
  }

  // Private Methods:
  async startChrome() {
    return this.startChromeChromium('chrome');
  };

  async startChromium() {
    return this.startChromeChromium('chromium');
  };

  async startChromeChromium(browserType) {
    const spki = getSPKIFingerprint(this.paths.keyPath, this.paths.certPath);
    const profilePath = `${this.paths.tmpPath}/${browserType}-profile${this.clientData.id}`;

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

    browserInstance.on('stop', function(code) {
      console.log('[Backend] Browser instance stopped with exit code:', code);
      console.log(`[Backend] Killing proxy process PID: ${this.proxy.pid}`);
      try {
        process.kill(proxyPid);
        // TODO: Move this out of the class:
        global.childrenPIds = global.childrenPIds.filter(pid => pid !== proxyPid);
      } catch(err) {
        // This will occur if we have already closed the proxy process i.e. on exit
        console.log(err.message)
      } finally {
        // TODO: Update this.clientData with open=false
        //closeClientDb();
      }
    });

    this.puppeteerBrowser = await instrumentBrowserWithPuppeteer(this.clientData.id, this.clientData.browserPort);
    this.pid = browserInstance.pid;
  }
}

module.exports = { Browser };
