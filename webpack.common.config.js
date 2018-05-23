'use strict';


// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
// Load Module
// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
const os            = require('os');
const path          = require('path');


// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
// Variables
// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
const BASE_DIR    = __dirname;
const BASE_DEV_IP = 'localhost';
const BANNER      = [
  'Paparazzi Report',
  ''
].join('\n');


// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
// Export
// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
module.exports = {
  DEV_IP            : BASE_DEV_IP,
  DOMAIN            : 'http://' + BASE_DEV_IP,
  ROW_PORT          : 80,
  BROWSER_SYNC_PORT : 8088,
  BUILD_INTERVAL    : 500,
  ROOT              : BASE_DIR + path.sep + 'report' + path.sep,
  DEV_ROOT          : BASE_DIR + path.sep + 'front_end' + path.sep,
  CONTENTS_SUB_ROOT : 'assets' + path.sep,
  PATH              : {
    ts   : 'ts' + path.sep,
    js   : 'js' + path.sep,
    css  : 'css' + path.sep,
    scss : 'style' + path.sep
  },
  BANNER            : BANNER
};