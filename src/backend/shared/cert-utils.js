const forge = require('node-forge');
const uuid = require('uuid');
const fs = require('fs');

const {
  pki,
  md,
  util: { encode64 }
} = forge;

const generateCACertificate = async (options = {}) => {
  options = {
    commonName: 'OneProxy Mock CA - FOR TESTING ONLY',
    bits: 2048
  };

  const keyPair = await new Promise((resolve, reject) => {
    pki.rsa.generateKeyPair({ bits: options.bits }, (error, keyPair2) => {
      if (error) reject(error);
      else resolve(keyPair2);
    });
  });

  const cert = pki.createCertificate();
  cert.publicKey = keyPair.publicKey;
  cert.serialNumber = uuid.v4().replace(/-/g, '');

  cert.validity.notBefore = new Date();
  // Make it valid for the last 24h - helps in cases where clocks slightly disagree
  cert.validity.notBefore.setDate(cert.validity.notBefore.getDate() - 1);

  cert.validity.notAfter = new Date();
  // Valid for the next year by default.
  cert.validity.notAfter.setFullYear(cert.validity.notAfter.getFullYear() + 1);

  cert.setSubject([{ name: 'commonName', value: options.commonName }]);

  cert.setExtensions([
    {
      name: 'basicConstraints',
      cA: true
    }
  ]);

  // Self-issued too
  cert.setIssuer(cert.subject.attributes);

  // Self-sign the certificate - we're the root
  cert.sign(keyPair.privateKey, md.sha256.create());

  return {
    key: pki.privateKeyToPem(keyPair.privateKey),
    cert: pki.certificateToPem(cert)
  };
};

const generateCerts = async (keyPath, certPath) => {
  const certKeyPair = await generateCACertificate();
  fs.writeFileSync(keyPath, certKeyPair.key);
  fs.writeFileSync(certPath, certKeyPair.cert);
  console.log(`Generated certs in ${keyPath} and ${certPath}`);
};

const generateCertsIfNotExists = async (keyPath, certPath) => {
  if (!fs.existsSync(keyPath) || !fs.existsSync(certPath)) {
    await generateCerts(keyPath, certPath);
  }
};

const getCertKeyPair = (keyPath, certPath) => {
  if (!fs.existsSync(keyPath) || !fs.existsSync(certPath)) {
    throw new Error(`The cert files do not exist!`);
  } else {
    const key = fs.readFileSync(keyPath, { encoding: 'utf8' });
    const cert = fs.readFileSync(certPath, { encoding: 'utf8' });

    return { key, cert };
  }
};

const getSPKIFingerprint = (keyPath, certPath) => {
  const certKeyPair = getCertKeyPair(keyPath, certPath);
  const cert = pki.certificateFromPem(certKeyPair.cert);

  return encode64(
    pki.getPublicKeyFingerprint(cert.publicKey, {
      type: 'SubjectPublicKeyInfo',
      md: md.sha256.create(),
      encoding: 'binary'
    })
  );
};

let KEY_PAIR;

class CA {
  constructor(keyPath,certPath,keyLength) {
    const caKey = fs.readFileSync(keyPath, {encoding: 'utf8'});
    const caCert = fs.readFileSync(certPath, {encoding: 'utf8'});

    this.caKey = pki.privateKeyFromPem(caKey);
    this.caCert = pki.certificateFromPem(caCert);
    this.certCache = {};

    if (!KEY_PAIR || KEY_PAIR.length < keyLength) {
      // If we have no key, or not a long enough one, generate one.
      KEY_PAIR = Object.assign(pki.rsa.generateKeyPair(keyLength), { length: keyLength });
    }
  }

  generateCertificate(domain) {
    if (this.certCache[domain]) return this.certCache[domain];

    let cert = pki.createCertificate();

    cert.publicKey = KEY_PAIR.publicKey;
    cert.serialNumber = uuid.v4().replace(/-/g, '');

    cert.validity.notBefore = new Date();
    // Make it valid for the last 24h - helps in cases where clocks slightly disagree.
    cert.validity.notBefore.setDate(cert.validity.notBefore.getDate() - 1);

    cert.validity.notAfter = new Date();
    // Valid for the next year by default. TODO: Shorten (and expire the cache) automatically.
    cert.validity.notAfter.setFullYear(cert.validity.notBefore.getFullYear() + 1);

    cert.setSubject([
      { name: 'commonName', value: domain },
      { name: 'organizationName', value: 'OneProxy Cert' }
    ]);
    cert.setIssuer(this.caCert.subject.attributes);

    cert.setExtensions([{
      name: 'keyUsage',
      keyCertSign: true,
      digitalSignature: true,
      nonRepudiation: true,
      keyEncipherment: true,
      dataEncipherment: true
    }, {
      name: 'subjectAltName',
      altNames: [{type: 2, value: domain}]
    }]);

    cert.sign(this.caKey, md.sha256.create());

    const generatedCertificate = {
      key: pki.privateKeyToPem(KEY_PAIR.privateKey),
      cert: pki.certificateToPem(cert),
      ca: pki.certificateToPem(this.caCert)
    };

    this.certCache[domain] = generatedCertificate;
    return generatedCertificate;
  }
}

module.exports = {
  CA,
  generateCACertificate,
  generateCertsIfNotExists,
  getSPKIFingerprint,
  getCertKeyPair
};
