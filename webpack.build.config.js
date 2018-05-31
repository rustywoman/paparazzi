'use strict';


// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
// Config
// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
const CONFIG = require('./webpack.common.config');


// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
// Load Module
// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
const ExtractTextPlugin = require('extract-text-webpack-plugin');
const path              = require('path');
const webpack           = require('webpack');


// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
// Task - Webpack - Build.
// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
module.exports = [
  {
    entry : {
      'paparazzi-script' : [
        './front_end/ts/libs.ts',
        './front_end/ts/main.ts'
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
        }
      ]
    },
    plugins : [
      new webpack.optimize.UglifyJsPlugin(
        {
          compress : {
            warnings     : false,
            drop_console : true
          },
          minimize : true
        }
      ),
      new webpack.BannerPlugin(CONFIG.BANNER)
    ]
  },
  {
    entry : {
      'paparazzi-style' : [
        './front_end/scss/libs.scss',
        './front_end/scss/main.scss'
      ]
    },
    resolve : {
      modules : [
        CONFIG.DEV_ROOT + CONFIG.PATH.scss,
        'node_modules'
      ],
      extensions : ['.js', '.scss']
    },
    output : {
      path     : CONFIG.ROOT + CONFIG.CONTENTS_SUB_ROOT + CONFIG.PATH.css + CONFIG.PATH.chunk,
      filename : '[name].css'
    },
    module : {
      rules : [
        {
          test : /\.scss$/,
          use  : ExtractTextPlugin.extract(
            {
              fallback : 'style-loader',
              use      : ['css-loader?minimize', 'sass-loader']
            }
          )
        }
      ]
    },
    plugins : [
      new webpack.BannerPlugin(CONFIG.BANNER),
      new ExtractTextPlugin('../[name].css')
    ]
  }
];