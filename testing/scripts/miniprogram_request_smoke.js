#!/usr/bin/env node
/* eslint-disable no-console */

const assert = require('assert');

const queue = [];
const storage = {};

function pushResponse(kind, payload) {
  queue.push({ kind, payload });
}

function nextResponse() {
  if (!queue.length) {
    throw new Error('No queued wx.request response');
  }
  return queue.shift();
}

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
    success({ code: 'mock-code' });
  },
  request(opts) {
    const item = nextResponse();
    if (item.kind === 'success') {
      opts.success(item.payload);
      return;
    }
    opts.fail(item.payload);
  },
  showToast() {},
  switchTab() {},
};

async function main() {
  const requestSdk = require('../../hioshop-miniprogram/utils/request/index.js');

  // success path
  pushResponse('success', { statusCode: 200, data: { errno: 0, data: { ok: true } } });
  const ok = await requestSdk.request('http://example.com/ok', {}, 'GET', {});
  assert.strictEqual(ok.errno, 0);

  // profile gate path
  pushResponse('success', { statusCode: 200, data: { errno: 412, errmsg: 'profile incomplete' } });
  let profileError = null;
  try {
    await requestSdk.request('http://example.com/profile', {}, 'GET', { skipProfileGuard: false });
  } catch (err) {
    profileError = err;
  }
  assert(profileError && profileError.code === 'PROFILE_INCOMPLETE');

  // unauthorized path with refresh attempt failed
  pushResponse('success', { statusCode: 200, data: { errno: 401, errmsg: 'unauthorized' } });
  pushResponse('success', { statusCode: 200, data: { errno: 401, errmsg: 'refresh failed' } });
  let unauthorized = null;
  try {
    await requestSdk.request('http://example.com/auth', {}, 'GET', { skipAuthRefresh: false });
  } catch (err) {
    unauthorized = err;
  }
  assert(unauthorized && unauthorized.code === 'UNAUTHORIZED');

  // network fail path
  pushResponse('fail', { errMsg: 'request:fail timeout' });
  let networkErr = null;
  try {
    await requestSdk.request('http://example.com/network', {}, 'GET', { retry: 0 });
  } catch (err) {
    networkErr = err;
  }
  assert(networkErr && (networkErr.code === 'TIMEOUT' || networkErr.code === 'NETWORK_FAIL'));

  console.log('miniprogram request smoke passed');
}

main().catch((err) => {
  console.error('miniprogram request smoke failed:', err.message || err);
  process.exit(1);
});
