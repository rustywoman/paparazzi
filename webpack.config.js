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
const glob             = require('glob');
const path             = require('path');


// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
// Export
// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
module.exports = {
  entry : (function(){
    let entries = {}
    glob.sync(CONFIG.DEV_ROOT + CONFIG.PATH.ts + '*.ts').map(function(file){
      entries[path.basename(file).replace('.ts', '')] = file;
    });
    return entries;
  })(),
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
      }
    ]
  },
  devtool : 'inline-source-map',
  plugins : [
    new LiveReloadPlugin(),
    new webpack.HotModuleReplacementPlugin()
  ],
  devServer : {
    hot         : true,
    inline      : true,
    contentBase : CONFIG.ROOT,
    host        : CONFIG.DEV_IP,
    port        : CONFIG.BROWSER_SYNC_PORT
  },
  watchOptions : {
    aggregateTimeout : CONFIG.BUILD_INTERVAL,
    poll             : CONFIG.BUILD_INTERVAL,
    ignored          : /node_modules/
  }
};