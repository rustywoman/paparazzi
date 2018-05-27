declare function require(x: string): any;


// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
// Load Module - Raw Library
// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
(<any>window).hljs = require('lib/highlight.min.js');
(<any>window).Ps = require('lib/perfect-scrollbar.min.js');
(<any>window).axios = require('lib/axios.min.js');