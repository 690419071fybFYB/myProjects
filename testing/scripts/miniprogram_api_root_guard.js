#!/usr/bin/env node
/* eslint-disable no-console */

const assert = require('assert');
const path = require('path');

const apiModulePath = path.resolve(__dirname, '../../hioshop-miniprogram/config/api.js');

function loadApiFor(platform, storedOverride) {
  const storage = {};
  if (storedOverride) {
    storage.apiRootOverride = storedOverride;
  }
  global.wx = {
    getSystemInfoSync() {
      return { platform };
    },
    getStorageSync(key) {
      return storage[key] || '';
    },
    setStorageSync(key, value) {
      storage[key] = value;
    },
    removeStorageSync(key) {
      delete storage[key];
    }
  };
  delete require.cache[apiModulePath];
  return require(apiModulePath);
}

function main() {
  const deviceApi = loadApiFor('ios', 'https://evil.example.com');
  assert.strictEqual(deviceApi.canUseApiRootOverride(), false);
  assert.strictEqual(
    deviceApi.resolveApiRoot('https://evil.example.com'),
    deviceApi.runtime.defaultDeviceApiRoot
  );
  assert.strictEqual(
    deviceApi.resolveApiRoot('https://api.fybshop.site'),
    deviceApi.runtime.defaultDeviceApiRoot
  );

  const devApi = loadApiFor('devtools', 'https://evil.example.com');
  assert.strictEqual(devApi.canUseApiRootOverride(), true);
  assert.strictEqual(devApi.isAllowedOverrideRoot('https://api.fybshop.site'), true);
  assert.strictEqual(devApi.isAllowedOverrideRoot('http://127.0.0.1:8360'), true);
  assert.strictEqual(devApi.isAllowedOverrideRoot('https://evil.example.com'), false);
  assert.strictEqual(
    devApi.resolveApiRoot('https://evil.example.com'),
    devApi.runtime.defaultDevtoolsApiRoot
  );
  assert.strictEqual(devApi.resolveApiRoot('http://127.0.0.1:9000'), 'http://127.0.0.1:9000');
  assert.strictEqual(devApi.resolveApiRoot('https://api.fybshop.site'), 'https://api.fybshop.site');

  const devStoredApi = loadApiFor('devtools', 'https://api.fybshop.site');
  assert.strictEqual(devStoredApi.resolveApiRoot(''), 'https://api.fybshop.site');

  console.log('miniprogram api root guard passed');
}

main();
