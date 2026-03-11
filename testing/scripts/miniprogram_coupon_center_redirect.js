#!/usr/bin/env node
/* eslint-disable no-console */

const assert = require('assert');
const path = require('path');

const redirectPagePath = path.resolve(__dirname, '../../hioshop-miniprogram/pages/coupon-center/index.js');

let pageDef = null;
const redirectUrls = [];

global.Page = function (def) {
  pageDef = def;
};

global.wx = {
  redirectTo({ url }) {
    redirectUrls.push(url);
  }
};

delete require.cache[redirectPagePath];
require(redirectPagePath);

assert(pageDef && typeof pageDef.onLoad === 'function', 'coupon-center redirect page should expose onLoad');
pageDef.onLoad.call({});

assert.strictEqual(
  redirectUrls[0],
  '/pages/ucenter/coupon/index?tab=claimable&skin=promo',
  'legacy coupon-center route should redirect to unified claimable tab'
);

console.log('miniprogram coupon-center redirect passed');
