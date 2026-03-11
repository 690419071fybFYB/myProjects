#!/usr/bin/env node
/* eslint-disable no-console */

const assert = require('assert');
const path = require('path');

const orderCheckPath = path.resolve(__dirname, '../../hioshop-miniprogram/pages/order-check/index.js');
const utilPath = path.resolve(__dirname, '../../hioshop-miniprogram/utils/util.js');
const payPath = path.resolve(__dirname, '../../hioshop-miniprogram/services/pay.js');
const apiPath = path.resolve(__dirname, '../../hioshop-miniprogram/config/api.js');
const ADDRESS_PICKED_ONCE_KEY = 'checkoutAddressPickedOnce';

let pageDef = null;
const storage = {};
const state = {
  showLoadingCalls: 0,
  hideLoadingCalls: 0,
  redirects: [],
  toasts: []
};

global.getApp = function () {
  return {};
};

global.Page = function (def) {
  pageDef = def;
};

global.wx = {
  showLoading() {
    state.showLoadingCalls += 1;
  },
  hideLoading() {
    state.hideLoadingCalls += 1;
  },
  redirectTo({ url }) {
    state.redirects.push(url);
  },
  removeStorageSync(key) {
    delete storage[key];
  },
  setStorageSync(key, value) {
    storage[key] = value;
  },
  navigateTo() {},
  getStorageSync(key) {
    return storage[key];
  },
  showToast() {}
};

delete require.cache[orderCheckPath];
require(orderCheckPath);

const util = require(utilPath);
const pay = require(payPath);
const api = require(apiPath);

function resetState() {
  state.showLoadingCalls = 0;
  state.hideLoadingCalls = 0;
  state.redirects = [];
  state.toasts = [];
  Object.keys(storage).forEach((key) => {
    delete storage[key];
  });
}

function createPageContext() {
  return Object.assign({}, pageDef, {
    data: {
      addressId: 1001,
      postscript: '',
      freightPrice: 0,
      actualPrice: 9.9,
      selectedUserCouponIds: []
    },
    setData(next) {
      this.data = Object.assign({}, this.data, next || {});
    }
  });
}

function flushAsync() {
  return new Promise((resolve) => setTimeout(resolve, 0));
}

async function flushAsyncTwice() {
  await flushAsync();
  await flushAsync();
}

function createCheckoutPayload(addressId) {
  return {
    checkedGoodsList: [],
    checkedAddress: addressId > 0 ? { id: addressId } : 0,
    actualPrice: 9.9,
    freightPrice: 0,
    couponPrice: 0,
    couponCandidates: [],
    selectedCoupons: [],
    goodsOriginalPrice: 9.9,
    promotionPrice: 0,
    goodsTotalPrice: 9.9,
    orderTotalPrice: 9.9,
    goodsCount: 1,
    outStock: 0
  };
}

async function testSubmitOrderRejectShouldHideLoading() {
  resetState();
  util.request = function () {
    return Promise.reject({ message: 'network down' });
  };
  util.showErrorToast = function (msg) {
    state.toasts.push(msg);
  };
  pay.payOrder = function () {
    return Promise.resolve();
  };
  const ctx = createPageContext();
  await pageDef.submitOrder.call(ctx);
  assert.strictEqual(state.showLoadingCalls, 1, 'submitOrder should show loading once');
  assert.strictEqual(state.hideLoadingCalls, 1, 'submitOrder should always hide loading');
  assert.ok(state.toasts.includes('network down'), 'submitOrder should surface request error');
}

async function testOfflineOrderRejectShouldHideLoadingAndRedirect() {
  resetState();
  util.request = function () {
    return Promise.reject({ message: 'offline network down' });
  };
  util.showErrorToast = function (msg) {
    state.toasts.push(msg);
  };
  const ctx = createPageContext();
  await pageDef.offlineOrder.call(ctx);
  assert.strictEqual(state.showLoadingCalls, 1, 'offlineOrder should show loading once');
  assert.strictEqual(state.hideLoadingCalls, 1, 'offlineOrder should always hide loading');
  assert.ok(state.toasts.includes('offline network down'), 'offlineOrder should surface request error');
  assert.strictEqual(
    state.redirects[state.redirects.length - 1],
    '/pages/payOffline/index?status=0',
    'offlineOrder should redirect to failed page on request failure'
  );
}

async function testSubmitOrderShouldLoadDefaultAddressWhenAddressMissing() {
  resetState();
  const calls = [];
  util.request = function (url, data) {
    calls.push({ url, data });
    if (url === api.CartCheckout) {
      return Promise.resolve({
        errno: 0,
        data: createCheckoutPayload(3003)
      });
    }
    if (url === api.OrderSubmit) {
      return Promise.resolve({
        errno: 0,
        data: {
          orderInfo: { id: 9001 }
        }
      });
    }
    return Promise.reject(new Error('unexpected request url'));
  };
  util.showErrorToast = function (msg) {
    state.toasts.push(msg);
  };
  pay.payOrder = function () {
    return Promise.resolve({ ok: true });
  };
  const ctx = createPageContext();
  ctx.data.addressId = 0;
  await pageDef.submitOrder.call(ctx);
  await flushAsync();

  assert.strictEqual(calls.length, 2, 'submitOrder should call checkout then submit when address missing');
  assert.strictEqual(calls[0].url, api.CartCheckout);
  assert.strictEqual(calls[1].url, api.OrderSubmit);
  assert.strictEqual(calls[1].data.addressId, 3003, 'submit should use default address from checkout');
  assert.strictEqual(state.showLoadingCalls, 1, 'submitOrder should still show loading');
  assert.strictEqual(state.hideLoadingCalls, 1, 'submitOrder should hide loading');
  assert.strictEqual(
    state.redirects[state.redirects.length - 1],
    '/pages/payResult/payResult?status=1&orderId=9001',
    'submitOrder should continue to success payment flow'
  );
}

async function testSubmitOrderWithoutAnyAddressShouldStopBeforeLoading() {
  resetState();
  const calls = [];
  util.request = function (url) {
    calls.push(url);
    if (url === api.CartCheckout) {
      return Promise.resolve({
        errno: 0,
        data: createCheckoutPayload(0)
      });
    }
    return Promise.reject(new Error('unexpected submit request'));
  };
  util.showErrorToast = function (msg) {
    state.toasts.push(msg);
  };
  pay.payOrder = function () {
    return Promise.resolve({ ok: true });
  };
  const ctx = createPageContext();
  ctx.data.addressId = 0;
  await pageDef.submitOrder.call(ctx);

  assert.deepStrictEqual(calls, [api.CartCheckout], 'should only request checkout when no address selected');
  assert.strictEqual(state.showLoadingCalls, 0, 'should not show loading when address still missing');
  assert.strictEqual(state.hideLoadingCalls, 0, 'should not hide loading when loading never shown');
  assert.ok(state.toasts.includes('请选择收货地址'));
}

async function testOnShowShouldPreferServerDefaultAddressOverStaleStorage() {
  resetState();
  storage.addressId = 8888;
  const calls = [];
  util.request = function (url, data) {
    calls.push({ url, data });
    if (url === api.CartCheckout) {
      return Promise.resolve({
        errno: 0,
        data: createCheckoutPayload(2002)
      });
    }
    return Promise.reject(new Error('unexpected request url'));
  };
  util.showErrorToast = function () {};
  const ctx = createPageContext();

  pageDef.onShow.call(ctx);
  await flushAsyncTwice();

  assert.strictEqual(calls.length, 1, 'onShow should request checkout once');
  assert.strictEqual(calls[0].url, api.CartCheckout);
  assert.strictEqual(
    calls[0].data.addressId,
    0,
    'onShow should not trust stale storage address without manual-selection marker'
  );
  assert.strictEqual(ctx.data.addressId, 2002, 'onShow should use default address returned by checkout');
}

async function testOnShowShouldUsePickedAddressOnce() {
  resetState();
  storage.addressId = 7777;
  storage[ADDRESS_PICKED_ONCE_KEY] = 1;
  const calls = [];
  util.request = function (url, data) {
    calls.push({ url, data });
    if (url === api.CartCheckout) {
      return Promise.resolve({
        errno: 0,
        data: createCheckoutPayload(7777)
      });
    }
    return Promise.reject(new Error('unexpected request url'));
  };
  util.showErrorToast = function () {};
  const ctx = createPageContext();

  pageDef.onShow.call(ctx);
  await flushAsyncTwice();

  assert.strictEqual(calls.length, 1);
  assert.strictEqual(calls[0].data.addressId, 7777, 'picked address should be used once on return from selector');
  assert.strictEqual(
    storage[ADDRESS_PICKED_ONCE_KEY],
    undefined,
    'manual-selection marker should be consumed after onShow'
  );
}

async function main() {
  assert(pageDef && typeof pageDef.submitOrder === 'function', 'order-check page should be loaded');
  await testSubmitOrderRejectShouldHideLoading();
  await testOfflineOrderRejectShouldHideLoadingAndRedirect();
  await testSubmitOrderShouldLoadDefaultAddressWhenAddressMissing();
  await testSubmitOrderWithoutAnyAddressShouldStopBeforeLoading();
  await testOnShowShouldPreferServerDefaultAddressOverStaleStorage();
  await testOnShowShouldUsePickedAddressOnce();
  console.log('miniprogram checkout resilience passed');
}

main().catch((err) => {
  console.error('miniprogram checkout resilience failed:', err.message || err);
  process.exit(1);
});
