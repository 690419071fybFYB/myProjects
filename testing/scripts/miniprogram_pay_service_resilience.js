#!/usr/bin/env node
/* eslint-disable no-console */

const assert = require('assert');
const path = require('path');

const utilPath = path.resolve(__dirname, '../../hioshop-miniprogram/utils/util.js');
const payPath = path.resolve(__dirname, '../../hioshop-miniprogram/services/pay.js');

global.wx = global.wx || {};
global.wx.requestPayment = function () {
  throw new Error('wx.requestPayment is not initialized');
};

const util = require(utilPath);
delete require.cache[payPath];
const pay = require(payPath);

async function expectRejectedWithTimeout(factory, message) {
  const outcome = await Promise.race([
    factory().then(() => 'resolved').catch(() => 'rejected'),
    new Promise((resolve) => setTimeout(() => resolve('timeout'), 120))
  ]);
  assert.strictEqual(outcome, 'rejected', message);
}

async function testRequestRejectShouldNotHang() {
  util.request = function () {
    return Promise.reject(new Error('request failed'));
  };
  await expectRejectedWithTimeout(
    () => pay.payOrder(101),
    'payOrder should reject when prepay request fails'
  );
}

async function testBusinessErrnoReject() {
  util.request = function () {
    return Promise.resolve({ errno: 700, errmsg: 'prepay failed' });
  };
  await expectRejectedWithTimeout(
    () => pay.payOrder(102),
    'payOrder should reject when prepay errno is not 0'
  );
}

async function testWxPaymentFailReject() {
  util.request = function () {
    return Promise.resolve({
      errno: 0,
      data: {
        timeStamp: '1',
        nonceStr: 'abc',
        package: 'prepay',
        signType: 'MD5',
        paySign: 'sign'
      }
    });
  };
  global.wx.requestPayment = function (opts) {
    opts.fail({ errMsg: 'cancel' });
  };
  await expectRejectedWithTimeout(
    () => pay.payOrder(103),
    'payOrder should reject when wx.requestPayment fails'
  );
}

async function testWxPaymentSuccessResolve() {
  util.request = function () {
    return Promise.resolve({
      errno: 0,
      data: {
        timeStamp: '1',
        nonceStr: 'abc',
        package: 'prepay',
        signType: 'MD5',
        paySign: 'sign'
      }
    });
  };
  global.wx.requestPayment = function (opts) {
    opts.success({ ok: true });
  };
  const result = await pay.payOrder(104);
  assert.deepStrictEqual(result, { ok: true });
}

async function main() {
  await testRequestRejectShouldNotHang();
  await testBusinessErrnoReject();
  await testWxPaymentFailReject();
  await testWxPaymentSuccessResolve();
  console.log('miniprogram pay service resilience passed');
}

main().catch((err) => {
  console.error('miniprogram pay service resilience failed:', err.message || err);
  process.exit(1);
});
