const fs = require('fs');

const { generateCACertificate } = require('./shared/cert-utils');

const keyPath = '/home/evan/Code/oneproxypy/rootCA.key';
const certPath = '/home/evan/Code/oneproxypy/rootCA.csr';

// Top-level async function:
(async () => {
    const rootCert = await generateCACertificate();

    fs.writeFileSync(keyPath, rootCert.key);
    fs.writeFileSync(certPath, rootCert.cert);

    console.log(`Wrote key to ${keyPath}`);
    console.log(`Wrote cert to ${certPath}`);
})();

