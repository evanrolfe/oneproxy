const RequestResponsePair = require('../../../../shared/models/request-response-pair');
const Request = require('../../../../shared/models/request');

describe('RequestResponsePair', () => {
  let reqResPair;

  beforeEach(() => {
    reqResPair = new RequestResponsePair()
    reqResPair.isEncrypted = false;
    reqResPair.request = new Request({
      method: 'GET',
      url: 'http://localhost:3000/',
      host: 'localhost',
      port: 3000,
      httpVersion: '1.1',
      path: '/',
      headers: {
        host: 'localhost:3000',
        'user-agent': 'curl/7.58.0',
        accept: '*/*'
      }
    });
  });

  describe('#addModifiedRequest', () => {
    it('parses the raw request and update the request object', () => {
      rawRequest = `GET /api/posts.json HTTP/1.2
host: localhost:3000
user-agent: curl/1.2.3
accept: */*
`;

      reqResPair.addModifiedRequest(rawRequest);

      expect(reqResPair.requestModified()).to.eql(true);
      expect(reqResPair.modifiedRequest.url).to.eql('http://localhost:3000/api/posts.json');
      expect(reqResPair.modifiedRequest.host).to.eql('localhost:3000');
      expect(reqResPair.modifiedRequest.httpVersion).to.eql('1.2');
      expect(reqResPair.modifiedRequest.path).to.eql('/api/posts.json');
      expect(reqResPair.modifiedRequest.ext).to.eql('json');
      expect(reqResPair.modifiedRequest.headers).to.eql({ host: 'localhost:3000', 'user-agent': 'curl/1.2.3', accept: '*/*' })
    });
  });
});
