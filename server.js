'use strict';


// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
// Config
// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
const CONFIG = require('./webpack.common.config');
const WEBPACK_CUSTOM_CONFIG = require('./webpack.config');


// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
// Load Module
// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
const express = require('express');
const cookieParser = require('cookie-parser');
const bodyParser = require('body-parser');
const session = require('express-session');
const webpack = require('webpack');
const webpackDevMiddleware = require('webpack-dev-middleware');
const webpackHotMiddleware = require('webpack-hot-middleware');


// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
// Variables
// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
const WEBPACK_COMPILER = webpack(WEBPACK_CUSTOM_CONFIG);
const APP = express();


// ++++++++++++++++++++++++++++++++++++++++++++++++
// Router
// ++++++++++++++++++++++++++++++++++++++++++++++++
const MAIN = require('./back_end/js/router/Main');


// ------------------------------------------------
// Webpack Hot Loread
// ------------------------------------------------
APP.use(
  webpackDevMiddleware(
    WEBPACK_COMPILER,
    {
      noInfo     : true,
      publicPath : '/'
    }
  )
);
APP.use(webpackHotMiddleware(WEBPACK_COMPILER));


// ------------------------------------------------
// Default Cookie Parser
// ------------------------------------------------
APP.use(cookieParser());


// ------------------------------------------------
// Default Body Parser
// ------------------------------------------------
APP.use(
  bodyParser.urlencoded(
    {
      extended : true
    }
  )
);
APP.use(bodyParser.json());


// ------------------------------------------------
// Default Document Root for Static
// ------------------------------------------------
APP.use(express.static('report'));


// ------------------------------------------------
// Default Document Root for Template
// ------------------------------------------------
APP.set(
  'view engine',
  'ejs'
);
APP.set(
  'views',
  __dirname + '/front_end/ejs'
);


// ------------------------------------------------
// Default Session Information
// ------------------------------------------------
APP.use(
  session(
    {
      secret            : 'PAPARAZZI_WEB_PAGE',
      resave            : false,
      saveUninitialized : false,
      cookie            : {
        maxAge : 30 * 60 * 1000
      }
    }
  )
);


// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
// Router - Common
// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
new MAIN(APP).render();


// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
// Main
// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
const server = APP.listen(
  CONFIG.PROXY_PORT,
  () => {
    console.log('Local Server is listening port [ ' + server.address().port + ' ]');
  }
);