#!/usr/bin/env node
/* eslint-disable no-console */

const assert = require('assert');

const storage = {};
const callState = {
  loginCalls: 0,
  refreshCalls: 0,
  requestA: 0,
  requestB: 0
};

global.getCurrentPages = () => [{ route: 'pages/index/index' }];

global.wx = {
  getSystemInfoSync() {
    return { platform: 'devtools' };
  },
  getStorageSync(key) {
    return storage[key];
  },
  setStorageSync(key, value) {
    storage[key] = value;
  },
  removeStorageSync(key) {
    delete storage[key];
  },
  login({ success }) {
    callState.loginCalls += 1;
    success({ code: 'single-flight-code' });
  },
  request() {
    throw new Error('wx.request is not initialized');
  },
  showToast() {},
  switchTab() {}
};

function ok(data, delayMs) {
  return {
    delayMs: delayMs || 0,
    payload: {
      statusCode: 200,
      data
    }
  };
}

async function main() {
  const api = require('../../hioshop-miniprogram/config/api.js');
  const requestSdk = require('../../hioshop-miniprogram/utils/request/index.js');
  const authUrl = api.AuthLoginByWeixin;

  global.wx.request = function request(opts) {
    const url = String(opts.url || '');
    if (url === authUrl) {
      callState.refreshCalls += 1;
      const refreshResponse = ok({
        errno: 0,
        data: {
          token: 'fresh-token',
          userInfo: { id: 1001 }
        }
      }, 15);
      return setTimeout(function () {
        opts.success(refreshResponse.payload);
      }, refreshResponse.delayMs);
    }

    if (url === 'http://example.com/resource-a') {
      callState.requestA += 1;
      if (callState.requestA === 1) {
        return opts.success(ok({ errno: 401, errmsg: 'expired' }).payload);
      }
      return opts.success(ok({ errno: 0, data: { key: 'A' } }).payload);
    }

    if (url === 'http://example.com/resource-b') {
      callState.requestB += 1;
      if (callState.requestB === 1) {
        return opts.success(ok({ errno: 401, errmsg: 'expired' }).payload);
      }
      return opts.success(ok({ errno: 0, data: { key: 'B' } }).payload);
    }

    return opts.fail({ errMsg: 'request:fail unexpected url ' + url });
  };

  const pair = await Promise.all([
    requestSdk.request('http://example.com/resource-a', {}, 'GET', { skipAuthRefresh: false }),
    requestSdk.request('http://example.com/resource-b', {}, 'GET', { skipAuthRefresh: false })
  ]);

  assert.strictEqual(pair[0].errno, 0);
  assert.strictEqual(pair[1].errno, 0);
  assert.strictEqual(callState.loginCalls, 1, 'wx.login should be called once');
  assert.strictEqual(callState.refreshCalls, 1, 'token refresh request should be single-flight');
  assert.strictEqual(storage.token, 'fresh-token');

  console.log('miniprogram auth refresh race passed');
}

main().catch((err) => {
  console.error('miniprogram auth refresh race failed:', err.message || err);
  process.exit(1);
});
