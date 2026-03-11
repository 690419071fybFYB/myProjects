#!/usr/bin/env node
/* eslint-disable no-console */

const assert = require('assert');
const path = require('path');

const couponPagePath = path.resolve(__dirname, '../../hioshop-miniprogram/pages/ucenter/coupon/index.js');
const homePagePath = path.resolve(__dirname, '../../hioshop-miniprogram/pages/index/index.js');
const ucenterPagePath = path.resolve(__dirname, '../../hioshop-miniprogram/pages/ucenter/index/index.js');
const utilPath = path.resolve(__dirname, '../../hioshop-miniprogram/utils/util.js');
const apiPath = path.resolve(__dirname, '../../hioshop-miniprogram/config/api.js');

const storage = {};
const navUrls = [];
const switchTabUrls = [];
const redirectUrls = [];

global.getApp = function () {
  return { globalData: {} };
};

global.getCurrentPages = function () {
  return [];
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
  navigateTo({ url }) {
    navUrls.push(url);
  },
  switchTab({ url }) {
    switchTabUrls.push(url);
  },
  redirectTo({ url }) {
    redirectUrls.push(url);
  },
  showToast() {},
  showLoading() {},
  hideLoading() {},
  showModal() {}
};

function loadPage(modulePath) {
  let pageDef = null;
  global.Page = function (def) {
    pageDef = def;
  };
  delete require.cache[modulePath];
  require(modulePath);
  assert(pageDef, `failed to load page: ${modulePath}`);
  return pageDef;
}

const util = require(utilPath);
const api = require(apiPath);

function createPageContext(pageDef) {
  const initialData = pageDef && pageDef.data ? JSON.parse(JSON.stringify(pageDef.data)) : {};
  return Object.assign({}, pageDef, {
    data: initialData,
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

function resetRuntimeState() {
  Object.keys(storage).forEach((key) => {
    delete storage[key];
  });
  navUrls.length = 0;
  switchTabUrls.length = 0;
  redirectUrls.length = 0;
}

function createClaimableSample(overrides = {}) {
  return Object.assign({
    id: 101,
    name: 'auto-full',
    type: 'full_reduction',
    threshold_amount: '100',
    reduce_amount: '20',
    discount_rate: '9',
    discount_max_reduce: '50',
    use_start_at: 1773232776,
    use_end_at: 1773632776,
    has_received: 0
  }, overrides);
}

function createMyCouponSample(overrides = {}) {
  return Object.assign({
    user_coupon_id: 201,
    name: 'my-coupon',
    type: 'full_reduction',
    threshold_amount: '100',
    reduce_amount: '20',
    discount_rate: '9',
    discount_max_reduce: '50',
    claim_time: 1773232776,
    used_time: 1773332776,
    expire_time: 1773832776
  }, overrides);
}

function testSkinThemeMapping() {
  resetRuntimeState();
  const couponPage = loadPage(couponPagePath);
  const ctx = createPageContext(couponPage);

  couponPage.onLoad.call(ctx, {});
  assert.strictEqual(ctx.data.skin, 'premium', 'default skin should be premium');
  assert.strictEqual(ctx.data.skinThemeClass, '', 'premium skin should not inject promo class');

  couponPage.onLoad.call(ctx, { skin: 'promo', tab: 'claimable' });
  assert.strictEqual(ctx.data.skin, 'promo', 'skin query should activate promo skin');
  assert.strictEqual(ctx.data.skinThemeClass, 'coupon-theme--promo', 'promo skin should inject promo class');

  couponPage.onLoad.call(ctx, { theme: 'promo', status: 'used' });
  assert.strictEqual(ctx.data.skin, 'promo', 'theme alias should also activate promo skin');

  couponPage.onLoad.call(ctx, { skin: 'unknown' });
  assert.strictEqual(ctx.data.skin, 'premium', 'invalid skin should fallback to premium');
}

async function testApiSelectionByQueryTabAndLegacyStatus() {
  resetRuntimeState();
  const couponPage = loadPage(couponPagePath);
  const requestCalls = [];

  util.request = function (url, data) {
    requestCalls.push({ url, data });
    if (url === api.CouponCenter) {
      return Promise.resolve({
        errno: 0,
        data: [createClaimableSample()]
      });
    }

    if (url === api.CouponMy) {
      if (data && data.status === 'used') {
        return Promise.resolve({
          errno: 0,
          data: [createMyCouponSample({
            type: 'discount',
            reduce_amount: '0'
          })]
        });
      }
      return Promise.resolve({
        errno: 0,
        data: [createMyCouponSample()]
      });
    }

    return Promise.resolve({ errno: 0, data: [] });
  };

  util.showErrorToast = function () {};
  util.showSuccessToast = function () {};

  const ctx = createPageContext(couponPage);

  couponPage.onLoad.call(ctx, { tab: 'claimable' });
  assert.strictEqual(ctx.data.tab, 'claimable', 'tab query should activate claimable tab');
  await couponPage.fetchList.call(ctx);
  assert.strictEqual(requestCalls[0].url, api.CouponCenter, 'claimable tab should call CouponCenter');
  assert.strictEqual(ctx.data.list.length, 1, 'claimable should map one coupon');
  assert.strictEqual(ctx.data.list[0].amountText, '20', 'claimable should expose amountText');
  assert.strictEqual(ctx.data.list[0].amountUnit, '元', 'claimable should expose amountUnit');
  assert.strictEqual(ctx.data.list[0].thresholdText, '满100可用', 'claimable should expose thresholdText');
  assert.strictEqual(ctx.data.list[0].buttonStateClass, 'claim-btn--active', 'claimable button class should map');
  assert.strictEqual(ctx.data.list[0].cardStateClass, '', 'unreceived claimable should stay active card');

  requestCalls.length = 0;
  couponPage.onLoad.call(ctx, { status: 'used' });
  assert.strictEqual(ctx.data.tab, 'used', 'legacy status should map to used tab');
  await couponPage.fetchList.call(ctx);
  assert.strictEqual(requestCalls[0].url, api.CouponMy, 'used tab should call CouponMy');
  assert.strictEqual(requestCalls[0].data.status, 'used', 'used tab should pass used status');
  assert.strictEqual(ctx.data.list[0].statusBadgeText, '已使用', 'used tab should map used badge text');
  assert.strictEqual(ctx.data.list[0].statusBadgeClass, 'status-badge--used', 'used tab should map used badge class');
  assert.strictEqual(ctx.data.list[0].cardStateClass, 'coupon-card--muted', 'used tab should map muted card class');

  requestCalls.length = 0;
  couponPage.onLoad.call(ctx, { status: 'unknown-status' });
  assert.strictEqual(ctx.data.tab, 'unused', 'invalid legacy status should fallback to unused tab');
  await couponPage.fetchList.call(ctx);
  assert.strictEqual(requestCalls[0].url, api.CouponMy, 'unused tab should call CouponMy');
  assert.strictEqual(requestCalls[0].data.status, 'unused', 'unused tab should pass unused status');
  assert.strictEqual(ctx.data.list[0].statusBadgeText, '未使用', 'unused tab should map unused badge text');
  assert.strictEqual(ctx.data.list[0].statusBadgeClass, 'status-badge--unused', 'unused tab should map unused badge class');
  assert.strictEqual(ctx.data.list[0].secondaryTimeLabel, '有效期至', 'unused tab should map secondary time label');
}

function testClaimableDisabledDisplayMapping() {
  resetRuntimeState();
  const couponPage = loadPage(couponPagePath);
  const ctx = createPageContext(couponPage);

  const mapped = couponPage.mapClaimableCoupon.call(
    ctx,
    createClaimableSample({
      id: 102,
      type: 'discount',
      has_received: 1,
      reduce_amount: '0'
    })
  );

  assert.strictEqual(mapped.amountText, '9', 'discount coupon should map amountText as discount rate');
  assert.strictEqual(mapped.amountUnit, '折', 'discount coupon should map amountUnit as 折');
  assert.strictEqual(mapped.thresholdText, '最高减50', 'discount coupon should map threshold text as cap');
  assert.strictEqual(mapped.cardStateClass, 'coupon-card--disabled', 'received claimable should be disabled card');
  assert.strictEqual(mapped.buttonStateClass, 'claim-btn--disabled', 'received claimable should be disabled button');
  assert.strictEqual(mapped.actionText, '已领取', 'received claimable should show 已领取');
}

async function testClaimableReceiveRefreshesList() {
  resetRuntimeState();
  const couponPage = loadPage(couponPagePath);
  let receiveCount = 0;
  let centerFetchCount = 0;
  const successMessages = [];

  storage.token = 'token-test';
  util.request = function (url) {
    if (url === api.CouponReceive) {
      receiveCount += 1;
      return Promise.resolve({ errno: 0 });
    }
    if (url === api.CouponCenter) {
      centerFetchCount += 1;
      return Promise.resolve({ errno: 0, data: [] });
    }
    return Promise.resolve({ errno: 0, data: [] });
  };
  util.showSuccessToast = function (msg) {
    successMessages.push(msg);
  };
  util.showErrorToast = function () {};

  const ctx = createPageContext(couponPage);
  couponPage.onLoad.call(ctx, { tab: 'claimable' });
  couponPage.receiveCoupon.call(ctx, {
    currentTarget: {
      dataset: { id: 1001 }
    }
  });
  await flushAsyncTwice();

  assert.strictEqual(receiveCount, 1, 'claimable receive should call CouponReceive once');
  assert.strictEqual(centerFetchCount, 1, 'claimable receive success should refresh claimable list');
  assert.ok(successMessages.includes('领取成功'), 'claimable receive should show success toast');
}

function testDefaultLandingRoutes() {
  resetRuntimeState();
  const homePage = loadPage(homePagePath);
  const homeCtx = createPageContext(homePage);
  homePage.toCouponCenter.call(homeCtx);
  assert.strictEqual(
    navUrls[navUrls.length - 1],
    '/pages/ucenter/coupon/index?tab=claimable&skin=promo',
    'home entry should land on claimable tab'
  );

  const ucenterPage = loadPage(ucenterPagePath);
  const ucenterCtx = createPageContext(ucenterPage);
  ucenterCtx.ensureProfileReady = function () {
    return true;
  };
  ucenterPage.toCoupon.call(ucenterCtx);
  assert.strictEqual(
    navUrls[navUrls.length - 1],
    '/pages/ucenter/coupon/index?skin=promo',
    'ucenter entry should land on my coupon default tab'
  );
}

async function main() {
  testSkinThemeMapping();
  await testApiSelectionByQueryTabAndLegacyStatus();
  testClaimableDisabledDisplayMapping();
  await testClaimableReceiveRefreshesList();
  testDefaultLandingRoutes();
  console.log('miniprogram coupon unified page passed');
}

main().catch((err) => {
  console.error('miniprogram coupon unified page failed:', err.message || err);
  process.exit(1);
});
