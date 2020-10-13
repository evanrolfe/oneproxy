const DEFAULT_FILTERS = {
  hostList: [],
  hostSetting: '',
  pathList: [],
  pathSetting: '',
  extList: [],
  extSetting: '',
  navigationRequests: true
};

const PORTS_AVAILABLE = {
  proxy: [8080, 8081, 8082, 8083, 8084, 8085, 8086, 8087, 8088, 8089, 8090],
  browser: [9222, 9223, 9224, 9225, 9226, 9227, 9228, 9229, 9230, 9231, 9232]
};

module.exports = {
  DEFAULT_FILTERS,
  PORTS_AVAILABLE
};
