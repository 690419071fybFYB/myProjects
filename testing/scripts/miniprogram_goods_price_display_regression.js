#!/usr/bin/env node
/* eslint-disable no-console */
const assert = require('assert');
const fs = require('fs');
const path = require('path');

const goodsPagePath = path.resolve(__dirname, '../../hioshop-miniprogram/pages/goods/goods.js');
const goodsWxmlPath = path.resolve(__dirname, '../../hioshop-miniprogram/pages/goods/goods.wxml');
const wxParseModulePath = path.resolve(__dirname, '../../hioshop-miniprogram/lib/wxParse/wxParse.js');

global.getApp = function () {
  return { globalData: {} };
};

global.wx = {
  getStorageSync() {
    return '';
  },
  setStorageSync() {},
  showToast() {},
  navigateTo() {},
  switchTab() {},
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
    exports: {
      wxParse() {}
    }
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

function testPromotionDisplayMapping() {
  console.log('1) 商品原价展示映射回归');
  const pageDef = loadPage(goodsPagePath);
  const ctx = createPageContext(pageDef);

  const hiddenOriginal = pageDef.mapPromotionDisplay.call(ctx, {
    has_promotion: 1,
    retail_price: 99,
    promotion_price: 99,
    promotion_original_price: 0
  });
  assert.strictEqual(hiddenOriginal.showOriginalPrice, false, '原价为0或等于现价时应隐藏原价');

  const showOriginal = pageDef.mapPromotionDisplay.call(ctx, {
    has_promotion: 1,
    retail_price: 120,
    promotion_price: 100,
    promotion_original_price: 120
  });
  assert.strictEqual(showOriginal.showOriginalPrice, true, '原价大于现价时应显示原价');

  const nonPromotion = pageDef.mapPromotionDisplay.call(ctx, {
    has_promotion: 0,
    retail_price: 88
  });
  assert.strictEqual(nonPromotion.showOriginalPrice, false, '非促销商品不应展示原价标记');
}

function testTemplateBinding() {
  console.log('2) 商品详情模板绑定回归');
  const wxml = fs.readFileSync(goodsWxmlPath, 'utf8');
  assert(wxml.includes('wx:if="{{goods.showOriginalPrice}}"'), '详情页顶部应使用 goods.showOriginalPrice 控制原价展示');
  assert(wxml.includes('wx:if="{{checkedSpecShowOriginalPrice}}"'), '规格弹窗应使用 checkedSpecShowOriginalPrice 控制原价展示');
}

function main() {
  testPromotionDisplayMapping();
  testTemplateBinding();
  console.log('goods 原价展示回归测试通过。');
}

try {
  main();
} catch (error) {
  console.error('goods 原价展示回归测试失败:', error.message);
  process.exit(1);
}
