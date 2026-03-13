#!/usr/bin/env node
/* eslint-disable no-console */

const assert = require('assert');
const fs = require('fs');
const path = require('path');

const miniRoot = path.resolve(__dirname, '../../hioshop-miniprogram');

function read(relativePath) {
  return fs.readFileSync(path.join(miniRoot, relativePath), 'utf8');
}

function assertContains(content, snippet, message) {
  assert(content.includes(snippet), `${message}\nmissing snippet: ${snippet}`);
}

function runApiConfigRegression() {
  console.log('1) VIP API 配置回归');
  const apiConfig = read('config/api.js');
  assertContains(apiConfig, "api.VipHome = apiRootUrl + 'vip/home';", '缺少 VipHome 接口配置');
  assertContains(apiConfig, "api.VipPlans = apiRootUrl + 'vip/plans';", '缺少 VipPlans 接口配置');
  assertContains(apiConfig, "api.VipStatus = apiRootUrl + 'vip/status';", '缺少 VipStatus 接口配置');
  assertContains(apiConfig, "api.VipCheckout = apiRootUrl + 'vip/checkout';", '缺少 VipCheckout 接口配置');
  assertContains(apiConfig, "api.VipSubmit = apiRootUrl + 'vip/submit';", '缺少 VipSubmit 接口配置');
  assertContains(apiConfig, "api.VipRefundApply = apiRootUrl + 'vip/refundApply';", '缺少 VipRefundApply 接口配置');
  assertContains(apiConfig, "api.VipAutoRenewSign = apiRootUrl + 'vip/autorenewSign';", '缺少 VipAutoRenewSign 接口配置');
  assertContains(apiConfig, "api.VipAutoRenewCancel = apiRootUrl + 'vip/autorenewCancel';", '缺少 VipAutoRenewCancel 接口配置');
}

function runSubmitFlowRegression() {
  console.log('2) VIP 提交流程回归（提交 + 调起支付）');
  const vipPageJs = read('pages/vip/index.js');
  assertContains(vipPageJs, "util.request(api.VipSubmit, payload, 'POST'", 'VIP 页面未调用 VipSubmit');
  assertContains(vipPageJs, 'pay.payOrder(parsedOrderId)', 'VIP 页面未调起支付');
  assertContains(vipPageJs, 'redirectPayResult(status, orderId)', 'VIP 页面缺少支付结果跳转');
  assertContains(vipPageJs, "agreementChecked: true", 'VIP 页面缺少协议勾选默认值');
  assertContains(vipPageJs, "util.showErrorToast('请先同意会员服务协议');", 'VIP 页面缺少协议勾选校验');
  assertContains(vipPageJs, 'autorenew_available', 'VIP 页面未接收自动续费可用状态');
}

function runVisualStructureRegression() {
  console.log('3) VIP 视觉结构回归（仿图风格）');
  const vipWxml = read('pages/vip/index.wxml');
  const vipWxss = read('pages/vip/index.wxss');

  assertContains(vipWxml, 'class="hero-card"', 'VIP 页缺少深色头图容器');
  assertContains(vipWxml, 'class="hero-tabs"', 'VIP 页缺少顶部会员标签区域');
  assertContains(vipWxml, 'class="benefit-grid"', 'VIP 页缺少权益网格区域');
  assertContains(vipWxml, 'class="plan-item {{selectedPlanId == item.planId ? \'plan-item-active\' : \'\'}}"', 'VIP 页缺少套餐激活态样式绑定');
  assertContains(vipWxml, 'class="bottom-action"', 'VIP 页缺少底部固定开通栏');

  assertContains(vipWxss, 'background: linear-gradient(180deg, #0c0f15', 'VIP 页未应用深色顶部背景');
  assertContains(vipWxss, '.hero-card {', 'VIP 页缺少 hero-card 样式');
  assertContains(vipWxss, '.plan-item-active {', 'VIP 页缺少套餐激活样式');
  assertContains(vipWxss, '.bottom-action {', 'VIP 页缺少底部固定栏样式');
}

function main() {
  runApiConfigRegression();
  runSubmitFlowRegression();
  runVisualStructureRegression();
  console.log('miniprogram vip module regression passed');
}

main();
