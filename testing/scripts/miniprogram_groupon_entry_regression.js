#!/usr/bin/env node
/* eslint-disable no-console */

const assert = require('assert');
const path = require('path');

const goodsPagePath = path.resolve(__dirname, '../../hioshop-miniprogram/pages/goods/goods.js');
const ucenterPagePath = path.resolve(__dirname, '../../hioshop-miniprogram/pages/ucenter/index/index.js');
const utilPath = path.resolve(__dirname, '../../hioshop-miniprogram/utils/util.js');
const wxParseModulePath = path.resolve(__dirname, '../../hioshop-miniprogram/lib/wxParse/wxParse.js');

const navUrls = [];
const switchTabUrls = [];
const toastMessages = [];

global.getApp = function () {
  return { globalData: {} };
};

global.getCurrentPages = function () {
  return [];
};

global.wx = {
  getStorageSync() {
    return '';
  },
  setStorageSync() {},
  removeStorageSync() {},
  navigateTo({ url }) {
    navUrls.push(url);
  },
  switchTab({ url }) {
    switchTabUrls.push(url);
  },
  showToast(opts) {
    toastMessages.push((opts && opts.title) || '');
  },
  showLoading() {},
  hideLoading() {},
  stopPullDownRefresh() {}
};

function loadPage(modulePath) {
  let pageDef = null;
  global.Page = function (def) {
    pageDef = def;
  };
  require.cache[wxParseModulePath] = {
    id: wxParseModulePath,
    filename: wxParseModulePath,
    loaded: true,
    exports: { wxParse() {} }
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

function resetRuntimeState() {
  navUrls.length = 0;
  switchTabUrls.length = 0;
  toastMessages.length = 0;
}

function testGoodsEntryJump() {
  resetRuntimeState();
  const util = require(utilPath);
  util.loginNow = () => true;

  const goodsPage = loadPage(goodsPagePath);
  const ctx = createPageContext(goodsPage);

  ctx.setData({
    id: 1001,
    number: 2,
    grouponActivities: [{ id: 9001 }],
    productList: [{ id: 3001, goods_number: 99 }]
  });

  goodsPage.goOpenGroupon.call(ctx, {
    currentTarget: {
      dataset: {
        activityId: 9001
      }
    }
  });

  assert(navUrls[0], 'goOpenGroupon should navigate');
  assert(navUrls[0].includes('/pages/order-check/index?orderType=2'), 'open groupon should carry orderType=2');
  assert(navUrls[0].includes('grouponActivityId=9001'), 'open groupon should carry grouponActivityId');
  assert(navUrls[0].includes('productId=3001'), 'open groupon should carry productId');

  goodsPage.goJoinGroupon.call(ctx, {
    currentTarget: {
      dataset: {
        activityId: 9001,
        teamId: 81001
      }
    }
  });

  assert(navUrls[1], 'goJoinGroupon should navigate');
  assert(navUrls[1].includes('teamId=81001'), 'join groupon should carry teamId');
}

function testUcenterEntryJump() {
  resetRuntimeState();
  const page = loadPage(ucenterPagePath);
  const ctx = createPageContext(page);
  ctx.ensureProfileReady = () => true;

  page.toGroupon.call(ctx);
  assert.strictEqual(navUrls[0], '/pages/ucenter/groupon/index', 'ucenter groupon entry should navigate to my groupon page');
}

function main() {
  testGoodsEntryJump();
  testUcenterEntryJump();
  console.log('miniprogram groupon entry regression passed');
}

try {
  main();
} catch (error) {
  console.error('miniprogram groupon entry regression failed:', error.message);
  process.exit(1);
}
