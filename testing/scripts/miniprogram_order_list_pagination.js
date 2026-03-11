#!/usr/bin/env node
/* eslint-disable no-console */

const assert = require('assert');
const path = require('path');

const pagePath = path.resolve(__dirname, '../../hioshop-miniprogram/pages/ucenter/order-list/index.js');
const utilPath = path.resolve(__dirname, '../../hioshop-miniprogram/utils/util.js');
const apiPath = path.resolve(__dirname, '../../hioshop-miniprogram/config/api.js');

let pageDef = null;
const storage = {};

global.getApp = function () {
  return {};
};

global.Page = function (def) {
  pageDef = def;
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
  navigateTo() {},
  switchTab() {},
  showToast() {},
  showModal() {}
};

delete require.cache[pagePath];
require(pagePath);

const util = require(utilPath);
const api = require(apiPath);

function createContext() {
  return Object.assign({}, pageDef, {
    data: JSON.parse(JSON.stringify(pageDef.data)),
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

async function testOrderListPaginationStopsAtLastPage() {
  const orderListCalls = [];
  util.request = function (url, data) {
    if (url === api.OrderList) {
      orderListCalls.push({ url, data });
      const page = Number(data.page || 1);
      if (page === 1) {
        return Promise.resolve({
          errno: 0,
          data: {
            count: 9,
            currentPage: 1,
            data: [1, 2, 3, 4, 5, 6, 7, 8].map((id) => ({ id }))
          }
        });
      }
      if (page === 2) {
        return Promise.resolve({
          errno: 0,
          data: {
            count: 9,
            currentPage: 2,
            data: [{ id: 9 }]
          }
        });
      }
      return Promise.resolve({
        errno: 0,
        data: {
          count: 9,
          currentPage: page,
          data: []
        }
      });
    }
    if (url === api.OrderCountInfo) {
      return Promise.resolve({ errno: 0, data: {} });
    }
    return Promise.reject(new Error('unexpected request url: ' + url));
  };

  const ctx = createContext();
  await pageDef.getOrderList.call(ctx);
  assert.strictEqual(orderListCalls.length, 1, 'first page should be requested once');
  assert.strictEqual(orderListCalls[0].data.page, 1);
  assert.strictEqual(ctx.data.orderList.length, 8);
  assert.strictEqual(ctx.data.hasMore, true);

  pageDef.onReachBottom.call(ctx);
  await flushAsyncTwice();
  assert.strictEqual(orderListCalls.length, 2, 'second page should be requested on reach bottom');
  assert.strictEqual(orderListCalls[1].data.page, 2);
  assert.strictEqual(ctx.data.orderList.length, 9);
  assert.strictEqual(ctx.data.hasMore, false, 'should stop loading after last page');
  assert.strictEqual(ctx.data.showTips, 1, 'should show end-of-list tip at last page');

  pageDef.onReachBottom.call(ctx);
  await flushAsyncTwice();
  assert.strictEqual(orderListCalls.length, 2, 'no extra request after hasMore=false');
}

async function testOrderListLoadingGuardPreventsDuplicateRequests() {
  let resolveFirst = null;
  let orderListCallCount = 0;
  util.request = function (url) {
    if (url === api.OrderList) {
      orderListCallCount += 1;
      return new Promise((resolve) => {
        resolveFirst = resolve;
      });
    }
    if (url === api.OrderCountInfo) {
      return Promise.resolve({ errno: 0, data: {} });
    }
    return Promise.reject(new Error('unexpected request url: ' + url));
  };

  const ctx = createContext();
  const firstPromise = pageDef.getOrderList.call(ctx);
  const secondResult = await pageDef.getOrderList.call(ctx);
  assert.strictEqual(orderListCallCount, 1, 'loading guard should block duplicate in-flight requests');
  assert.strictEqual(secondResult, false, 'second getOrderList call should short-circuit while loading');

  resolveFirst({
    errno: 0,
    data: {
      count: 0,
      currentPage: 1,
      data: []
    }
  });
  await firstPromise;
  assert.strictEqual(ctx.data.loading, false, 'loading flag should be cleared after request finished');
}

async function main() {
  assert(pageDef && typeof pageDef.getOrderList === 'function', 'order-list page should be loaded');
  await testOrderListPaginationStopsAtLastPage();
  await testOrderListLoadingGuardPreventsDuplicateRequests();
  console.log('miniprogram order list pagination passed');
}

main().catch((err) => {
  console.error('miniprogram order list pagination failed:', err.message || err);
  process.exit(1);
});
