'use strict';


// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
// Config
// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
const CONFIG = require('./webpack.common.config');


// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
// Load Module
// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
const LiveReloadPlugin = require('webpack-livereload-plugin');
const webpack          = require('webpack');
const path             = require('path');


// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
// Export
// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
module.exports = {
  entry : {
    'paparazzi-main-script' : [
      'webpack-hot-middleware/client',
      './front_end/ts/main.ts',
      './front_end/scss/main.scss'
    ],
    'paparazzi-libs-style' : [
      './front_end/scss/libs.scss'
    ],
    'paparazzi-libs-script' : [
      './front_end/ts/libs.ts'
    ]
  },
  output : {
    path     : CONFIG.ROOT + CONFIG.CONTENTS_SUB_ROOT + CONFIG.PATH.js,
    filename : '[name].js'
  },
  resolve : {
    modules: [
      CONFIG.DEV_ROOT + CONFIG.PATH.ts,
      'node_modules'
    ],
    extensions : ['.ts', '.js']
  },
  module : {
    rules : [
      {
        test : /\.ts$/,
        use  : 'ts-loader'
      },
      {
        test    : /\.scss$/,
        loaders : ['style-loader', 'css-loader', 'sass-loader']
      }
    ]
  },
  devtool : 'inline-source-map',
  plugins : [
    new LiveReloadPlugin(
      {
        port : CONFIG.SYNC_PORT
      }
    ),
    new webpack.HotModuleReplacementPlugin()
  ],
  devServer : {
    contentBase : CONFIG.ROOT
  },
  watchOptions : {
    aggregateTimeout : CONFIG.BUILD_INTERVAL,
    poll             : CONFIG.BUILD_INTERVAL,
    ignored          : /node_modules/
  }
};