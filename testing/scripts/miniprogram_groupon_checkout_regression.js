#!/usr/bin/env node
/* eslint-disable no-console */

const assert = require('assert');
const path = require('path');

const checkoutPagePath = path.resolve(__dirname, '../../hioshop-miniprogram/pages/order-check/index.js');
const utilPath = path.resolve(__dirname, '../../hioshop-miniprogram/utils/util.js');
const apiPath = path.resolve(__dirname, '../../hioshop-miniprogram/config/api.js');
const payPath = path.resolve(__dirname, '../../hioshop-miniprogram/services/pay.js');

const storage = {};
const toastMessages = [];
const requestCalls = [];

function resetRuntimeState() {
  Object.keys(storage).forEach((key) => delete storage[key]);
  toastMessages.length = 0;
  requestCalls.length = 0;
}

global.getApp = function () {
  return { globalData: {} };
};

global.wx = {
  getStorageSync(key) {
    return storage[key];
  },
  setStorageSync(key, value) {
    storage[key] = value;
  },
  removeStorageSync(key) {
    delete storage[key];
  },
  showToast(opts) {
    toastMessages.push((opts && opts.title) || '');
  },
  showLoading() {},
  hideLoading() {},
  showNavigationBarLoading() {},
  hideNavigationBarLoading() {},
  stopPullDownRefresh() {},
  navigateTo() {},
  redirectTo() {}
};

function loadPage(modulePath) {
  let pageDef = null;
  global.Page = function (def) {
    pageDef = def;
  };
  delete require.cache[modulePath];
  require(modulePath);
  assert(pageDef, 'failed to load page: ' + modulePath);
  return pageDef;
}

function createPageContext(pageDef) {
  const initialData = pageDef && pageDef.data ? JSON.parse(JSON.stringify(pageDef.data)) : {};
  return Object.assign({}, pageDef, {
    data: initialData,
    setData(next) {
      this.data = Object.assign({}, this.data, next || {});
    }
  });
}

async function testCheckoutAndSubmitSwitching() {
  resetRuntimeState();
  const util = require(utilPath);
  const api = require(apiPath);
  const pay = require(payPath);

  pay.payOrder = () => Promise.resolve({});
  util.showErrorToast = (msg) => toastMessages.push(msg || '');
  util.request = (url, data) => {
    requestCalls.push({ url, data });
    if (url === api.GrouponCheckout) {
      return Promise.resolve({
        errno: 0,
        data: {
          checkedGoodsList: [],
          checkedAddress: 0,
          actualPrice: 10,
          freightPrice: 0,
          couponPrice: 0,
          couponCandidates: [],
          selectedCoupons: [],
          goodsTotalPrice: 10,
          orderTotalPrice: 10,
          goodsCount: 1,
          outStock: 0
        }
      });
    }
    return Promise.resolve({ errno: 1, errmsg: 'mock fail' });
  };

  const page = loadPage(checkoutPagePath);
  const ctx = createPageContext(page);

  page.onLoad.call(ctx, {
    orderType: '2',
    grouponActivityId: '7001',
    teamId: '0',
    productId: '3001',
    number: '2'
  });

  assert.strictEqual(ctx.data.isGroupon, true, 'orderType=2 should enable groupon mode');
  assert.strictEqual(ctx.data.grouponActivityId, 7001, 'grouponActivityId should be parsed');

  await page.requestCheckout.call(ctx, 0);
  assert.strictEqual(requestCalls[0].url, api.GrouponCheckout, 'groupon checkout should call GrouponCheckout API');

  page.goSelectCoupon.call(ctx);
  assert(toastMessages.some((msg) => String(msg).includes('拼团订单不支持优惠券')), 'groupon coupon select should be blocked');

  ctx.ensureAddressBeforeSubmit = () => Promise.resolve(true);
  ctx.setData({
    addressId: 99,
    postscript: 'memo',
    freightPrice: 0,
    actualPrice: 9,
    selectedUserCouponIds: [1, 2]
  });

  await page.submitOrder.call(ctx);
  const submitCall = requestCalls.find((item) => item.url === api.GrouponSubmit);
  assert(submitCall, 'groupon submit should call GrouponSubmit API');
  assert.deepStrictEqual(submitCall.data.selectedUserCouponIds, [], 'groupon submit should not send selected coupons');
  assert.strictEqual(Number(submitCall.data.orderType), 2, 'groupon submit should send orderType=2');
}

async function main() {
  await testCheckoutAndSubmitSwitching();
  console.log('miniprogram groupon checkout regression passed');
}

main().catch((error) => {
  console.error('miniprogram groupon checkout regression failed:', error.message);
  process.exit(1);
});
