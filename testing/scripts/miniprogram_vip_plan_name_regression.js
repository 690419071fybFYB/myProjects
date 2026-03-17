#!/usr/bin/env node
/* eslint-disable no-console */

const assert = require('assert');
const path = require('path');

const vipPagePath = path.resolve(__dirname, '../../hioshop-miniprogram/pages/vip/index.js');

const storage = {};

global.getApp = function () {
  return {globalData: {}};
};

global.getCurrentPages = function () {
  return [];
};

global.wx = {
  getSystemInfoSync() {
    return {platform: 'devtools'};
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
  showToast() {},
  showLoading() {},
  hideLoading() {},
  stopPullDownRefresh() {},
  redirectTo() {},
  switchTab() {},
  navigateBack() {},
  request() {
    throw new Error('unexpected wx.request in vip plan name regression');
  }
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

function createPageContext(pageDef) {
  const initialData = pageDef && pageDef.data ? JSON.parse(JSON.stringify(pageDef.data)) : {};
  return Object.assign({}, pageDef, {
    data: initialData,
    setData(next) {
      this.data = Object.assign({}, this.data, next || {});
    }
  });
}

function testNormalizePlansRepairsMojibakeAndFallback() {
  const vipPage = loadPage(vipPagePath);
  const ctx = createPageContext(vipPage);

  const plans = vipPage.normalizePlans.call(ctx, [
    {
      id: 1,
      plan_name: 'é»„é‡‘ä¼šå‘˜å¹´å¡',
      duration_days: 365,
      price: '69'
    },
    {
      id: 2,
      plan_name: '??????',
      duration_days: 90,
      price: '25'
    }
  ]);

  assert.strictEqual(plans[0].name, '黄金会员年卡', '应修复 latin1/utf8 错乱套餐名称');
  assert.strictEqual(plans[1].name, '黄金会员季卡', '应在不可恢复乱码时按套餐类型回退中文名称');
  assert.strictEqual(plans[0].tag, '年卡', '年卡标签应正确');
  assert.strictEqual(plans[1].tag, '季卡', '季卡标签应正确');
}

function testApplyVipHomeUsesReadableName() {
  const vipPage = loadPage(vipPagePath);
  const ctx = createPageContext(vipPage);

  vipPage.applyVipHome.call(ctx, {
    status: {
      is_vip: 0
    },
    plans: [
      {
        id: 3,
        plan_name: '????',
        duration_days: 365,
        price: '69',
        is_default: 1
      }
    ]
  });

  assert.strictEqual(ctx.data.selectedPlanName, '黄金会员年卡', '首页渲染应展示可读套餐名称');
  assert.strictEqual(ctx.data.selectedPlanPrice, '69.00', '价格展示应格式化为两位小数');
}

function main() {
  testNormalizePlansRepairsMojibakeAndFallback();
  testApplyVipHomeUsesReadableName();
  console.log('miniprogram vip plan name regression passed');
}

main();
