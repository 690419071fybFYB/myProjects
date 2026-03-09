# Hioshop Nightly Full Regression

- mode: `nightly`
- started_at: `2026-03-09T20:05:15+08:00`
- finished_at: `2026-03-09T20:07:46+08:00`
- summary: `passed=188`, `failed=103`, `skipped=0`, `total=291`

## Layer Summary

| layer | passed | failed | skipped | total |
|---|---:|---:|---:|---:|
| L1 | 178 | 86 | 0 | 264 |
| L2 | 3 | 14 | 0 | 17 |
| L3 | 3 | 3 | 0 | 6 |
| L4 | 4 | 0 | 0 | 4 |

## Results

| id | layer | status | severity | message |
|---|---|---|---|---|
| L2-ADDRESS-FLOW | L2 | failed | P0 | core user journey failed: checkout unexpected errno=412, status=200, errmsg=请先完善登录资料 |
| L2-CART-FLOW | L2 | failed | P0 | core user journey failed: checkout unexpected errno=412, status=200, errmsg=请先完善登录资料 |
| L2-CHECKOUT-FLOW | L2 | failed | P0 | core user journey failed: checkout unexpected errno=412, status=200, errmsg=请先完善登录资料 |
| L2-COUPON-LIFECYCLE | L2 | failed | P0 | 4) 在线单：下单锁券 + 取消释放 |
| L2-GOODS-FLOW | L2 | failed | P0 | core user journey failed: checkout unexpected errno=412, status=200, errmsg=请先完善登录资料 |
| L2-LOGIN-GATE | L2 | failed | P0 | core user journey failed: checkout unexpected errno=412, status=200, errmsg=请先完善登录资料 |
| L2-ORDER-LIFECYCLE | L2 | failed | P0 | core user journey failed: checkout unexpected errno=412, status=200, errmsg=请先完善登录资料 |
| L2-PAY-FLOW | L2 | failed | P0 | notify results: ok=1, fail=0 |
| L2-PROMOTION-LIFECYCLE | L2 | failed | P0 | 开始执行 Promotion V1 mock 联调验证... |
| L2-SUBMIT-FLOW | L2 | failed | P0 | core user journey failed: checkout unexpected errno=412, status=200, errmsg=请先完善登录资料 |
| NIGHTLY-NOTIFY-CONCURRENCY | L2 | failed | P0 | RuntimeError: notify failures: ['OK', 'OK', 'OK'] |
| L1-CORE-PAY | L1 | failed | P1 | mapped_actions=1, failed=1, skipped=0 |
| L2-HOME-PAGE | L2 | failed | P1 | request error: Expecting value: line 1 column 1 (char 0) |
| L3-CROSS-END-SUITE | L3 | failed | P1 | ad create unexpected errno=100, status=200, errmsg=该商品已经有广告关联 |
| L3-ORDER-OPS-CROSS-END | L3 | failed | P1 | blocked by cross-end suite runtime error: ad create unexpected errno=100, status=200, errmsg=该商品已经有广告关联 |
| L1-CORE-ADDRESS | L1 | passed | P1 | mapped_actions=1, failed=0, skipped=0 |
| L1-CORE-AUTH | L1 | passed | P1 | mapped_actions=1, failed=0, skipped=0 |
| L1-CORE-CART | L1 | passed | P1 | mapped_actions=1, failed=0, skipped=0 |
| L1-CORE-COUPON | L1 | passed | P1 | mapped_actions=1, failed=0, skipped=0 |
| L1-CORE-ORDER | L1 | passed | P1 | mapped_actions=1, failed=0, skipped=0 |
| NIGHTLY-SECURITY-ABUSE | L2 | passed | P1 | Security abuse smoke passed. |
| L3-COUPON-CROSS-END | L3 | passed | P1 | coupon_id=142, user_coupon_id=141 |
| L3-PROMOTION-CROSS-END | L3 | passed | P1 | promotion_id=22, goods_id=1009012 |
| L4-ADMIN-LOGIN-SMOKE | L4 | passed | P1 | admin login passed |
| L4-MINI-REQUEST-SMOKE | L4 | passed | P1 | 401/412/network handling smoke passed |
| NIGHTLY-COS-REAL-SMOKE | L4 | passed | P1 | COS 冒烟通过。 |
| L1-FULL-ADMIN-ACTIONS | L1 | failed | P2 | actions=186, failed=68, skipped=0 |
| L1-FULL-ADMIN-ACTIONS::admin.showsetStore | L1 | failed | P2 | status=500 server error |
| L1-FULL-ADMIN-ACTIONS::admin.store | L1 | failed | P2 | status=500 server error |
| L1-FULL-ADMIN-ACTIONS::category.categoryStatus | L1 | failed | P2 | status=500 server error |
| L1-FULL-ADMIN-ACTIONS::category.channelStatus | L1 | failed | P2 | status=500 server error |
| L1-FULL-ADMIN-ACTIONS::category.showStatus | L1 | failed | P2 | status=200 non-json response |
| L1-FULL-ADMIN-ACTIONS::category.store | L1 | failed | P2 | status=500 server error |
| L1-FULL-ADMIN-ACTIONS::goods.checkSku | L1 | failed | P2 | status=500 server error |
| L1-FULL-ADMIN-ACTIONS::goods.copygoods | L1 | failed | P2 | status=500 server error |
| L1-FULL-ADMIN-ACTIONS::goods.gallery | L1 | failed | P2 | status=500 server error |
| L1-FULL-ADMIN-ACTIONS::goods.galleryEdit | L1 | failed | P2 | status=500 server error |
| L1-FULL-ADMIN-ACTIONS::goods.galleryList | L1 | failed | P2 | status=500 server error |
| L1-FULL-ADMIN-ACTIONS::goods.getGalleryList | L1 | failed | P2 | status=500 server error |
| L1-FULL-ADMIN-ACTIONS::goods.indexShowStatus | L1 | failed | P2 | status=200 non-json response |
| L1-FULL-ADMIN-ACTIONS::goods.productStatus | L1 | failed | P2 | status=500 server error |
| L1-FULL-ADMIN-ACTIONS::goods.saleStatus | L1 | failed | P2 | status=500 server error |
| L1-FULL-ADMIN-ACTIONS::goods.sort | L1 | failed | P2 | status=200 non-json response |
| L1-FULL-ADMIN-ACTIONS::goods.store | L1 | failed | P2 | status=500 server error |
| L1-FULL-ADMIN-ACTIONS::goods.updateGoodsNumber | L1 | failed | P2 | request error: HTTPConnectionPool(host='127.0.0.1', port=8360): Read timed out. (read timeout=20) |
| L1-FULL-ADMIN-ACTIONS::goods.updatePrice | L1 | failed | P2 | status=500 server error |
| L1-FULL-ADMIN-ACTIONS::goods.updateShortName | L1 | failed | P2 | status=500 server error |
| L1-FULL-ADMIN-ACTIONS::notice.updateContent | L1 | failed | P2 | status=500 server error |
| L1-FULL-ADMIN-ACTIONS::order.changeStatus | L1 | failed | P2 | status=500 server error |
| L1-FULL-ADMIN-ACTIONS::order.detail | L1 | failed | P2 | status=500 server error |
| L1-FULL-ADMIN-ACTIONS::order.directPrintExpress | L1 | failed | P2 | status=500 server error |
| L1-FULL-ADMIN-ACTIONS::order.getGoodsSpecification | L1 | failed | P2 | status=500 server error |
| L1-FULL-ADMIN-ACTIONS::order.getMianExpress | L1 | failed | P2 | status=500 server error |
| L1-FULL-ADMIN-ACTIONS::order.getOrderExpress | L1 | failed | P2 | status=500 server error |
| L1-FULL-ADMIN-ACTIONS::order.goDelivery | L1 | failed | P2 | status=500 server error |
| L1-FULL-ADMIN-ACTIONS::order.goodsListDelete | L1 | failed | P2 | status=500 server error |
| L1-FULL-ADMIN-ACTIONS::order.orderDelivery | L1 | failed | P2 | status=500 server error |
| L1-FULL-ADMIN-ACTIONS::order.orderPrice | L1 | failed | P2 | status=500 server error |
| L1-FULL-ADMIN-ACTIONS::order.orderReceive | L1 | failed | P2 | status=500 server error |
| L1-FULL-ADMIN-ACTIONS::order.orderpack | L1 | failed | P2 | status=500 server error |
| L1-FULL-ADMIN-ACTIONS::order.rePrintExpress | L1 | failed | P2 | status=500 server error |
| L1-FULL-ADMIN-ACTIONS::order.saveAddress | L1 | failed | P2 | status=500 server error |
| L1-FULL-ADMIN-ACTIONS::order.saveAdminMemo | L1 | failed | P2 | status=500 server error |
| L1-FULL-ADMIN-ACTIONS::order.saveExpressValueInfo | L1 | failed | P2 | status=500 server error |
| L1-FULL-ADMIN-ACTIONS::order.saveGoodsList | L1 | failed | P2 | status=200 non-json response |
| L1-FULL-ADMIN-ACTIONS::order.savePrintInfo | L1 | failed | P2 | status=500 server error |
| L1-FULL-ADMIN-ACTIONS::order.saveRemarkInfo | L1 | failed | P2 | status=500 server error |
| L1-FULL-ADMIN-ACTIONS::order.store | L1 | failed | P2 | status=500 server error |
| L1-FULL-ADMIN-ACTIONS::shipper.addExceptArea | L1 | failed | P2 | status=500 server error |
| L1-FULL-ADMIN-ACTIONS::shipper.addTable | L1 | failed | P2 | status=500 server error |
| L1-FULL-ADMIN-ACTIONS::shipper.enabledStatus | L1 | failed | P2 | status=500 server error |
| L1-FULL-ADMIN-ACTIONS::shipper.exceptAreaDetail | L1 | failed | P2 | status=500 server error |
| L1-FULL-ADMIN-ACTIONS::shipper.saveExceptArea | L1 | failed | P2 | status=500 server error |
| L1-FULL-ADMIN-ACTIONS::shipper.saveTable | L1 | failed | P2 | status=500 server error |
| L1-FULL-ADMIN-ACTIONS::specification.checkSn | L1 | failed | P2 | status=500 server error |
| L1-FULL-ADMIN-ACTIONS::specification.detail | L1 | failed | P2 | status=500 server error |
| L1-FULL-ADMIN-ACTIONS::specification.getGoodsSpec | L1 | failed | P2 | status=500 server error |
| L1-FULL-ADMIN-ACTIONS::specification.productDele | L1 | failed | P2 | status=500 server error |
| L1-FULL-ADMIN-ACTIONS::specification.productUpdate | L1 | failed | P2 | status=500 server error |
| L1-FULL-ADMIN-ACTIONS::user.address | L1 | failed | P2 | status=500 server error |
| L1-FULL-ADMIN-ACTIONS::user.cartdata | L1 | failed | P2 | status=500 server error |
| L1-FULL-ADMIN-ACTIONS::user.datainfo | L1 | failed | P2 | status=500 server error |
| L1-FULL-ADMIN-ACTIONS::user.foot | L1 | failed | P2 | status=500 server error |
| L1-FULL-ADMIN-ACTIONS::user.info | L1 | failed | P2 | status=500 server error |
| L1-FULL-ADMIN-ACTIONS::user.order | L1 | failed | P2 | status=500 server error |
| L1-FULL-ADMIN-ACTIONS::user.saveaddress | L1 | failed | P2 | status=500 server error |
| L1-FULL-ADMIN-ACTIONS::user.store | L1 | failed | P2 | status=500 server error |
| L1-FULL-ADMIN-ACTIONS::user.updateInfo | L1 | failed | P2 | status=500 server error |
| L1-FULL-ADMIN-ACTIONS::user.updateMobile | L1 | failed | P2 | status=500 server error |
| L1-FULL-ADMIN-ACTIONS::wap.getGoodsSnName | L1 | failed | P2 | status=500 server error |
| L1-FULL-ADMIN-ACTIONS::wap.info | L1 | failed | P2 | status=500 server error |
| L1-FULL-ADMIN-ACTIONS::wap.saleStatus | L1 | failed | P2 | status=500 server error |
| L1-FULL-ADMIN-ACTIONS::wap.sort | L1 | failed | P2 | status=200 non-json response |
| L1-FULL-ADMIN-ACTIONS::wap.store | L1 | failed | P2 | status=500 server error |
| L1-FULL-ADMIN-ACTIONS::wap.updatePrice | L1 | failed | P2 | status=500 server error |
| L1-FULL-API-ACTIONS | L1 | failed | P2 | actions=68, failed=15, skipped=0 |
| L1-FULL-API-ACTIONS::cart.checked | L1 | failed | P2 | status=500 server error |
| L1-FULL-API-ACTIONS::catalog.currentlist | L1 | failed | P2 | status=500 server error |
| L1-FULL-API-ACTIONS::crontab.resetSql | L1 | failed | P2 | status=200 non-json response |
| L1-FULL-API-ACTIONS::crontab.timetask | L1 | failed | P2 | status=200 non-json response |
| L1-FULL-API-ACTIONS::goods.goodsShare | L1 | failed | P2 | status=500 server error |
| L1-FULL-API-ACTIONS::index.index | L1 | failed | P2 | status=200 non-json response |
| L1-FULL-API-ACTIONS::pay.notify | L1 | failed | P2 | status=200 non-json response |
| L1-FULL-API-ACTIONS::pay.preWeixinPay | L1 | failed | P2 | status=500 server error |
| L1-FULL-API-ACTIONS::pay.preWeixinPaya | L1 | failed | P2 | status=404 non-json response |
| L1-FULL-API-ACTIONS::region.code | L1 | failed | P2 | status=500 server error |
| L1-FULL-API-ACTIONS::region.data | L1 | failed | P2 | status=500 server error |
| L1-FULL-API-ACTIONS::region.info | L1 | failed | P2 | status=500 server error |
| L1-FULL-API-ACTIONS::upload.deleteFile | L1 | failed | P2 | status=404 non-json response |
| L1-FULL-API-ACTIONS::weChat.notify | L1 | failed | P2 | status=500 server error |
| L1-FULL-API-ACTIONS::weChat.receive | L1 | failed | P2 | status=500 server error |
| L2-OPERATIONS-FLOW | L2 | failed | P2 | import_script=failed; operations_audit=failed |
| L2-SEARCH-FOOTPRINT | L2 | failed | P2 | footprint list unexpected errno=412, status=200, errmsg=请先完善登录资料 |
| L3-AD-CROSS-END | L3 | failed | P2 | blocked by cross-end suite runtime error: ad create unexpected errno=100, status=200, errmsg=该商品已经有广告关联 |
| L1-CORE-AD | L1 | passed | P2 | mapped_actions=1, failed=0, skipped=0 |
| L1-CORE-SETTINGS | L1 | passed | P2 | mapped_actions=1, failed=0, skipped=0 |
| L1-FULL-ADMIN-ACTIONS::ad.destory | L1 | passed | P2 | status=200, errno=400 |
| L1-FULL-ADMIN-ACTIONS::ad.getallrelate | L1 | passed | P2 | status=200, errno=0 |
| L1-FULL-ADMIN-ACTIONS::ad.index | L1 | passed | P2 | status=200, errno=0 |
| L1-FULL-ADMIN-ACTIONS::ad.info | L1 | passed | P2 | status=200, errno=400 |
| L1-FULL-ADMIN-ACTIONS::ad.saleStatus | L1 | passed | P2 | status=200, errno=400 |
| L1-FULL-ADMIN-ACTIONS::ad.store | L1 | passed | P2 | status=200, errno=400 |
| L1-FULL-ADMIN-ACTIONS::ad.updateSort | L1 | passed | P2 | status=200, errno=400 |
| L1-FULL-ADMIN-ACTIONS::admin.adminAdd | L1 | passed | P2 | status=200, errno=400 |
| L1-FULL-ADMIN-ACTIONS::admin.adminDetail | L1 | passed | P2 | status=200, errno=404 |
| L1-FULL-ADMIN-ACTIONS::admin.adminSave | L1 | passed | P2 | status=200, errno=400 |
| L1-FULL-ADMIN-ACTIONS::admin.changeAutoStatus | L1 | passed | P2 | status=200, errno=0 |
| L1-FULL-ADMIN-ACTIONS::admin.deleAdmin | L1 | passed | P2 | status=200, errno=0 |
| L1-FULL-ADMIN-ACTIONS::admin.index | L1 | passed | P2 | status=200, errno=0 |
| L1-FULL-ADMIN-ACTIONS::admin.info | L1 | passed | P2 | status=200, errno=0 |
| L1-FULL-ADMIN-ACTIONS::admin.senderInfo | L1 | passed | P2 | status=200, errno=0 |
| L1-FULL-ADMIN-ACTIONS::admin.showset | L1 | passed | P2 | status=200, errno=0 |
| L1-FULL-ADMIN-ACTIONS::admin.storeShipperSettings | L1 | passed | P2 | status=200, errno=0 |
| L1-FULL-ADMIN-ACTIONS::auth.login | L1 | passed | P2 | status=200, errno=401 |
| L1-FULL-ADMIN-ACTIONS::category.deleteBannerImage | L1 | passed | P2 | status=200, errno=0 |
| L1-FULL-ADMIN-ACTIONS::category.deleteIconImage | L1 | passed | P2 | status=200, errno=0 |
| L1-FULL-ADMIN-ACTIONS::category.destory | L1 | passed | P2 | status=200, errno=0 |
| L1-FULL-ADMIN-ACTIONS::category.index | L1 | passed | P2 | status=200, errno=0 |
| L1-FULL-ADMIN-ACTIONS::category.info | L1 | passed | P2 | status=200, errno=0 |
| L1-FULL-ADMIN-ACTIONS::category.topCategory | L1 | passed | P2 | status=200, errno=0 |
| L1-FULL-ADMIN-ACTIONS::category.updateSort | L1 | passed | P2 | status=200, errno=0 |
| L1-FULL-ADMIN-ACTIONS::coupon.claimRecord | L1 | passed | P2 | status=200, errno=0 |
| L1-FULL-ADMIN-ACTIONS::coupon.claimRecordExport | L1 | passed | P2 | status=200 non-json allowed |
| L1-FULL-ADMIN-ACTIONS::coupon.create | L1 | passed | P2 | status=200, errno=400 |
| L1-FULL-ADMIN-ACTIONS::coupon.delete | L1 | passed | P2 | status=200, errno=400 |
| L1-FULL-ADMIN-ACTIONS::coupon.detail | L1 | passed | P2 | status=200, errno=400 |
| L1-FULL-ADMIN-ACTIONS::coupon.list | L1 | passed | P2 | status=200, errno=0 |
| L1-FULL-ADMIN-ACTIONS::coupon.toggle | L1 | passed | P2 | status=200, errno=400 |
| L1-FULL-ADMIN-ACTIONS::coupon.update | L1 | passed | P2 | status=200, errno=400 |
| L1-FULL-ADMIN-ACTIONS::coupon.useRecord | L1 | passed | P2 | status=200, errno=0 |
| L1-FULL-ADMIN-ACTIONS::coupon.useRecordExport | L1 | passed | P2 | status=200 non-json allowed |
| L1-FULL-ADMIN-ACTIONS::delivery.index | L1 | passed | P2 | status=200, errno=0 |
| L1-FULL-ADMIN-ACTIONS::goods.deleteGalleryFile | L1 | passed | P2 | status=200, errno=0 |
| L1-FULL-ADMIN-ACTIONS::goods.deleteListPicUrl | L1 | passed | P2 | status=200, errno=0 |
| L1-FULL-ADMIN-ACTIONS::goods.destory | L1 | passed | P2 | status=200, errno=0 |
| L1-FULL-ADMIN-ACTIONS::goods.drop | L1 | passed | P2 | status=200, errno=0 |
| L1-FULL-ADMIN-ACTIONS::goods.getAllCategory | L1 | passed | P2 | status=200, errno=0 |
| L1-FULL-ADMIN-ACTIONS::goods.getAllCategory1 | L1 | passed | P2 | status=200, errno=0 |
| L1-FULL-ADMIN-ACTIONS::goods.getAllSpecification | L1 | passed | P2 | status=200, errno=0 |
| L1-FULL-ADMIN-ACTIONS::goods.getExpressData | L1 | passed | P2 | status=200, errno=0 |
| L1-FULL-ADMIN-ACTIONS::goods.importTaskCreate | L1 | passed | P2 | status=200, errno=400 |
| L1-FULL-ADMIN-ACTIONS::goods.importTaskDetail | L1 | passed | P2 | status=200, errno=400 |
| L1-FULL-ADMIN-ACTIONS::goods.importTaskErrorFile | L1 | passed | P2 | status=200, errno=400 |
| L1-FULL-ADMIN-ACTIONS::goods.importTaskList | L1 | passed | P2 | status=200, errno=0 |
| L1-FULL-ADMIN-ACTIONS::goods.importTemplate | L1 | passed | P2 | status=200 non-json allowed |
| L1-FULL-ADMIN-ACTIONS::goods.index | L1 | passed | P2 | status=200, errno=0 |
| L1-FULL-ADMIN-ACTIONS::goods.info | L1 | passed | P2 | status=200, errno=0 |
| L1-FULL-ADMIN-ACTIONS::goods.onsale | L1 | passed | P2 | status=200, errno=0 |
| L1-FULL-ADMIN-ACTIONS::goods.out | L1 | passed | P2 | status=200, errno=0 |
| L1-FULL-ADMIN-ACTIONS::goods.picker | L1 | passed | P2 | status=200, errno=0 |
| L1-FULL-ADMIN-ACTIONS::goods.pickerList | L1 | passed | P2 | status=200, errno=0 |
| L1-FULL-ADMIN-ACTIONS::goods.pickerSelected | L1 | passed | P2 | status=200, errno=0 |
| L1-FULL-ADMIN-ACTIONS::goods.pickerSku | L1 | passed | P2 | status=200, errno=400 |
| L1-FULL-ADMIN-ACTIONS::goods.updateSort | L1 | passed | P2 | status=200, errno=0 |
| L1-FULL-ADMIN-ACTIONS::goods.uploadHttpsImage | L1 | passed | P2 | status=200, errno=400 |
| L1-FULL-ADMIN-ACTIONS::index.checkLogin | L1 | passed | P2 | status=200, errno=0 |
| L1-FULL-ADMIN-ACTIONS::index.getQiniuToken | L1 | passed | P2 | status=200, errno=0 |
| L1-FULL-ADMIN-ACTIONS::index.index | L1 | passed | P2 | status=200, errno=0 |
| L1-FULL-ADMIN-ACTIONS::index.main | L1 | passed | P2 | status=200, errno=0 |
| L1-FULL-ADMIN-ACTIONS::invite.config | L1 | passed | P2 | status=200, errno=0 |
| L1-FULL-ADMIN-ACTIONS::invite.list | L1 | passed | P2 | status=200, errno=0 |
| L1-FULL-ADMIN-ACTIONS::keywords.index | L1 | passed | P2 | status=200, errno=0 |
| L1-FULL-ADMIN-ACTIONS::notice.add | L1 | passed | P2 | status=200, errno=0 |
| L1-FULL-ADMIN-ACTIONS::notice.destory | L1 | passed | P2 | status=200, errno=0 |
| L1-FULL-ADMIN-ACTIONS::notice.index | L1 | passed | P2 | status=200, errno=0 |
| L1-FULL-ADMIN-ACTIONS::notice.update | L1 | passed | P2 | status=200, errno=0 |
| L1-FULL-ADMIN-ACTIONS::order.checkExpress | L1 | passed | P2 | status=200, errno=100 |
| L1-FULL-ADMIN-ACTIONS::order.destory | L1 | passed | P2 | status=200, errno=0 |
| L1-FULL-ADMIN-ACTIONS::order.getAllRegion | L1 | passed | P2 | status=200, errno=0 |
| L1-FULL-ADMIN-ACTIONS::order.getAutoStatus | L1 | passed | P2 | status=200, errno=0 |
| L1-FULL-ADMIN-ACTIONS::order.getPrintTest | L1 | passed | P2 | status=200, errno=0 |
| L1-FULL-ADMIN-ACTIONS::order.goPrintOnly | L1 | passed | P2 | status=200, errno=0 |
| L1-FULL-ADMIN-ACTIONS::order.index | L1 | passed | P2 | status=200, errno=0 |
| L1-FULL-ADMIN-ACTIONS::order.toDelivery | L1 | passed | P2 | status=200, errno=0 |
| L1-FULL-ADMIN-ACTIONS::permission.tree | L1 | passed | P2 | status=200, errno=0 |
| L1-FULL-ADMIN-ACTIONS::promotion.create | L1 | passed | P2 | status=200, errno=400 |
| L1-FULL-ADMIN-ACTIONS::promotion.delete | L1 | passed | P2 | status=200, errno=400 |
| L1-FULL-ADMIN-ACTIONS::promotion.detail | L1 | passed | P2 | status=200, errno=400 |
| L1-FULL-ADMIN-ACTIONS::promotion.list | L1 | passed | P2 | status=200, errno=0 |
| L1-FULL-ADMIN-ACTIONS::promotion.toggle | L1 | passed | P2 | status=200, errno=400 |
| L1-FULL-ADMIN-ACTIONS::promotion.update | L1 | passed | P2 | status=200, errno=400 |
| L1-FULL-ADMIN-ACTIONS::role.create | L1 | passed | P2 | status=200, errno=400 |
| L1-FULL-ADMIN-ACTIONS::role.delete | L1 | passed | P2 | status=200, errno=400 |
| L1-FULL-ADMIN-ACTIONS::role.grant | L1 | passed | P2 | status=200, errno=400 |
| L1-FULL-ADMIN-ACTIONS::role.list | L1 | passed | P2 | status=200, errno=0 |
| L1-FULL-ADMIN-ACTIONS::role.update | L1 | passed | P2 | status=200, errno=400 |
| L1-FULL-ADMIN-ACTIONS::shipper.destory | L1 | passed | P2 | status=200, errno=0 |
| L1-FULL-ADMIN-ACTIONS::shipper.exceptAreaDelete | L1 | passed | P2 | status=200, errno=0 |
| L1-FULL-ADMIN-ACTIONS::shipper.exceptarea | L1 | passed | P2 | status=200, errno=0 |
| L1-FULL-ADMIN-ACTIONS::shipper.freight | L1 | passed | P2 | status=200, errno=0 |
| L1-FULL-ADMIN-ACTIONS::shipper.freightdetail | L1 | passed | P2 | status=200, errno=0 |
| L1-FULL-ADMIN-ACTIONS::shipper.getareadata | L1 | passed | P2 | status=200, errno=0 |
| L1-FULL-ADMIN-ACTIONS::shipper.index | L1 | passed | P2 | status=200, errno=0 |
| L1-FULL-ADMIN-ACTIONS::shipper.info | L1 | passed | P2 | status=200, errno=0 |
| L1-FULL-ADMIN-ACTIONS::shipper.list | L1 | passed | P2 | status=200, errno=0 |
| L1-FULL-ADMIN-ACTIONS::shipper.store | L1 | passed | P2 | status=200, errno=0 |
| L1-FULL-ADMIN-ACTIONS::shipper.updateSort | L1 | passed | P2 | status=200, errno=0 |
| L1-FULL-ADMIN-ACTIONS::shopcart.index | L1 | passed | P2 | status=200, errno=0 |
| L1-FULL-ADMIN-ACTIONS::specification.add | L1 | passed | P2 | status=200, errno=0 |
| L1-FULL-ADMIN-ACTIONS::specification.delePrimarySpec | L1 | passed | P2 | status=200, errno=0 |
| L1-FULL-ADMIN-ACTIONS::specification.delete | L1 | passed | P2 | status=200, errno=0 |
| L1-FULL-ADMIN-ACTIONS::specification.index | L1 | passed | P2 | status=200, errno=0 |
| L1-FULL-ADMIN-ACTIONS::specification.update | L1 | passed | P2 | status=200, errno=0 |
| L1-FULL-ADMIN-ACTIONS::user.destory | L1 | passed | P2 | status=200, errno=0 |
| L1-FULL-ADMIN-ACTIONS::user.index | L1 | passed | P2 | status=200, errno=0 |
| L1-FULL-ADMIN-ACTIONS::user.updateName | L1 | passed | P2 | status=200, errno=0 |
| L1-FULL-ADMIN-ACTIONS::wap.destory | L1 | passed | P2 | status=200, errno=0 |
| L1-FULL-ADMIN-ACTIONS::wap.drop | L1 | passed | P2 | status=200, errno=0 |
| L1-FULL-ADMIN-ACTIONS::wap.getAllCategory | L1 | passed | P2 | status=200, errno=0 |
| L1-FULL-ADMIN-ACTIONS::wap.getAllCategory1 | L1 | passed | P2 | status=200, errno=0 |
| L1-FULL-ADMIN-ACTIONS::wap.index | L1 | passed | P2 | status=200, errno=0 |
| L1-FULL-ADMIN-ACTIONS::wap.onsale | L1 | passed | P2 | status=200, errno=0 |
| L1-FULL-ADMIN-ACTIONS::wap.out | L1 | passed | P2 | status=200, errno=0 |
| L1-FULL-ADMIN-ACTIONS::wap.outsale | L1 | passed | P2 | status=200, errno=0 |
| L1-FULL-API-ACTIONS::ad.messages | L1 | passed | P2 | status=200, errno=0 |
| L1-FULL-API-ACTIONS::ad.readAll | L1 | passed | P2 | status=200, errno=0 |
| L1-FULL-API-ACTIONS::ad.unreadCount | L1 | passed | P2 | status=200, errno=0 |
| L1-FULL-API-ACTIONS::address.addressDetail | L1 | passed | P2 | status=200, errno=412 |
| L1-FULL-API-ACTIONS::address.deleteAddress | L1 | passed | P2 | status=200, errno=412 |
| L1-FULL-API-ACTIONS::address.getAddresses | L1 | passed | P2 | status=200, errno=412 |
| L1-FULL-API-ACTIONS::address.saveAddress | L1 | passed | P2 | status=200, errno=412 |
| L1-FULL-API-ACTIONS::auth.loginByWeixin | L1 | passed | P2 | status=200, errno=400 |
| L1-FULL-API-ACTIONS::auth.logout | L1 | passed | P2 | status=200, errno=0 |
| L1-FULL-API-ACTIONS::auth.phoneNumber | L1 | passed | P2 | status=200, errno=401 |
| L1-FULL-API-ACTIONS::cart.add | L1 | passed | P2 | status=200, errno=400 |
| L1-FULL-API-ACTIONS::cart.checkout | L1 | passed | P2 | status=200, errno=412 |
| L1-FULL-API-ACTIONS::cart.delete | L1 | passed | P2 | status=200, errno=1000 |
| L1-FULL-API-ACTIONS::cart.goodsCount | L1 | passed | P2 | status=200, errno=0 |
| L1-FULL-API-ACTIONS::cart.index | L1 | passed | P2 | status=200, errno=0 |
| L1-FULL-API-ACTIONS::cart.update | L1 | passed | P2 | status=200, errno=404 |
| L1-FULL-API-ACTIONS::catalog.current | L1 | passed | P2 | status=200, errno=0 |
| L1-FULL-API-ACTIONS::catalog.index | L1 | passed | P2 | status=200, errno=0 |
| L1-FULL-API-ACTIONS::coupon.center | L1 | passed | P2 | status=200, errno=0 |
| L1-FULL-API-ACTIONS::coupon.my | L1 | passed | P2 | status=200, errno=0 |
| L1-FULL-API-ACTIONS::coupon.preview | L1 | passed | P2 | status=200, errno=0 |
| L1-FULL-API-ACTIONS::coupon.receive | L1 | passed | P2 | status=200, errno=400 |
| L1-FULL-API-ACTIONS::crontab.processGoodsImportTask | L1 | passed | P2 | status=200, errno=0 |
| L1-FULL-API-ACTIONS::footprint.delete | L1 | passed | P2 | status=200, errno=412 |
| L1-FULL-API-ACTIONS::footprint.list | L1 | passed | P2 | status=200, errno=412 |
| L1-FULL-API-ACTIONS::goods.count | L1 | passed | P2 | status=200, errno=0 |
| L1-FULL-API-ACTIONS::goods.detail | L1 | passed | P2 | status=200, errno=1000 |
| L1-FULL-API-ACTIONS::goods.index | L1 | passed | P2 | status=200, errno=0 |
| L1-FULL-API-ACTIONS::goods.list | L1 | passed | P2 | status=200, errno=0 |
| L1-FULL-API-ACTIONS::index.appInfo | L1 | passed | P2 | status=200, errno=0 |
| L1-FULL-API-ACTIONS::invite.myRecords | L1 | passed | P2 | status=200, errno=0 |
| L1-FULL-API-ACTIONS::invite.mySummary | L1 | passed | P2 | status=200, errno=0 |
| L1-FULL-API-ACTIONS::order.cancel | L1 | passed | P2 | status=200, errno=412 |
| L1-FULL-API-ACTIONS::order.complete | L1 | passed | P2 | status=200, errno=412 |
| L1-FULL-API-ACTIONS::order.confirm | L1 | passed | P2 | status=200, errno=412 |
| L1-FULL-API-ACTIONS::order.count | L1 | passed | P2 | status=200, errno=412 |
| L1-FULL-API-ACTIONS::order.delete | L1 | passed | P2 | status=200, errno=412 |
| L1-FULL-API-ACTIONS::order.detail | L1 | passed | P2 | status=200, errno=412 |
| L1-FULL-API-ACTIONS::order.express | L1 | passed | P2 | status=200, errno=412 |
| L1-FULL-API-ACTIONS::order.list | L1 | passed | P2 | status=200, errno=412 |
| L1-FULL-API-ACTIONS::order.orderCount | L1 | passed | P2 | status=200, errno=412 |
| L1-FULL-API-ACTIONS::order.orderGoods | L1 | passed | P2 | status=200, errno=412 |
| L1-FULL-API-ACTIONS::order.submit | L1 | passed | P2 | status=200, errno=412 |
| L1-FULL-API-ACTIONS::order.update | L1 | passed | P2 | status=200, errno=412 |
| L1-FULL-API-ACTIONS::qrcode.getBase64 | L1 | passed | P2 | status=200, errno=0 |
| L1-FULL-API-ACTIONS::region.list | L1 | passed | P2 | status=200, errno=0 |
| L1-FULL-API-ACTIONS::search.clearHistory | L1 | passed | P2 | status=200, errno=0 |
| L1-FULL-API-ACTIONS::search.helper | L1 | passed | P2 | status=200, errno=0 |
| L1-FULL-API-ACTIONS::search.index | L1 | passed | P2 | status=200, errno=0 |
| L1-FULL-API-ACTIONS::settings.save | L1 | passed | P2 | status=200, errno=400 |
| L1-FULL-API-ACTIONS::settings.showSettings | L1 | passed | P2 | status=200, errno=0 |
| L1-FULL-API-ACTIONS::settings.userDetail | L1 | passed | P2 | status=200, errno=0 |
| L1-FULL-API-ACTIONS::upload.uploadAvatar | L1 | passed | P2 | status=200, errno=1000 |
| L2-AD-MESSAGE-FLOW | L2 | passed | P2 | before=0, after=0, user_ad_read_before=2, user_ad_read_after=2 |
| L2-INVITE-FLOW | L2 | passed | P2 | schema_ready=1, invite_total=0 |
| L3-ADMIN-AUTH-PREREQ | L3 | passed | P2 | admin token acquired |
| L4-MINI-SYNTAX-SMOKE | L4 | passed | P2 | syntax checks passed |

## Failures (With Repro)

- `L2-ADDRESS-FLOW` [P0] Address create/default/use flow: core user journey failed: checkout unexpected errno=412, status=200, errmsg=请先完善登录资料
  - repro_step: run `python3 testing/scripts/core_user_journey.py --base-url http://127.0.0.1:8360 --api-jwt-secret bae4fdabcc11cba5bb4aa9225bdbda8a936b41d729e86a65f44c02313d839278 --api-user-id 1 --db-host 127.0.0.1 --db-port 3306 --db-user root --db-password CHANGE_ME_STRONG_PASSWORD --db-name hiolabsDB`
  - evidence: `core user journey failed: checkout unexpected errno=412, status=200, errmsg=请先完善登录资料`
- `L2-CART-FLOW` [P0] Cart select/update/delete/count flow: core user journey failed: checkout unexpected errno=412, status=200, errmsg=请先完善登录资料
  - repro_step: run `python3 testing/scripts/core_user_journey.py --base-url http://127.0.0.1:8360 --api-jwt-secret bae4fdabcc11cba5bb4aa9225bdbda8a936b41d729e86a65f44c02313d839278 --api-user-id 1 --db-host 127.0.0.1 --db-port 3306 --db-user root --db-password CHANGE_ME_STRONG_PASSWORD --db-name hiolabsDB`
  - evidence: `core user journey failed: checkout unexpected errno=412, status=200, errmsg=请先完善登录资料`
- `L2-CHECKOUT-FLOW` [P0] Checkout freight/promotion/coupon flow: core user journey failed: checkout unexpected errno=412, status=200, errmsg=请先完善登录资料
  - repro_step: run `python3 testing/scripts/core_user_journey.py --base-url http://127.0.0.1:8360 --api-jwt-secret bae4fdabcc11cba5bb4aa9225bdbda8a936b41d729e86a65f44c02313d839278 --api-user-id 1 --db-host 127.0.0.1 --db-port 3306 --db-user root --db-password CHANGE_ME_STRONG_PASSWORD --db-name hiolabsDB`
  - evidence: `core user journey failed: checkout unexpected errno=412, status=200, errmsg=请先完善登录资料`
- `L2-COUPON-LIFECYCLE` [P0] Coupon receive/preview/lock/use/release flow: 4) 在线单：下单锁券 + 取消释放
  - repro_step: run `node scripts/test-coupon.js`
  - evidence: `Coupon 自动化测试失败: [/api/order/submit] errno=412 errmsg=请先完善登录资料`
- `L2-GOODS-FLOW` [P0] Goods detail/spec/add-cart/buy-now flow: core user journey failed: checkout unexpected errno=412, status=200, errmsg=请先完善登录资料
  - repro_step: run `python3 testing/scripts/core_user_journey.py --base-url http://127.0.0.1:8360 --api-jwt-secret bae4fdabcc11cba5bb4aa9225bdbda8a936b41d729e86a65f44c02313d839278 --api-user-id 1 --db-host 127.0.0.1 --db-port 3306 --db-user root --db-password CHANGE_ME_STRONG_PASSWORD --db-name hiolabsDB`
  - evidence: `core user journey failed: checkout unexpected errno=412, status=200, errmsg=请先完善登录资料`
- `L2-LOGIN-GATE` [P0] Login gate and profile completeness checks: core user journey failed: checkout unexpected errno=412, status=200, errmsg=请先完善登录资料
  - repro_step: run `python3 testing/scripts/core_user_journey.py --base-url http://127.0.0.1:8360 --api-jwt-secret bae4fdabcc11cba5bb4aa9225bdbda8a936b41d729e86a65f44c02313d839278 --api-user-id 1 --db-host 127.0.0.1 --db-port 3306 --db-user root --db-password CHANGE_ME_STRONG_PASSWORD --db-name hiolabsDB`
  - evidence: `core user journey failed: checkout unexpected errno=412, status=200, errmsg=请先完善登录资料`
- `L2-ORDER-LIFECYCLE` [P0] Order lifecycle cancel/status flow: core user journey failed: checkout unexpected errno=412, status=200, errmsg=请先完善登录资料
  - repro_step: run `python3 testing/scripts/core_user_journey.py --base-url http://127.0.0.1:8360 --api-jwt-secret bae4fdabcc11cba5bb4aa9225bdbda8a936b41d729e86a65f44c02313d839278 --api-user-id 1 --db-host 127.0.0.1 --db-port 3306 --db-user root --db-password CHANGE_ME_STRONG_PASSWORD --db-name hiolabsDB`
  - evidence: `core user journey failed: checkout unexpected errno=412, status=200, errmsg=请先完善登录资料`
- `L2-PAY-FLOW` [P0] Pay notify and idempotency flow: notify results: ok=1, fail=0
  - repro_step: run `python3 testing/scripts/pay_notify_concurrency.py --base-url http://127.0.0.1:8360 --workers 1 --user-id 1 --api-jwt-secret bae4fdabcc11cba5bb4aa9225bdbda8a936b41d729e86a65f44c02313d839278 --db-host 127.0.0.1 --db-port 3306 --db-user root --db-password CHANGE_ME_STRONG_PASSWORD --db-name hiolabsDB`
  - evidence: `Traceback (most recent call last):
  File "/Volumes/SAMSUNG/fyb/myProjects/testing/scripts/pay_notify_concurrency.py", line 383, in <module>
    raise SystemExit(main())
                     ~~~~^^
  File "/Volumes/SAMSUNG/fyb/myProjects/testing/scripts/pay_notify_concurrency.py", line 370, in main
    raise RuntimeError(f"goods stock decrement expected 1, got before={goods_before}, after={goods_after}")
RuntimeError: goods stock decrement expected 1, got before=71, after=71`
- `L2-PROMOTION-LIFECYCLE` [P0] Promotion and best-price flow: 开始执行 Promotion V1 mock 联调验证...
  - repro_step: run `node scripts/test-promotion-v1.js`
  - evidence: `Promotion V1 mock 联调验证失败: service.previewCartPromotions is not a function`
- `L2-SUBMIT-FLOW` [P0] Submit order and anti-tamper flow: core user journey failed: checkout unexpected errno=412, status=200, errmsg=请先完善登录资料
  - repro_step: run `python3 testing/scripts/core_user_journey.py --base-url http://127.0.0.1:8360 --api-jwt-secret bae4fdabcc11cba5bb4aa9225bdbda8a936b41d729e86a65f44c02313d839278 --api-user-id 1 --db-host 127.0.0.1 --db-port 3306 --db-user root --db-password CHANGE_ME_STRONG_PASSWORD --db-name hiolabsDB`
  - evidence: `core user journey failed: checkout unexpected errno=412, status=200, errmsg=请先完善登录资料`
- `NIGHTLY-NOTIFY-CONCURRENCY` [P0] Pay notify concurrency and idempotency consistency: RuntimeError: notify failures: ['OK', 'OK', 'OK']
  - repro_step: run `python3 testing/scripts/pay_notify_concurrency.py --base-url http://127.0.0.1:8360 --workers 8 --user-id 1 --api-jwt-secret bae4fdabcc11cba5bb4aa9225bdbda8a936b41d729e86a65f44c02313d839278 --db-host 127.0.0.1 --db-port 3306 --db-user root --db-password CHANGE_ME_STRONG_PASSWORD --db-name hiolabsDB`
  - evidence: `Traceback (most recent call last):
  File "/Volumes/SAMSUNG/fyb/myProjects/testing/scripts/pay_notify_concurrency.py", line 383, in <module>
    raise SystemExit(main())
                     ~~~~^^
  File "/Volumes/SAMSUNG/fyb/myProjects/testing/scripts/pay_notify_concurrency.py", line 362, in main
    raise RuntimeError(f"notify failures: {samples}")
RuntimeError: notify failures: ['OK', 'OK', 'OK']`
- `L1-CORE-PAY` [P1] Pay core contract responses: mapped_actions=1, failed=1, skipped=0
- `L2-HOME-PAGE` [P1] Home page load and popup/channel visibility: request error: Expecting value: line 1 column 1 (char 0)
  - repro_step: run `GET /api/index/index + GET /api/index/appInfo`
- `L3-CROSS-END-SUITE` [P1] Cross-end suite runtime: ad create unexpected errno=100, status=200, errmsg=该商品已经有广告关联
- `L3-ORDER-OPS-CROSS-END` [P1] Admin order memo/status -> mini order detail consistency: blocked by cross-end suite runtime error: ad create unexpected errno=100, status=200, errmsg=该商品已经有广告关联
- `L1-FULL-ADMIN-ACTIONS` [P2] All Admin actions contract probing: actions=186, failed=68, skipped=0
- `L1-FULL-ADMIN-ACTIONS::admin.showsetStore` [P2] Admin contract admin.showsetStore: status=500 server error
  - repro_step: run `GET /admin/admin/showsetStore`
  - evidence: `<!DOCTYPE html>
<html>
<head>
	<meta charset="utf-8">
	<title>Internal Server Error - ThinkJS</title>
	<style>
	
		body,code,dd,div,dl,dt,h1,h2,h3,h4,h5,h6,li,pre,ul{margin:0;padding:0}a{text-decoration:none}.clearfix{clear:both;zoom:1}.clearfix:after{clear:both;content:"";display:block;height:0;vis`
- `L1-FULL-ADMIN-ACTIONS::admin.store` [P2] Admin contract admin.store: status=500 server error
  - repro_step: run `POST /admin/admin/store`
  - evidence: `<!DOCTYPE html>
<html>
<head>
	<meta charset="utf-8">
	<title>Internal Server Error - ThinkJS</title>
	<style>
	
		body,code,dd,div,dl,dt,h1,h2,h3,h4,h5,h6,li,pre,ul{margin:0;padding:0}a{text-decoration:none}.clearfix{clear:both;zoom:1}.clearfix:after{clear:both;content:"";display:block;height:0;vis`
- `L1-FULL-ADMIN-ACTIONS::category.categoryStatus` [P2] Admin contract category.categoryStatus: status=500 server error
  - repro_step: run `POST /admin/category/categoryStatus`
  - evidence: `<!DOCTYPE html>
<html>
<head>
	<meta charset="utf-8">
	<title>Internal Server Error - ThinkJS</title>
	<style>
	
		body,code,dd,div,dl,dt,h1,h2,h3,h4,h5,h6,li,pre,ul{margin:0;padding:0}a{text-decoration:none}.clearfix{clear:both;zoom:1}.clearfix:after{clear:both;content:"";display:block;height:0;vis`
- `L1-FULL-ADMIN-ACTIONS::category.channelStatus` [P2] Admin contract category.channelStatus: status=500 server error
  - repro_step: run `POST /admin/category/channelStatus`
  - evidence: `<!DOCTYPE html>
<html>
<head>
	<meta charset="utf-8">
	<title>Internal Server Error - ThinkJS</title>
	<style>
	
		body,code,dd,div,dl,dt,h1,h2,h3,h4,h5,h6,li,pre,ul{margin:0;padding:0}a{text-decoration:none}.clearfix{clear:both;zoom:1}.clearfix:after{clear:both;content:"";display:block;height:0;vis`
- `L1-FULL-ADMIN-ACTIONS::category.showStatus` [P2] Admin contract category.showStatus: status=200 non-json response
  - repro_step: run `GET /admin/category/showStatus`
  - evidence: `OK`
- `L1-FULL-ADMIN-ACTIONS::category.store` [P2] Admin contract category.store: status=500 server error
  - repro_step: run `POST /admin/category/store`
  - evidence: `<!DOCTYPE html>
<html>
<head>
	<meta charset="utf-8">
	<title>Internal Server Error - ThinkJS</title>
	<style>
	
		body,code,dd,div,dl,dt,h1,h2,h3,h4,h5,h6,li,pre,ul{margin:0;padding:0}a{text-decoration:none}.clearfix{clear:both;zoom:1}.clearfix:after{clear:both;content:"";display:block;height:0;vis`
- `L1-FULL-ADMIN-ACTIONS::goods.checkSku` [P2] Admin contract goods.checkSku: status=500 server error
  - repro_step: run `GET /admin/goods/checkSku`
  - evidence: `<!DOCTYPE html>
<html>
<head>
	<meta charset="utf-8">
	<title>Internal Server Error - ThinkJS</title>
	<style>
	
		body,code,dd,div,dl,dt,h1,h2,h3,h4,h5,h6,li,pre,ul{margin:0;padding:0}a{text-decoration:none}.clearfix{clear:both;zoom:1}.clearfix:after{clear:both;content:"";display:block;height:0;vis`
- `L1-FULL-ADMIN-ACTIONS::goods.copygoods` [P2] Admin contract goods.copygoods: status=500 server error
  - repro_step: run `POST /admin/goods/copygoods`
  - evidence: `<!DOCTYPE html>
<html>
<head>
	<meta charset="utf-8">
	<title>Internal Server Error - ThinkJS</title>
	<style>
	
		body,code,dd,div,dl,dt,h1,h2,h3,h4,h5,h6,li,pre,ul{margin:0;padding:0}a{text-decoration:none}.clearfix{clear:both;zoom:1}.clearfix:after{clear:both;content:"";display:block;height:0;vis`
- `L1-FULL-ADMIN-ACTIONS::goods.gallery` [P2] Admin contract goods.gallery: status=500 server error
  - repro_step: run `POST /admin/goods/gallery`
  - evidence: `<!DOCTYPE html>
<html>
<head>
	<meta charset="utf-8">
	<title>Internal Server Error - ThinkJS</title>
	<style>
	
		body,code,dd,div,dl,dt,h1,h2,h3,h4,h5,h6,li,pre,ul{margin:0;padding:0}a{text-decoration:none}.clearfix{clear:both;zoom:1}.clearfix:after{clear:both;content:"";display:block;height:0;vis`
- `L1-FULL-ADMIN-ACTIONS::goods.galleryEdit` [P2] Admin contract goods.galleryEdit: status=500 server error
  - repro_step: run `POST /admin/goods/galleryEdit`
  - evidence: `<!DOCTYPE html>
<html>
<head>
	<meta charset="utf-8">
	<title>Internal Server Error - ThinkJS</title>
	<style>
	
		body,code,dd,div,dl,dt,h1,h2,h3,h4,h5,h6,li,pre,ul{margin:0;padding:0}a{text-decoration:none}.clearfix{clear:both;zoom:1}.clearfix:after{clear:both;content:"";display:block;height:0;vis`
- `L1-FULL-ADMIN-ACTIONS::goods.galleryList` [P2] Admin contract goods.galleryList: status=500 server error
  - repro_step: run `POST /admin/goods/galleryList`
  - evidence: `<!DOCTYPE html>
<html>
<head>
	<meta charset="utf-8">
	<title>Internal Server Error - ThinkJS</title>
	<style>
	
		body,code,dd,div,dl,dt,h1,h2,h3,h4,h5,h6,li,pre,ul{margin:0;padding:0}a{text-decoration:none}.clearfix{clear:both;zoom:1}.clearfix:after{clear:both;content:"";display:block;height:0;vis`
- `L1-FULL-ADMIN-ACTIONS::goods.getGalleryList` [P2] Admin contract goods.getGalleryList: status=500 server error
  - repro_step: run `GET /admin/goods/getGalleryList`
  - evidence: `<!DOCTYPE html>
<html>
<head>
	<meta charset="utf-8">
	<title>Internal Server Error - ThinkJS</title>
	<style>
	
		body,code,dd,div,dl,dt,h1,h2,h3,h4,h5,h6,li,pre,ul{margin:0;padding:0}a{text-decoration:none}.clearfix{clear:both;zoom:1}.clearfix:after{clear:both;content:"";display:block;height:0;vis`
- `L1-FULL-ADMIN-ACTIONS::goods.indexShowStatus` [P2] Admin contract goods.indexShowStatus: status=200 non-json response
  - repro_step: run `GET /admin/goods/indexShowStatus`
  - evidence: `OK`
- `L1-FULL-ADMIN-ACTIONS::goods.productStatus` [P2] Admin contract goods.productStatus: status=500 server error
  - repro_step: run `POST /admin/goods/productStatus`
  - evidence: `<!DOCTYPE html>
<html>
<head>
	<meta charset="utf-8">
	<title>Internal Server Error - ThinkJS</title>
	<style>
	
		body,code,dd,div,dl,dt,h1,h2,h3,h4,h5,h6,li,pre,ul{margin:0;padding:0}a{text-decoration:none}.clearfix{clear:both;zoom:1}.clearfix:after{clear:both;content:"";display:block;height:0;vis`
- `L1-FULL-ADMIN-ACTIONS::goods.saleStatus` [P2] Admin contract goods.saleStatus: status=500 server error
  - repro_step: run `POST /admin/goods/saleStatus`
  - evidence: `<!DOCTYPE html>
<html>
<head>
	<meta charset="utf-8">
	<title>Internal Server Error - ThinkJS</title>
	<style>
	
		body,code,dd,div,dl,dt,h1,h2,h3,h4,h5,h6,li,pre,ul{margin:0;padding:0}a{text-decoration:none}.clearfix{clear:both;zoom:1}.clearfix:after{clear:both;content:"";display:block;height:0;vis`
- `L1-FULL-ADMIN-ACTIONS::goods.sort` [P2] Admin contract goods.sort: status=200 non-json response
  - repro_step: run `POST /admin/goods/sort`
  - evidence: `OK`
- `L1-FULL-ADMIN-ACTIONS::goods.store` [P2] Admin contract goods.store: status=500 server error
  - repro_step: run `POST /admin/goods/store`
  - evidence: `<!DOCTYPE html>
<html>
<head>
	<meta charset="utf-8">
	<title>Internal Server Error - ThinkJS</title>
	<style>
	
		body,code,dd,div,dl,dt,h1,h2,h3,h4,h5,h6,li,pre,ul{margin:0;padding:0}a{text-decoration:none}.clearfix{clear:both;zoom:1}.clearfix:after{clear:both;content:"";display:block;height:0;vis`
- `L1-FULL-ADMIN-ACTIONS::goods.updateGoodsNumber` [P2] Admin contract goods.updateGoodsNumber: request error: HTTPConnectionPool(host='127.0.0.1', port=8360): Read timed out. (read timeout=20)
  - repro_step: run `POST /admin/goods/updateGoodsNumber`
- `L1-FULL-ADMIN-ACTIONS::goods.updatePrice` [P2] Admin contract goods.updatePrice: status=500 server error
  - repro_step: run `POST /admin/goods/updatePrice`
  - evidence: `<!DOCTYPE html>
<html>
<head>
	<meta charset="utf-8">
	<title>Internal Server Error - ThinkJS</title>
	<style>
	
		body,code,dd,div,dl,dt,h1,h2,h3,h4,h5,h6,li,pre,ul{margin:0;padding:0}a{text-decoration:none}.clearfix{clear:both;zoom:1}.clearfix:after{clear:both;content:"";display:block;height:0;vis`
- `L1-FULL-ADMIN-ACTIONS::goods.updateShortName` [P2] Admin contract goods.updateShortName: status=500 server error
  - repro_step: run `POST /admin/goods/updateShortName`
  - evidence: `<!DOCTYPE html>
<html>
<head>
	<meta charset="utf-8">
	<title>Internal Server Error - ThinkJS</title>
	<style>
	
		body,code,dd,div,dl,dt,h1,h2,h3,h4,h5,h6,li,pre,ul{margin:0;padding:0}a{text-decoration:none}.clearfix{clear:both;zoom:1}.clearfix:after{clear:both;content:"";display:block;height:0;vis`
- `L1-FULL-ADMIN-ACTIONS::notice.updateContent` [P2] Admin contract notice.updateContent: status=500 server error
  - repro_step: run `POST /admin/notice/updateContent`
  - evidence: `<!DOCTYPE html>
<html>
<head>
	<meta charset="utf-8">
	<title>Internal Server Error - ThinkJS</title>
	<style>
	
		body,code,dd,div,dl,dt,h1,h2,h3,h4,h5,h6,li,pre,ul{margin:0;padding:0}a{text-decoration:none}.clearfix{clear:both;zoom:1}.clearfix:after{clear:both;content:"";display:block;height:0;vis`
- `L1-FULL-ADMIN-ACTIONS::order.changeStatus` [P2] Admin contract order.changeStatus: status=500 server error
  - repro_step: run `POST /admin/order/changeStatus`
  - evidence: `<!DOCTYPE html>
<html>
<head>
	<meta charset="utf-8">
	<title>Internal Server Error - ThinkJS</title>
	<style>
	
		body,code,dd,div,dl,dt,h1,h2,h3,h4,h5,h6,li,pre,ul{margin:0;padding:0}a{text-decoration:none}.clearfix{clear:both;zoom:1}.clearfix:after{clear:both;content:"";display:block;height:0;vis`
- `L1-FULL-ADMIN-ACTIONS::order.detail` [P2] Admin contract order.detail: status=500 server error
  - repro_step: run `GET /admin/order/detail`
  - evidence: `<!DOCTYPE html>
<html>
<head>
	<meta charset="utf-8">
	<title>Internal Server Error - ThinkJS</title>
	<style>
	
		body,code,dd,div,dl,dt,h1,h2,h3,h4,h5,h6,li,pre,ul{margin:0;padding:0}a{text-decoration:none}.clearfix{clear:both;zoom:1}.clearfix:after{clear:both;content:"";display:block;height:0;vis`
- `L1-FULL-ADMIN-ACTIONS::order.directPrintExpress` [P2] Admin contract order.directPrintExpress: status=500 server error
  - repro_step: run `POST /admin/order/directPrintExpress`
  - evidence: `<!DOCTYPE html>
<html>
<head>
	<meta charset="utf-8">
	<title>Internal Server Error - ThinkJS</title>
	<style>
	
		body,code,dd,div,dl,dt,h1,h2,h3,h4,h5,h6,li,pre,ul{margin:0;padding:0}a{text-decoration:none}.clearfix{clear:both;zoom:1}.clearfix:after{clear:both;content:"";display:block;height:0;vis`
- `L1-FULL-ADMIN-ACTIONS::order.getGoodsSpecification` [P2] Admin contract order.getGoodsSpecification: status=500 server error
  - repro_step: run `GET /admin/order/getGoodsSpecification`
  - evidence: `<!DOCTYPE html>
<html>
<head>
	<meta charset="utf-8">
	<title>Internal Server Error - ThinkJS</title>
	<style>
	
		body,code,dd,div,dl,dt,h1,h2,h3,h4,h5,h6,li,pre,ul{margin:0;padding:0}a{text-decoration:none}.clearfix{clear:both;zoom:1}.clearfix:after{clear:both;content:"";display:block;height:0;vis`
- `L1-FULL-ADMIN-ACTIONS::order.getMianExpress` [P2] Admin contract order.getMianExpress: status=500 server error
  - repro_step: run `GET /admin/order/getMianExpress`
  - evidence: `<!DOCTYPE html>
<html>
<head>
	<meta charset="utf-8">
	<title>Internal Server Error - ThinkJS</title>
	<style>
	
		body,code,dd,div,dl,dt,h1,h2,h3,h4,h5,h6,li,pre,ul{margin:0;padding:0}a{text-decoration:none}.clearfix{clear:both;zoom:1}.clearfix:after{clear:both;content:"";display:block;height:0;vis`
- `L1-FULL-ADMIN-ACTIONS::order.getOrderExpress` [P2] Admin contract order.getOrderExpress: status=500 server error
  - repro_step: run `GET /admin/order/getOrderExpress`
  - evidence: `<!DOCTYPE html>
<html>
<head>
	<meta charset="utf-8">
	<title>Internal Server Error - ThinkJS</title>
	<style>
	
		body,code,dd,div,dl,dt,h1,h2,h3,h4,h5,h6,li,pre,ul{margin:0;padding:0}a{text-decoration:none}.clearfix{clear:both;zoom:1}.clearfix:after{clear:both;content:"";display:block;height:0;vis`
- `L1-FULL-ADMIN-ACTIONS::order.goDelivery` [P2] Admin contract order.goDelivery: status=500 server error
  - repro_step: run `POST /admin/order/goDelivery`
  - evidence: `<!DOCTYPE html>
<html>
<head>
	<meta charset="utf-8">
	<title>Internal Server Error - ThinkJS</title>
	<style>
	
		body,code,dd,div,dl,dt,h1,h2,h3,h4,h5,h6,li,pre,ul{margin:0;padding:0}a{text-decoration:none}.clearfix{clear:both;zoom:1}.clearfix:after{clear:both;content:"";display:block;height:0;vis`
- `L1-FULL-ADMIN-ACTIONS::order.goodsListDelete` [P2] Admin contract order.goodsListDelete: status=500 server error
  - repro_step: run `POST /admin/order/goodsListDelete`
  - evidence: `<!DOCTYPE html>
<html>
<head>
	<meta charset="utf-8">
	<title>Internal Server Error - ThinkJS</title>
	<style>
	
		body,code,dd,div,dl,dt,h1,h2,h3,h4,h5,h6,li,pre,ul{margin:0;padding:0}a{text-decoration:none}.clearfix{clear:both;zoom:1}.clearfix:after{clear:both;content:"";display:block;height:0;vis`
- `L1-FULL-ADMIN-ACTIONS::order.orderDelivery` [P2] Admin contract order.orderDelivery: status=500 server error
  - repro_step: run `POST /admin/order/orderDelivery`
  - evidence: `<!DOCTYPE html>
<html>
<head>
	<meta charset="utf-8">
	<title>Internal Server Error - ThinkJS</title>
	<style>
	
		body,code,dd,div,dl,dt,h1,h2,h3,h4,h5,h6,li,pre,ul{margin:0;padding:0}a{text-decoration:none}.clearfix{clear:both;zoom:1}.clearfix:after{clear:both;content:"";display:block;height:0;vis`
- `L1-FULL-ADMIN-ACTIONS::order.orderPrice` [P2] Admin contract order.orderPrice: status=500 server error
  - repro_step: run `POST /admin/order/orderPrice`
  - evidence: `<!DOCTYPE html>
<html>
<head>
	<meta charset="utf-8">
	<title>Internal Server Error - ThinkJS</title>
	<style>
	
		body,code,dd,div,dl,dt,h1,h2,h3,h4,h5,h6,li,pre,ul{margin:0;padding:0}a{text-decoration:none}.clearfix{clear:both;zoom:1}.clearfix:after{clear:both;content:"";display:block;height:0;vis`
- `L1-FULL-ADMIN-ACTIONS::order.orderReceive` [P2] Admin contract order.orderReceive: status=500 server error
  - repro_step: run `POST /admin/order/orderReceive`
  - evidence: `<!DOCTYPE html>
<html>
<head>
	<meta charset="utf-8">
	<title>Internal Server Error - ThinkJS</title>
	<style>
	
		body,code,dd,div,dl,dt,h1,h2,h3,h4,h5,h6,li,pre,ul{margin:0;padding:0}a{text-decoration:none}.clearfix{clear:both;zoom:1}.clearfix:after{clear:both;content:"";display:block;height:0;vis`
- `L1-FULL-ADMIN-ACTIONS::order.orderpack` [P2] Admin contract order.orderpack: status=500 server error
  - repro_step: run `POST /admin/order/orderpack`
  - evidence: `<!DOCTYPE html>
<html>
<head>
	<meta charset="utf-8">
	<title>Internal Server Error - ThinkJS</title>
	<style>
	
		body,code,dd,div,dl,dt,h1,h2,h3,h4,h5,h6,li,pre,ul{margin:0;padding:0}a{text-decoration:none}.clearfix{clear:both;zoom:1}.clearfix:after{clear:both;content:"";display:block;height:0;vis`
- `L1-FULL-ADMIN-ACTIONS::order.rePrintExpress` [P2] Admin contract order.rePrintExpress: status=500 server error
  - repro_step: run `POST /admin/order/rePrintExpress`
  - evidence: `<!DOCTYPE html>
<html>
<head>
	<meta charset="utf-8">
	<title>Internal Server Error - ThinkJS</title>
	<style>
	
		body,code,dd,div,dl,dt,h1,h2,h3,h4,h5,h6,li,pre,ul{margin:0;padding:0}a{text-decoration:none}.clearfix{clear:both;zoom:1}.clearfix:after{clear:both;content:"";display:block;height:0;vis`
- `L1-FULL-ADMIN-ACTIONS::order.saveAddress` [P2] Admin contract order.saveAddress: status=500 server error
  - repro_step: run `POST /admin/order/saveAddress`
  - evidence: `<!DOCTYPE html>
<html>
<head>
	<meta charset="utf-8">
	<title>Internal Server Error - ThinkJS</title>
	<style>
	
		body,code,dd,div,dl,dt,h1,h2,h3,h4,h5,h6,li,pre,ul{margin:0;padding:0}a{text-decoration:none}.clearfix{clear:both;zoom:1}.clearfix:after{clear:both;content:"";display:block;height:0;vis`
- `L1-FULL-ADMIN-ACTIONS::order.saveAdminMemo` [P2] Admin contract order.saveAdminMemo: status=500 server error
  - repro_step: run `POST /admin/order/saveAdminMemo`
  - evidence: `<!DOCTYPE html>
<html>
<head>
	<meta charset="utf-8">
	<title>Internal Server Error - ThinkJS</title>
	<style>
	
		body,code,dd,div,dl,dt,h1,h2,h3,h4,h5,h6,li,pre,ul{margin:0;padding:0}a{text-decoration:none}.clearfix{clear:both;zoom:1}.clearfix:after{clear:both;content:"";display:block;height:0;vis`
- `L1-FULL-ADMIN-ACTIONS::order.saveExpressValueInfo` [P2] Admin contract order.saveExpressValueInfo: status=500 server error
  - repro_step: run `POST /admin/order/saveExpressValueInfo`
  - evidence: `<!DOCTYPE html>
<html>
<head>
	<meta charset="utf-8">
	<title>Internal Server Error - ThinkJS</title>
	<style>
	
		body,code,dd,div,dl,dt,h1,h2,h3,h4,h5,h6,li,pre,ul{margin:0;padding:0}a{text-decoration:none}.clearfix{clear:both;zoom:1}.clearfix:after{clear:both;content:"";display:block;height:0;vis`
- `L1-FULL-ADMIN-ACTIONS::order.saveGoodsList` [P2] Admin contract order.saveGoodsList: status=200 non-json response
  - repro_step: run `POST /admin/order/saveGoodsList`
  - evidence: `OK`
- `L1-FULL-ADMIN-ACTIONS::order.savePrintInfo` [P2] Admin contract order.savePrintInfo: status=500 server error
  - repro_step: run `POST /admin/order/savePrintInfo`
  - evidence: `<!DOCTYPE html>
<html>
<head>
	<meta charset="utf-8">
	<title>Internal Server Error - ThinkJS</title>
	<style>
	
		body,code,dd,div,dl,dt,h1,h2,h3,h4,h5,h6,li,pre,ul{margin:0;padding:0}a{text-decoration:none}.clearfix{clear:both;zoom:1}.clearfix:after{clear:both;content:"";display:block;height:0;vis`
- `L1-FULL-ADMIN-ACTIONS::order.saveRemarkInfo` [P2] Admin contract order.saveRemarkInfo: status=500 server error
  - repro_step: run `POST /admin/order/saveRemarkInfo`
  - evidence: `<!DOCTYPE html>
<html>
<head>
	<meta charset="utf-8">
	<title>Internal Server Error - ThinkJS</title>
	<style>
	
		body,code,dd,div,dl,dt,h1,h2,h3,h4,h5,h6,li,pre,ul{margin:0;padding:0}a{text-decoration:none}.clearfix{clear:both;zoom:1}.clearfix:after{clear:both;content:"";display:block;height:0;vis`
- `L1-FULL-ADMIN-ACTIONS::order.store` [P2] Admin contract order.store: status=500 server error
  - repro_step: run `POST /admin/order/store`
  - evidence: `<!DOCTYPE html>
<html>
<head>
	<meta charset="utf-8">
	<title>Internal Server Error - ThinkJS</title>
	<style>
	
		body,code,dd,div,dl,dt,h1,h2,h3,h4,h5,h6,li,pre,ul{margin:0;padding:0}a{text-decoration:none}.clearfix{clear:both;zoom:1}.clearfix:after{clear:both;content:"";display:block;height:0;vis`
- `L1-FULL-ADMIN-ACTIONS::shipper.addExceptArea` [P2] Admin contract shipper.addExceptArea: status=500 server error
  - repro_step: run `POST /admin/shipper/addExceptArea`
  - evidence: `<!DOCTYPE html>
<html>
<head>
	<meta charset="utf-8">
	<title>Internal Server Error - ThinkJS</title>
	<style>
	
		body,code,dd,div,dl,dt,h1,h2,h3,h4,h5,h6,li,pre,ul{margin:0;padding:0}a{text-decoration:none}.clearfix{clear:both;zoom:1}.clearfix:after{clear:both;content:"";display:block;height:0;vis`
- `L1-FULL-ADMIN-ACTIONS::shipper.addTable` [P2] Admin contract shipper.addTable: status=500 server error
  - repro_step: run `POST /admin/shipper/addTable`
  - evidence: `<!DOCTYPE html>
<html>
<head>
	<meta charset="utf-8">
	<title>Internal Server Error - ThinkJS</title>
	<style>
	
		body,code,dd,div,dl,dt,h1,h2,h3,h4,h5,h6,li,pre,ul{margin:0;padding:0}a{text-decoration:none}.clearfix{clear:both;zoom:1}.clearfix:after{clear:both;content:"";display:block;height:0;vis`
- `L1-FULL-ADMIN-ACTIONS::shipper.enabledStatus` [P2] Admin contract shipper.enabledStatus: status=500 server error
  - repro_step: run `POST /admin/shipper/enabledStatus`
  - evidence: `<!DOCTYPE html>
<html>
<head>
	<meta charset="utf-8">
	<title>Internal Server Error - ThinkJS</title>
	<style>
	
		body,code,dd,div,dl,dt,h1,h2,h3,h4,h5,h6,li,pre,ul{margin:0;padding:0}a{text-decoration:none}.clearfix{clear:both;zoom:1}.clearfix:after{clear:both;content:"";display:block;height:0;vis`
- `L1-FULL-ADMIN-ACTIONS::shipper.exceptAreaDetail` [P2] Admin contract shipper.exceptAreaDetail: status=500 server error
  - repro_step: run `POST /admin/shipper/exceptAreaDetail`
  - evidence: `<!DOCTYPE html>
<html>
<head>
	<meta charset="utf-8">
	<title>Internal Server Error - ThinkJS</title>
	<style>
	
		body,code,dd,div,dl,dt,h1,h2,h3,h4,h5,h6,li,pre,ul{margin:0;padding:0}a{text-decoration:none}.clearfix{clear:both;zoom:1}.clearfix:after{clear:both;content:"";display:block;height:0;vis`
- `L1-FULL-ADMIN-ACTIONS::shipper.saveExceptArea` [P2] Admin contract shipper.saveExceptArea: status=500 server error
  - repro_step: run `POST /admin/shipper/saveExceptArea`
  - evidence: `<!DOCTYPE html>
<html>
<head>
	<meta charset="utf-8">
	<title>Internal Server Error - ThinkJS</title>
	<style>
	
		body,code,dd,div,dl,dt,h1,h2,h3,h4,h5,h6,li,pre,ul{margin:0;padding:0}a{text-decoration:none}.clearfix{clear:both;zoom:1}.clearfix:after{clear:both;content:"";display:block;height:0;vis`
- `L1-FULL-ADMIN-ACTIONS::shipper.saveTable` [P2] Admin contract shipper.saveTable: status=500 server error
  - repro_step: run `POST /admin/shipper/saveTable`
  - evidence: `<!DOCTYPE html>
<html>
<head>
	<meta charset="utf-8">
	<title>Internal Server Error - ThinkJS</title>
	<style>
	
		body,code,dd,div,dl,dt,h1,h2,h3,h4,h5,h6,li,pre,ul{margin:0;padding:0}a{text-decoration:none}.clearfix{clear:both;zoom:1}.clearfix:after{clear:both;content:"";display:block;height:0;vis`
- `L1-FULL-ADMIN-ACTIONS::specification.checkSn` [P2] Admin contract specification.checkSn: status=500 server error
  - repro_step: run `GET /admin/specification/checkSn`
  - evidence: `<!DOCTYPE html>
<html>
<head>
	<meta charset="utf-8">
	<title>Internal Server Error - ThinkJS</title>
	<style>
	
		body,code,dd,div,dl,dt,h1,h2,h3,h4,h5,h6,li,pre,ul{margin:0;padding:0}a{text-decoration:none}.clearfix{clear:both;zoom:1}.clearfix:after{clear:both;content:"";display:block;height:0;vis`
- `L1-FULL-ADMIN-ACTIONS::specification.detail` [P2] Admin contract specification.detail: status=500 server error
  - repro_step: run `GET /admin/specification/detail`
  - evidence: `<!DOCTYPE html>
<html>
<head>
	<meta charset="utf-8">
	<title>Internal Server Error - ThinkJS</title>
	<style>
	
		body,code,dd,div,dl,dt,h1,h2,h3,h4,h5,h6,li,pre,ul{margin:0;padding:0}a{text-decoration:none}.clearfix{clear:both;zoom:1}.clearfix:after{clear:both;content:"";display:block;height:0;vis`
- `L1-FULL-ADMIN-ACTIONS::specification.getGoodsSpec` [P2] Admin contract specification.getGoodsSpec: status=500 server error
  - repro_step: run `GET /admin/specification/getGoodsSpec`
  - evidence: `<!DOCTYPE html>
<html>
<head>
	<meta charset="utf-8">
	<title>Internal Server Error - ThinkJS</title>
	<style>
	
		body,code,dd,div,dl,dt,h1,h2,h3,h4,h5,h6,li,pre,ul{margin:0;padding:0}a{text-decoration:none}.clearfix{clear:both;zoom:1}.clearfix:after{clear:both;content:"";display:block;height:0;vis`
- `L1-FULL-ADMIN-ACTIONS::specification.productDele` [P2] Admin contract specification.productDele: status=500 server error
  - repro_step: run `POST /admin/specification/productDele`
  - evidence: `<!DOCTYPE html>
<html>
<head>
	<meta charset="utf-8">
	<title>Internal Server Error - ThinkJS</title>
	<style>
	
		body,code,dd,div,dl,dt,h1,h2,h3,h4,h5,h6,li,pre,ul{margin:0;padding:0}a{text-decoration:none}.clearfix{clear:both;zoom:1}.clearfix:after{clear:both;content:"";display:block;height:0;vis`
- `L1-FULL-ADMIN-ACTIONS::specification.productUpdate` [P2] Admin contract specification.productUpdate: status=500 server error
  - repro_step: run `POST /admin/specification/productUpdate`
  - evidence: `<!DOCTYPE html>
<html>
<head>
	<meta charset="utf-8">
	<title>Internal Server Error - ThinkJS</title>
	<style>
	
		body,code,dd,div,dl,dt,h1,h2,h3,h4,h5,h6,li,pre,ul{margin:0;padding:0}a{text-decoration:none}.clearfix{clear:both;zoom:1}.clearfix:after{clear:both;content:"";display:block;height:0;vis`
- `L1-FULL-ADMIN-ACTIONS::user.address` [P2] Admin contract user.address: status=500 server error
  - repro_step: run `POST /admin/user/address`
  - evidence: `<!DOCTYPE html>
<html>
<head>
	<meta charset="utf-8">
	<title>Internal Server Error - ThinkJS</title>
	<style>
	
		body,code,dd,div,dl,dt,h1,h2,h3,h4,h5,h6,li,pre,ul{margin:0;padding:0}a{text-decoration:none}.clearfix{clear:both;zoom:1}.clearfix:after{clear:both;content:"";display:block;height:0;vis`
- `L1-FULL-ADMIN-ACTIONS::user.cartdata` [P2] Admin contract user.cartdata: status=500 server error
  - repro_step: run `POST /admin/user/cartdata`
  - evidence: `<!DOCTYPE html>
<html>
<head>
	<meta charset="utf-8">
	<title>Internal Server Error - ThinkJS</title>
	<style>
	
		body,code,dd,div,dl,dt,h1,h2,h3,h4,h5,h6,li,pre,ul{margin:0;padding:0}a{text-decoration:none}.clearfix{clear:both;zoom:1}.clearfix:after{clear:both;content:"";display:block;height:0;vis`
- `L1-FULL-ADMIN-ACTIONS::user.datainfo` [P2] Admin contract user.datainfo: status=500 server error
  - repro_step: run `POST /admin/user/datainfo`
  - evidence: `<!DOCTYPE html>
<html>
<head>
	<meta charset="utf-8">
	<title>Internal Server Error - ThinkJS</title>
	<style>
	
		body,code,dd,div,dl,dt,h1,h2,h3,h4,h5,h6,li,pre,ul{margin:0;padding:0}a{text-decoration:none}.clearfix{clear:both;zoom:1}.clearfix:after{clear:both;content:"";display:block;height:0;vis`
- `L1-FULL-ADMIN-ACTIONS::user.foot` [P2] Admin contract user.foot: status=500 server error
  - repro_step: run `POST /admin/user/foot`
  - evidence: `<!DOCTYPE html>
<html>
<head>
	<meta charset="utf-8">
	<title>Internal Server Error - ThinkJS</title>
	<style>
	
		body,code,dd,div,dl,dt,h1,h2,h3,h4,h5,h6,li,pre,ul{margin:0;padding:0}a{text-decoration:none}.clearfix{clear:both;zoom:1}.clearfix:after{clear:both;content:"";display:block;height:0;vis`
- `L1-FULL-ADMIN-ACTIONS::user.info` [P2] Admin contract user.info: status=500 server error
  - repro_step: run `GET /admin/user/info`
  - evidence: `<!DOCTYPE html>
<html>
<head>
	<meta charset="utf-8">
	<title>Internal Server Error - ThinkJS</title>
	<style>
	
		body,code,dd,div,dl,dt,h1,h2,h3,h4,h5,h6,li,pre,ul{margin:0;padding:0}a{text-decoration:none}.clearfix{clear:both;zoom:1}.clearfix:after{clear:both;content:"";display:block;height:0;vis`
- `L1-FULL-ADMIN-ACTIONS::user.order` [P2] Admin contract user.order: status=500 server error
  - repro_step: run `POST /admin/user/order`
  - evidence: `<!DOCTYPE html>
<html>
<head>
	<meta charset="utf-8">
	<title>Internal Server Error - ThinkJS</title>
	<style>
	
		body,code,dd,div,dl,dt,h1,h2,h3,h4,h5,h6,li,pre,ul{margin:0;padding:0}a{text-decoration:none}.clearfix{clear:both;zoom:1}.clearfix:after{clear:both;content:"";display:block;height:0;vis`
- `L1-FULL-ADMIN-ACTIONS::user.saveaddress` [P2] Admin contract user.saveaddress: status=500 server error
  - repro_step: run `POST /admin/user/saveaddress`
  - evidence: `<!DOCTYPE html>
<html>
<head>
	<meta charset="utf-8">
	<title>Internal Server Error - ThinkJS</title>
	<style>
	
		body,code,dd,div,dl,dt,h1,h2,h3,h4,h5,h6,li,pre,ul{margin:0;padding:0}a{text-decoration:none}.clearfix{clear:both;zoom:1}.clearfix:after{clear:both;content:"";display:block;height:0;vis`
- `L1-FULL-ADMIN-ACTIONS::user.store` [P2] Admin contract user.store: status=500 server error
  - repro_step: run `POST /admin/user/store`
  - evidence: `<!DOCTYPE html>
<html>
<head>
	<meta charset="utf-8">
	<title>Internal Server Error - ThinkJS</title>
	<style>
	
		body,code,dd,div,dl,dt,h1,h2,h3,h4,h5,h6,li,pre,ul{margin:0;padding:0}a{text-decoration:none}.clearfix{clear:both;zoom:1}.clearfix:after{clear:both;content:"";display:block;height:0;vis`
- `L1-FULL-ADMIN-ACTIONS::user.updateInfo` [P2] Admin contract user.updateInfo: status=500 server error
  - repro_step: run `POST /admin/user/updateInfo`
  - evidence: `<!DOCTYPE html>
<html>
<head>
	<meta charset="utf-8">
	<title>Internal Server Error - ThinkJS</title>
	<style>
	
		body,code,dd,div,dl,dt,h1,h2,h3,h4,h5,h6,li,pre,ul{margin:0;padding:0}a{text-decoration:none}.clearfix{clear:both;zoom:1}.clearfix:after{clear:both;content:"";display:block;height:0;vis`
- `L1-FULL-ADMIN-ACTIONS::user.updateMobile` [P2] Admin contract user.updateMobile: status=500 server error
  - repro_step: run `POST /admin/user/updateMobile`
  - evidence: `<!DOCTYPE html>
<html>
<head>
	<meta charset="utf-8">
	<title>Internal Server Error - ThinkJS</title>
	<style>
	
		body,code,dd,div,dl,dt,h1,h2,h3,h4,h5,h6,li,pre,ul{margin:0;padding:0}a{text-decoration:none}.clearfix{clear:both;zoom:1}.clearfix:after{clear:both;content:"";display:block;height:0;vis`
- `L1-FULL-ADMIN-ACTIONS::wap.getGoodsSnName` [P2] Admin contract wap.getGoodsSnName: status=500 server error
  - repro_step: run `GET /admin/wap/getGoodsSnName`
  - evidence: `<!DOCTYPE html>
<html>
<head>
	<meta charset="utf-8">
	<title>Internal Server Error - ThinkJS</title>
	<style>
	
		body,code,dd,div,dl,dt,h1,h2,h3,h4,h5,h6,li,pre,ul{margin:0;padding:0}a{text-decoration:none}.clearfix{clear:both;zoom:1}.clearfix:after{clear:both;content:"";display:block;height:0;vis`
- `L1-FULL-ADMIN-ACTIONS::wap.info` [P2] Admin contract wap.info: status=500 server error
  - repro_step: run `GET /admin/wap/info`
  - evidence: `<!DOCTYPE html>
<html>
<head>
	<meta charset="utf-8">
	<title>Internal Server Error - ThinkJS</title>
	<style>
	
		body,code,dd,div,dl,dt,h1,h2,h3,h4,h5,h6,li,pre,ul{margin:0;padding:0}a{text-decoration:none}.clearfix{clear:both;zoom:1}.clearfix:after{clear:both;content:"";display:block;height:0;vis`
- `L1-FULL-ADMIN-ACTIONS::wap.saleStatus` [P2] Admin contract wap.saleStatus: status=500 server error
  - repro_step: run `POST /admin/wap/saleStatus`
  - evidence: `<!DOCTYPE html>
<html>
<head>
	<meta charset="utf-8">
	<title>Internal Server Error - ThinkJS</title>
	<style>
	
		body,code,dd,div,dl,dt,h1,h2,h3,h4,h5,h6,li,pre,ul{margin:0;padding:0}a{text-decoration:none}.clearfix{clear:both;zoom:1}.clearfix:after{clear:both;content:"";display:block;height:0;vis`
- `L1-FULL-ADMIN-ACTIONS::wap.sort` [P2] Admin contract wap.sort: status=200 non-json response
  - repro_step: run `POST /admin/wap/sort`
  - evidence: `OK`
- `L1-FULL-ADMIN-ACTIONS::wap.store` [P2] Admin contract wap.store: status=500 server error
  - repro_step: run `POST /admin/wap/store`
  - evidence: `<!DOCTYPE html>
<html>
<head>
	<meta charset="utf-8">
	<title>Internal Server Error - ThinkJS</title>
	<style>
	
		body,code,dd,div,dl,dt,h1,h2,h3,h4,h5,h6,li,pre,ul{margin:0;padding:0}a{text-decoration:none}.clearfix{clear:both;zoom:1}.clearfix:after{clear:both;content:"";display:block;height:0;vis`
- `L1-FULL-ADMIN-ACTIONS::wap.updatePrice` [P2] Admin contract wap.updatePrice: status=500 server error
  - repro_step: run `POST /admin/wap/updatePrice`
  - evidence: `<!DOCTYPE html>
<html>
<head>
	<meta charset="utf-8">
	<title>Internal Server Error - ThinkJS</title>
	<style>
	
		body,code,dd,div,dl,dt,h1,h2,h3,h4,h5,h6,li,pre,ul{margin:0;padding:0}a{text-decoration:none}.clearfix{clear:both;zoom:1}.clearfix:after{clear:both;content:"";display:block;height:0;vis`
- `L1-FULL-API-ACTIONS` [P2] All API actions contract probing: actions=68, failed=15, skipped=0
- `L1-FULL-API-ACTIONS::cart.checked` [P2] API contract cart.checked: status=500 server error
  - repro_step: run `GET /api/cart/checked`
  - evidence: `<!DOCTYPE html>
<html>
<head>
	<meta charset="utf-8">
	<title>Internal Server Error - ThinkJS</title>
	<style>
	
		body,code,dd,div,dl,dt,h1,h2,h3,h4,h5,h6,li,pre,ul{margin:0;padding:0}a{text-decoration:none}.clearfix{clear:both;zoom:1}.clearfix:after{clear:both;content:"";display:block;height:0;vis`
- `L1-FULL-API-ACTIONS::catalog.currentlist` [P2] API contract catalog.currentlist: status=500 server error
  - repro_step: run `GET /api/catalog/currentlist`
  - evidence: `<!DOCTYPE html>
<html>
<head>
	<meta charset="utf-8">
	<title>Internal Server Error - ThinkJS</title>
	<style>
	
		body,code,dd,div,dl,dt,h1,h2,h3,h4,h5,h6,li,pre,ul{margin:0;padding:0}a{text-decoration:none}.clearfix{clear:both;zoom:1}.clearfix:after{clear:both;content:"";display:block;height:0;vis`
- `L1-FULL-API-ACTIONS::crontab.resetSql` [P2] API contract crontab.resetSql: status=200 non-json response
  - repro_step: run `POST /api/crontab/resetSql`
  - evidence: `OK`
- `L1-FULL-API-ACTIONS::crontab.timetask` [P2] API contract crontab.timetask: status=200 non-json response
  - repro_step: run `POST /api/crontab/timetask`
  - evidence: `OK`
- `L1-FULL-API-ACTIONS::goods.goodsShare` [P2] API contract goods.goodsShare: status=500 server error
  - repro_step: run `POST /api/goods/goodsShare`
  - evidence: `<!DOCTYPE html>
<html>
<head>
	<meta charset="utf-8">
	<title>Internal Server Error - ThinkJS</title>
	<style>
	
		body,code,dd,div,dl,dt,h1,h2,h3,h4,h5,h6,li,pre,ul{margin:0;padding:0}a{text-decoration:none}.clearfix{clear:both;zoom:1}.clearfix:after{clear:both;content:"";display:block;height:0;vis`
- `L1-FULL-API-ACTIONS::index.index` [P2] API contract index.index: status=200 non-json response
  - repro_step: run `GET /api/index/index`
  - evidence: `<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>海鸥飞啊飞</title>
    <link rel="stylesheet" type="text/css" href="./static/css/style.css">
</head>
<body>
</body>
<!-- <script>window.location.href='http://www.zshxtop.com';</script> -->
<div class="wrap">
    <div class="top`
- `L1-FULL-API-ACTIONS::pay.notify` [P2] API contract pay.notify: status=200 non-json response
  - repro_step: run `POST /api/pay/notify`
  - evidence: `FAIL`
- `L1-FULL-API-ACTIONS::pay.preWeixinPay` [P2] API contract pay.preWeixinPay: status=500 server error
  - repro_step: run `POST /api/pay/preWeixinPay`
  - evidence: `<!DOCTYPE html>
<html>
<head>
	<meta charset="utf-8">
	<title>Internal Server Error - ThinkJS</title>
	<style>
	
		body,code,dd,div,dl,dt,h1,h2,h3,h4,h5,h6,li,pre,ul{margin:0;padding:0}a{text-decoration:none}.clearfix{clear:both;zoom:1}.clearfix:after{clear:both;content:"";display:block;height:0;vis`
- `L1-FULL-API-ACTIONS::pay.preWeixinPaya` [P2] API contract pay.preWeixinPaya: status=404 non-json response
  - repro_step: run `POST /api/pay/preWeixinPaya`
  - evidence: `<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>Not Found - ThinkJS</title>
  <style type="text/css">
  
    body,code,dd,div,dl,dt,h1,h2,h3,h4,h5,h6,li,ol,pre,ul{margin:0;padding:0}a{text-decoration:none}.clearfix{clear:both;zoom:1}.clearfix:after{clear:both;content:"";display:block`
- `L1-FULL-API-ACTIONS::region.code` [P2] API contract region.code: status=500 server error
  - repro_step: run `POST /api/region/code`
  - evidence: `<!DOCTYPE html>
<html>
<head>
	<meta charset="utf-8">
	<title>Internal Server Error - ThinkJS</title>
	<style>
	
		body,code,dd,div,dl,dt,h1,h2,h3,h4,h5,h6,li,pre,ul{margin:0;padding:0}a{text-decoration:none}.clearfix{clear:both;zoom:1}.clearfix:after{clear:both;content:"";display:block;height:0;vis`
- `L1-FULL-API-ACTIONS::region.data` [P2] API contract region.data: status=500 server error
  - repro_step: run `POST /api/region/data`
  - evidence: `<!DOCTYPE html>
<html>
<head>
	<meta charset="utf-8">
	<title>Internal Server Error - ThinkJS</title>
	<style>
	
		body,code,dd,div,dl,dt,h1,h2,h3,h4,h5,h6,li,pre,ul{margin:0;padding:0}a{text-decoration:none}.clearfix{clear:both;zoom:1}.clearfix:after{clear:both;content:"";display:block;height:0;vis`
- `L1-FULL-API-ACTIONS::region.info` [P2] API contract region.info: status=500 server error
  - repro_step: run `GET /api/region/info`
  - evidence: `<!DOCTYPE html>
<html>
<head>
	<meta charset="utf-8">
	<title>Internal Server Error - ThinkJS</title>
	<style>
	
		body,code,dd,div,dl,dt,h1,h2,h3,h4,h5,h6,li,pre,ul{margin:0;padding:0}a{text-decoration:none}.clearfix{clear:both;zoom:1}.clearfix:after{clear:both;content:"";display:block;height:0;vis`
- `L1-FULL-API-ACTIONS::upload.deleteFile` [P2] API contract upload.deleteFile: status=404 non-json response
  - repro_step: run `POST /api/upload/deleteFile`
  - evidence: `<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>Not Found - ThinkJS</title>
  <style type="text/css">
  
    body,code,dd,div,dl,dt,h1,h2,h3,h4,h5,h6,li,ol,pre,ul{margin:0;padding:0}a{text-decoration:none}.clearfix{clear:both;zoom:1}.clearfix:after{clear:both;content:"";display:block`
- `L1-FULL-API-ACTIONS::weChat.notify` [P2] API contract weChat.notify: status=500 server error
  - repro_step: run `POST /api/weChat/notify`
  - evidence: `<!DOCTYPE html>
<html>
<head>
	<meta charset="utf-8">
	<title>Internal Server Error - ThinkJS</title>
	<style>
	
		body,code,dd,div,dl,dt,h1,h2,h3,h4,h5,h6,li,pre,ul{margin:0;padding:0}a{text-decoration:none}.clearfix{clear:both;zoom:1}.clearfix:after{clear:both;content:"";display:block;height:0;vis`
- `L1-FULL-API-ACTIONS::weChat.receive` [P2] API contract weChat.receive: status=500 server error
  - repro_step: run `POST /api/weChat/receive`
  - evidence: `<!DOCTYPE html>
<html>
<head>
	<meta charset="utf-8">
	<title>Internal Server Error - ThinkJS</title>
	<style>
	
		body,code,dd,div,dl,dt,h1,h2,h3,h4,h5,h6,li,pre,ul{margin:0;padding:0}a{text-decoration:none}.clearfix{clear:both;zoom:1}.clearfix:after{clear:both;content:"";display:block;height:0;vis`
- `L2-OPERATIONS-FLOW` [P2] Admin goods import task records and exports: import_script=failed; operations_audit=failed
  - repro_step: run `node scripts/test-goods-import.js && python3 testing/scripts/operations_audit_suite.py --base-url http://127.0.0.1:8360 --admin-username qilelab.com --admin-password qilelab.com --db-host 127.0.0.1 --db-port 3306 --db-user root --db-password CHANGE_ME_STRONG_PASSWORD --db-name hiolabsDB --output /Volumes/SAMSUNG/fyb/myProjects/testing-artifacts/operations-audit-1773058062.json`
  - evidence: `import:任务轮询超时(taskId=70); audit:(1054, "Unknown column 'processed_rows' in 'field list'")`
- `L2-SEARCH-FOOTPRINT` [P2] Search history and footprint create/list/delete consistency: footprint list unexpected errno=412, status=200, errmsg=请先完善登录资料
  - repro_step: run `search index/clear + footprint list/delete`
- `L3-AD-CROSS-END` [P2] Admin ad config -> mini appInfo + ad messages: blocked by cross-end suite runtime error: ad create unexpected errno=100, status=200, errmsg=该商品已经有广告关联
