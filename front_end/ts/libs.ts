/**
 * @author      rustywoman
 * @description Custom Declarration
 * @type        {any}
 */
declare function require(x: string): any;


// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
// Load Module - Raw Library
// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
/**
 * @author      rustywoman
 * @description Window Library - [ hljs ]
 * @type        {any}
 */
(<any>window).hljs = require('lib/highlight.min.js');
/**
 * @author      rustywoman
 * @description Window Library - [ Ps ]
 * @type        {any}
 */
(<any>window).Ps = require('lib/perfect-scrollbar.min.js');
/**
 * @author      rustywoman
 * @description Window Library - [ axios ]
 * @type        {any}
 */
(<any>window).axios = require('lib/axios.min.js');
/**
 * @author      rustywoman
 * @description Window Library - [ d3 ]
 * @type        {any}
 */
(<any>window).d3 = require('lib/d3.v3.min.js');