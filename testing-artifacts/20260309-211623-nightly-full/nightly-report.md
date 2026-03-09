# Hioshop Nightly Full Regression

- mode: `nightly`
- started_at: `2026-03-09T21:16:23+08:00`
- finished_at: `2026-03-09T21:16:32+08:00`
- summary: `passed=290`, `failed=0`, `skipped=0`, `total=290`

## Layer Summary

| layer | passed | failed | skipped | total |
|---|---:|---:|---:|---:|
| L1 | 264 | 0 | 0 | 264 |
| L2 | 17 | 0 | 0 | 17 |
| L3 | 5 | 0 | 0 | 5 |
| L4 | 4 | 0 | 0 | 4 |

## Results

| id | layer | status | severity | message |
|---|---|---|---|---|
| L2-ADDRESS-FLOW | L2 | passed | P0 | core user journey passed |
| L2-CART-FLOW | L2 | passed | P0 | core user journey passed |
| L2-CHECKOUT-FLOW | L2 | passed | P0 | core user journey passed |
| L2-COUPON-LIFECYCLE | L2 | passed | P0 | Coupon 模块自动化冒烟通过。 |
| L2-GOODS-FLOW | L2 | passed | P0 | core user journey passed |
| L2-LOGIN-GATE | L2 | passed | P0 | core user journey passed |
| L2-ORDER-LIFECYCLE | L2 | passed | P0 | core user journey passed |
| L2-PAY-FLOW | L2 | passed | P0 | Concurrent pay notify idempotency check passed. |
| L2-PROMOTION-LIFECYCLE | L2 | passed | P0 | Promotion V1 mock 联调验证全部通过。 |
| L2-SUBMIT-FLOW | L2 | passed | P0 | core user journey passed |
| NIGHTLY-NOTIFY-CONCURRENCY | L2 | passed | P0 | Concurrent pay notify idempotency check passed. |
| L1-CORE-ADDRESS | L1 | passed | P1 | mapped_actions=1, failed=0, skipped=0 |
| L1-CORE-AUTH | L1 | passed | P1 | mapped_actions=1, failed=0, skipped=0 |
| L1-CORE-CART | L1 | passed | P1 | mapped_actions=1, failed=0, skipped=0 |
| L1-CORE-COUPON | L1 | passed | P1 | mapped_actions=1, failed=0, skipped=0 |
| L1-CORE-ORDER | L1 | passed | P1 | mapped_actions=1, failed=0, skipped=0 |
| L1-CORE-PAY | L1 | passed | P1 | mapped_actions=1, failed=0, skipped=0 |
| L2-HOME-PAGE | L2 | passed | P1 | appInfo ok, popupAd_present=1 |
| NIGHTLY-SECURITY-ABUSE | L2 | passed | P1 | Security abuse smoke passed. |
| L3-COUPON-CROSS-END | L3 | passed | P1 | coupon_id=180, user_coupon_id=179 |
| L3-ORDER-OPS-CROSS-END | L3 | passed | P1 | order_id=1592, order_sn=20260201131628846280, status=301, memo_synced=1 |
| L3-PROMOTION-CROSS-END | L3 | passed | P1 | promotion_id=26, goods_id=1009012 |
| L4-ADMIN-LOGIN-SMOKE | L4 | passed | P1 | admin login passed |
| L4-MINI-REQUEST-SMOKE | L4 | passed | P1 | 401/412/network handling smoke passed |
| NIGHTLY-COS-REAL-SMOKE | L4 | passed | P1 | COS 冒烟通过。 |
| L1-CORE-AD | L1 | passed | P2 | mapped_actions=1, failed=0, skipped=0 |
| L1-CORE-SETTINGS | L1 | passed | P2 | mapped_actions=1, failed=0, skipped=0 |
| L1-FULL-ADMIN-ACTIONS | L1 | passed | P2 | actions=186, failed=0, skipped=0 |
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
| L1-FULL-ADMIN-ACTIONS::admin.showsetStore | L1 | passed | P2 | status=200, errno=500 |
| L1-FULL-ADMIN-ACTIONS::admin.store | L1 | passed | P2 | status=200, errno=500 |
| L1-FULL-ADMIN-ACTIONS::admin.storeShipperSettings | L1 | passed | P2 | status=200, errno=0 |
| L1-FULL-ADMIN-ACTIONS::auth.login | L1 | passed | P2 | status=200, errno=401 |
| L1-FULL-ADMIN-ACTIONS::category.categoryStatus | L1 | passed | P2 | status=200, errno=500 |
| L1-FULL-ADMIN-ACTIONS::category.channelStatus | L1 | passed | P2 | status=200, errno=500 |
| L1-FULL-ADMIN-ACTIONS::category.deleteBannerImage | L1 | passed | P2 | status=200, errno=0 |
| L1-FULL-ADMIN-ACTIONS::category.deleteIconImage | L1 | passed | P2 | status=200, errno=0 |
| L1-FULL-ADMIN-ACTIONS::category.destory | L1 | passed | P2 | status=200, errno=0 |
| L1-FULL-ADMIN-ACTIONS::category.index | L1 | passed | P2 | status=200, errno=0 |
| L1-FULL-ADMIN-ACTIONS::category.info | L1 | passed | P2 | status=200, errno=0 |
| L1-FULL-ADMIN-ACTIONS::category.showStatus | L1 | passed | P2 | status=200, errno=0 |
| L1-FULL-ADMIN-ACTIONS::category.store | L1 | passed | P2 | status=200, errno=500 |
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
| L1-FULL-ADMIN-ACTIONS::goods.checkSku | L1 | passed | P2 | status=200, errno=500 |
| L1-FULL-ADMIN-ACTIONS::goods.copygoods | L1 | passed | P2 | status=200, errno=500 |
| L1-FULL-ADMIN-ACTIONS::goods.deleteGalleryFile | L1 | passed | P2 | status=200, errno=0 |
| L1-FULL-ADMIN-ACTIONS::goods.deleteListPicUrl | L1 | passed | P2 | status=200, errno=0 |
| L1-FULL-ADMIN-ACTIONS::goods.destory | L1 | passed | P2 | status=200, errno=0 |
| L1-FULL-ADMIN-ACTIONS::goods.drop | L1 | passed | P2 | status=200, errno=0 |
| L1-FULL-ADMIN-ACTIONS::goods.gallery | L1 | passed | P2 | status=200, errno=500 |
| L1-FULL-ADMIN-ACTIONS::goods.galleryEdit | L1 | passed | P2 | status=200, errno=500 |
| L1-FULL-ADMIN-ACTIONS::goods.galleryList | L1 | passed | P2 | status=200, errno=500 |
| L1-FULL-ADMIN-ACTIONS::goods.getAllCategory | L1 | passed | P2 | status=200, errno=0 |
| L1-FULL-ADMIN-ACTIONS::goods.getAllCategory1 | L1 | passed | P2 | status=200, errno=0 |
| L1-FULL-ADMIN-ACTIONS::goods.getAllSpecification | L1 | passed | P2 | status=200, errno=0 |
| L1-FULL-ADMIN-ACTIONS::goods.getExpressData | L1 | passed | P2 | status=200, errno=0 |
| L1-FULL-ADMIN-ACTIONS::goods.getGalleryList | L1 | passed | P2 | status=200, errno=500 |
| L1-FULL-ADMIN-ACTIONS::goods.importTaskCreate | L1 | passed | P2 | status=200, errno=400 |
| L1-FULL-ADMIN-ACTIONS::goods.importTaskDetail | L1 | passed | P2 | status=200, errno=400 |
| L1-FULL-ADMIN-ACTIONS::goods.importTaskErrorFile | L1 | passed | P2 | status=200, errno=400 |
| L1-FULL-ADMIN-ACTIONS::goods.importTaskList | L1 | passed | P2 | status=200, errno=0 |
| L1-FULL-ADMIN-ACTIONS::goods.importTemplate | L1 | passed | P2 | status=200 non-json allowed |
| L1-FULL-ADMIN-ACTIONS::goods.index | L1 | passed | P2 | status=200, errno=0 |
| L1-FULL-ADMIN-ACTIONS::goods.indexShowStatus | L1 | passed | P2 | status=200, errno=0 |
| L1-FULL-ADMIN-ACTIONS::goods.info | L1 | passed | P2 | status=200, errno=0 |
| L1-FULL-ADMIN-ACTIONS::goods.onsale | L1 | passed | P2 | status=200, errno=0 |
| L1-FULL-ADMIN-ACTIONS::goods.out | L1 | passed | P2 | status=200, errno=0 |
| L1-FULL-ADMIN-ACTIONS::goods.picker | L1 | passed | P2 | status=200, errno=0 |
| L1-FULL-ADMIN-ACTIONS::goods.pickerList | L1 | passed | P2 | status=200, errno=0 |
| L1-FULL-ADMIN-ACTIONS::goods.pickerSelected | L1 | passed | P2 | status=200, errno=0 |
| L1-FULL-ADMIN-ACTIONS::goods.pickerSku | L1 | passed | P2 | status=200, errno=400 |
| L1-FULL-ADMIN-ACTIONS::goods.productStatus | L1 | passed | P2 | status=200, errno=500 |
| L1-FULL-ADMIN-ACTIONS::goods.saleStatus | L1 | passed | P2 | status=200, errno=500 |
| L1-FULL-ADMIN-ACTIONS::goods.sort | L1 | passed | P2 | status=200, errno=0 |
| L1-FULL-ADMIN-ACTIONS::goods.store | L1 | passed | P2 | status=200, errno=500 |
| L1-FULL-ADMIN-ACTIONS::goods.updateGoodsNumber | L1 | passed | P2 | status=200, errno=0 |
| L1-FULL-ADMIN-ACTIONS::goods.updatePrice | L1 | passed | P2 | status=200, errno=500 |
| L1-FULL-ADMIN-ACTIONS::goods.updateShortName | L1 | passed | P2 | status=200, errno=500 |
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
| L1-FULL-ADMIN-ACTIONS::notice.updateContent | L1 | passed | P2 | status=200, errno=500 |
| L1-FULL-ADMIN-ACTIONS::order.changeStatus | L1 | passed | P2 | status=200, errno=500 |
| L1-FULL-ADMIN-ACTIONS::order.checkExpress | L1 | passed | P2 | status=200, errno=100 |
| L1-FULL-ADMIN-ACTIONS::order.destory | L1 | passed | P2 | status=200, errno=0 |
| L1-FULL-ADMIN-ACTIONS::order.detail | L1 | passed | P2 | status=200, errno=500 |
| L1-FULL-ADMIN-ACTIONS::order.directPrintExpress | L1 | passed | P2 | status=200, errno=500 |
| L1-FULL-ADMIN-ACTIONS::order.getAllRegion | L1 | passed | P2 | status=200, errno=0 |
| L1-FULL-ADMIN-ACTIONS::order.getAutoStatus | L1 | passed | P2 | status=200, errno=0 |
| L1-FULL-ADMIN-ACTIONS::order.getGoodsSpecification | L1 | passed | P2 | status=200, errno=500 |
| L1-FULL-ADMIN-ACTIONS::order.getMianExpress | L1 | passed | P2 | status=200, errno=500 |
| L1-FULL-ADMIN-ACTIONS::order.getOrderExpress | L1 | passed | P2 | status=200, errno=500 |
| L1-FULL-ADMIN-ACTIONS::order.getPrintTest | L1 | passed | P2 | status=200, errno=0 |
| L1-FULL-ADMIN-ACTIONS::order.goDelivery | L1 | passed | P2 | status=200, errno=500 |
| L1-FULL-ADMIN-ACTIONS::order.goPrintOnly | L1 | passed | P2 | status=200, errno=0 |
| L1-FULL-ADMIN-ACTIONS::order.goodsListDelete | L1 | passed | P2 | status=200, errno=500 |
| L1-FULL-ADMIN-ACTIONS::order.index | L1 | passed | P2 | status=200, errno=0 |
| L1-FULL-ADMIN-ACTIONS::order.orderDelivery | L1 | passed | P2 | status=200, errno=500 |
| L1-FULL-ADMIN-ACTIONS::order.orderPrice | L1 | passed | P2 | status=200, errno=500 |
| L1-FULL-ADMIN-ACTIONS::order.orderReceive | L1 | passed | P2 | status=200, errno=500 |
| L1-FULL-ADMIN-ACTIONS::order.orderpack | L1 | passed | P2 | status=200, errno=500 |
| L1-FULL-ADMIN-ACTIONS::order.rePrintExpress | L1 | passed | P2 | status=200, errno=500 |
| L1-FULL-ADMIN-ACTIONS::order.saveAddress | L1 | passed | P2 | status=200, errno=500 |
| L1-FULL-ADMIN-ACTIONS::order.saveAdminMemo | L1 | passed | P2 | status=200, errno=500 |
| L1-FULL-ADMIN-ACTIONS::order.saveExpressValueInfo | L1 | passed | P2 | status=200, errno=500 |
| L1-FULL-ADMIN-ACTIONS::order.saveGoodsList | L1 | passed | P2 | status=200, errno=400 |
| L1-FULL-ADMIN-ACTIONS::order.savePrintInfo | L1 | passed | P2 | status=200, errno=500 |
| L1-FULL-ADMIN-ACTIONS::order.saveRemarkInfo | L1 | passed | P2 | status=200, errno=500 |
| L1-FULL-ADMIN-ACTIONS::order.store | L1 | passed | P2 | status=200, errno=500 |
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
| L1-FULL-ADMIN-ACTIONS::shipper.addExceptArea | L1 | passed | P2 | status=200, errno=500 |
| L1-FULL-ADMIN-ACTIONS::shipper.addTable | L1 | passed | P2 | status=200, errno=500 |
| L1-FULL-ADMIN-ACTIONS::shipper.destory | L1 | passed | P2 | status=200, errno=0 |
| L1-FULL-ADMIN-ACTIONS::shipper.enabledStatus | L1 | passed | P2 | status=200, errno=500 |
| L1-FULL-ADMIN-ACTIONS::shipper.exceptAreaDelete | L1 | passed | P2 | status=200, errno=0 |
| L1-FULL-ADMIN-ACTIONS::shipper.exceptAreaDetail | L1 | passed | P2 | status=200, errno=500 |
| L1-FULL-ADMIN-ACTIONS::shipper.exceptarea | L1 | passed | P2 | status=200, errno=0 |
| L1-FULL-ADMIN-ACTIONS::shipper.freight | L1 | passed | P2 | status=200, errno=0 |
| L1-FULL-ADMIN-ACTIONS::shipper.freightdetail | L1 | passed | P2 | status=200, errno=0 |
| L1-FULL-ADMIN-ACTIONS::shipper.getareadata | L1 | passed | P2 | status=200, errno=0 |
| L1-FULL-ADMIN-ACTIONS::shipper.index | L1 | passed | P2 | status=200, errno=0 |
| L1-FULL-ADMIN-ACTIONS::shipper.info | L1 | passed | P2 | status=200, errno=0 |
| L1-FULL-ADMIN-ACTIONS::shipper.list | L1 | passed | P2 | status=200, errno=0 |
| L1-FULL-ADMIN-ACTIONS::shipper.saveExceptArea | L1 | passed | P2 | status=200, errno=500 |
| L1-FULL-ADMIN-ACTIONS::shipper.saveTable | L1 | passed | P2 | status=200, errno=500 |
| L1-FULL-ADMIN-ACTIONS::shipper.store | L1 | passed | P2 | status=200, errno=0 |
| L1-FULL-ADMIN-ACTIONS::shipper.updateSort | L1 | passed | P2 | status=200, errno=0 |
| L1-FULL-ADMIN-ACTIONS::shopcart.index | L1 | passed | P2 | status=200, errno=0 |
| L1-FULL-ADMIN-ACTIONS::specification.add | L1 | passed | P2 | status=200, errno=0 |
| L1-FULL-ADMIN-ACTIONS::specification.checkSn | L1 | passed | P2 | status=200, errno=500 |
| L1-FULL-ADMIN-ACTIONS::specification.delePrimarySpec | L1 | passed | P2 | status=200, errno=0 |
| L1-FULL-ADMIN-ACTIONS::specification.delete | L1 | passed | P2 | status=200, errno=0 |
| L1-FULL-ADMIN-ACTIONS::specification.detail | L1 | passed | P2 | status=200, errno=500 |
| L1-FULL-ADMIN-ACTIONS::specification.getGoodsSpec | L1 | passed | P2 | status=200, errno=500 |
| L1-FULL-ADMIN-ACTIONS::specification.index | L1 | passed | P2 | status=200, errno=0 |
| L1-FULL-ADMIN-ACTIONS::specification.productDele | L1 | passed | P2 | status=200, errno=500 |
| L1-FULL-ADMIN-ACTIONS::specification.productUpdate | L1 | passed | P2 | status=200, errno=500 |
| L1-FULL-ADMIN-ACTIONS::specification.update | L1 | passed | P2 | status=200, errno=0 |
| L1-FULL-ADMIN-ACTIONS::user.address | L1 | passed | P2 | status=200, errno=500 |
| L1-FULL-ADMIN-ACTIONS::user.cartdata | L1 | passed | P2 | status=200, errno=500 |
| L1-FULL-ADMIN-ACTIONS::user.datainfo | L1 | passed | P2 | status=200, errno=500 |
| L1-FULL-ADMIN-ACTIONS::user.destory | L1 | passed | P2 | status=200, errno=0 |
| L1-FULL-ADMIN-ACTIONS::user.foot | L1 | passed | P2 | status=200, errno=500 |
| L1-FULL-ADMIN-ACTIONS::user.index | L1 | passed | P2 | status=200, errno=0 |
| L1-FULL-ADMIN-ACTIONS::user.info | L1 | passed | P2 | status=200, errno=500 |
| L1-FULL-ADMIN-ACTIONS::user.order | L1 | passed | P2 | status=200, errno=500 |
| L1-FULL-ADMIN-ACTIONS::user.saveaddress | L1 | passed | P2 | status=200, errno=500 |
| L1-FULL-ADMIN-ACTIONS::user.store | L1 | passed | P2 | status=200, errno=500 |
| L1-FULL-ADMIN-ACTIONS::user.updateInfo | L1 | passed | P2 | status=200, errno=500 |
| L1-FULL-ADMIN-ACTIONS::user.updateMobile | L1 | passed | P2 | status=200, errno=500 |
| L1-FULL-ADMIN-ACTIONS::user.updateName | L1 | passed | P2 | status=200, errno=0 |
| L1-FULL-ADMIN-ACTIONS::wap.destory | L1 | passed | P2 | status=200, errno=0 |
| L1-FULL-ADMIN-ACTIONS::wap.drop | L1 | passed | P2 | status=200, errno=0 |
| L1-FULL-ADMIN-ACTIONS::wap.getAllCategory | L1 | passed | P2 | status=200, errno=0 |
| L1-FULL-ADMIN-ACTIONS::wap.getAllCategory1 | L1 | passed | P2 | status=200, errno=0 |
| L1-FULL-ADMIN-ACTIONS::wap.getGoodsSnName | L1 | passed | P2 | status=200, errno=500 |
| L1-FULL-ADMIN-ACTIONS::wap.index | L1 | passed | P2 | status=200, errno=0 |
| L1-FULL-ADMIN-ACTIONS::wap.info | L1 | passed | P2 | status=200, errno=500 |
| L1-FULL-ADMIN-ACTIONS::wap.onsale | L1 | passed | P2 | status=200, errno=0 |
| L1-FULL-ADMIN-ACTIONS::wap.out | L1 | passed | P2 | status=200, errno=0 |
| L1-FULL-ADMIN-ACTIONS::wap.outsale | L1 | passed | P2 | status=200, errno=0 |
| L1-FULL-ADMIN-ACTIONS::wap.saleStatus | L1 | passed | P2 | status=200, errno=500 |
| L1-FULL-ADMIN-ACTIONS::wap.sort | L1 | passed | P2 | status=200, errno=0 |
| L1-FULL-ADMIN-ACTIONS::wap.store | L1 | passed | P2 | status=200, errno=500 |
| L1-FULL-ADMIN-ACTIONS::wap.updatePrice | L1 | passed | P2 | status=200, errno=500 |
| L1-FULL-API-ACTIONS | L1 | passed | P2 | actions=68, failed=0, skipped=0 |
| L1-FULL-API-ACTIONS::ad.messages | L1 | passed | P2 | status=200, errno=0 |
| L1-FULL-API-ACTIONS::ad.readAll | L1 | passed | P2 | status=200, errno=0 |
| L1-FULL-API-ACTIONS::ad.unreadCount | L1 | passed | P2 | status=200, errno=0 |
| L1-FULL-API-ACTIONS::address.addressDetail | L1 | passed | P2 | status=200, errno=400 |
| L1-FULL-API-ACTIONS::address.deleteAddress | L1 | passed | P2 | status=200, errno=400 |
| L1-FULL-API-ACTIONS::address.getAddresses | L1 | passed | P2 | status=200, errno=0 |
| L1-FULL-API-ACTIONS::address.saveAddress | L1 | passed | P2 | status=200, errno=400 |
| L1-FULL-API-ACTIONS::auth.loginByWeixin | L1 | passed | P2 | status=200, errno=400 |
| L1-FULL-API-ACTIONS::auth.logout | L1 | passed | P2 | status=200, errno=0 |
| L1-FULL-API-ACTIONS::auth.phoneNumber | L1 | passed | P2 | status=200, errno=401 |
| L1-FULL-API-ACTIONS::cart.add | L1 | passed | P2 | status=200, errno=400 |
| L1-FULL-API-ACTIONS::cart.checked | L1 | passed | P2 | status=200, errno=500 |
| L1-FULL-API-ACTIONS::cart.checkout | L1 | passed | P2 | status=200, errno=0 |
| L1-FULL-API-ACTIONS::cart.delete | L1 | passed | P2 | status=200, errno=1000 |
| L1-FULL-API-ACTIONS::cart.goodsCount | L1 | passed | P2 | status=200, errno=0 |
| L1-FULL-API-ACTIONS::cart.index | L1 | passed | P2 | status=200, errno=0 |
| L1-FULL-API-ACTIONS::cart.update | L1 | passed | P2 | status=200, errno=404 |
| L1-FULL-API-ACTIONS::catalog.current | L1 | passed | P2 | status=200, errno=0 |
| L1-FULL-API-ACTIONS::catalog.currentlist | L1 | passed | P2 | status=200, errno=500 |
| L1-FULL-API-ACTIONS::catalog.index | L1 | passed | P2 | status=200, errno=0 |
| L1-FULL-API-ACTIONS::coupon.center | L1 | passed | P2 | status=200, errno=0 |
| L1-FULL-API-ACTIONS::coupon.my | L1 | passed | P2 | status=200, errno=0 |
| L1-FULL-API-ACTIONS::coupon.preview | L1 | passed | P2 | status=200, errno=0 |
| L1-FULL-API-ACTIONS::coupon.receive | L1 | passed | P2 | status=200, errno=400 |
| L1-FULL-API-ACTIONS::crontab.processGoodsImportTask | L1 | passed | P2 | status=200, errno=0 |
| L1-FULL-API-ACTIONS::crontab.resetSql | L1 | passed | P2 | status=200, errno=0 |
| L1-FULL-API-ACTIONS::crontab.timetask | L1 | passed | P2 | status=200, errno=0 |
| L1-FULL-API-ACTIONS::footprint.delete | L1 | passed | P2 | status=200, errno=500 |
| L1-FULL-API-ACTIONS::footprint.list | L1 | passed | P2 | status=200, errno=0 |
| L1-FULL-API-ACTIONS::goods.count | L1 | passed | P2 | status=200, errno=0 |
| L1-FULL-API-ACTIONS::goods.detail | L1 | passed | P2 | status=200, errno=1000 |
| L1-FULL-API-ACTIONS::goods.goodsShare | L1 | passed | P2 | status=200, errno=500 |
| L1-FULL-API-ACTIONS::goods.index | L1 | passed | P2 | status=200, errno=0 |
| L1-FULL-API-ACTIONS::goods.list | L1 | passed | P2 | status=200, errno=0 |
| L1-FULL-API-ACTIONS::index.appInfo | L1 | passed | P2 | status=200, errno=0 |
| L1-FULL-API-ACTIONS::index.index | L1 | passed | P2 | status=200, errno=0 |
| L1-FULL-API-ACTIONS::invite.myRecords | L1 | passed | P2 | status=200, errno=0 |
| L1-FULL-API-ACTIONS::invite.mySummary | L1 | passed | P2 | status=200, errno=0 |
| L1-FULL-API-ACTIONS::order.cancel | L1 | passed | P2 | status=200, errno=1000 |
| L1-FULL-API-ACTIONS::order.complete | L1 | passed | P2 | status=200, errno=500 |
| L1-FULL-API-ACTIONS::order.confirm | L1 | passed | P2 | status=200, errno=1000 |
| L1-FULL-API-ACTIONS::order.count | L1 | passed | P2 | status=200, errno=0 |
| L1-FULL-API-ACTIONS::order.delete | L1 | passed | P2 | status=200, errno=1000 |
| L1-FULL-API-ACTIONS::order.detail | L1 | passed | P2 | status=200, errno=1000 |
| L1-FULL-API-ACTIONS::order.express | L1 | passed | P2 | status=200, errno=500 |
| L1-FULL-API-ACTIONS::order.list | L1 | passed | P2 | status=200, errno=0 |
| L1-FULL-API-ACTIONS::order.orderCount | L1 | passed | P2 | status=200, errno=0 |
| L1-FULL-API-ACTIONS::order.orderGoods | L1 | passed | P2 | status=200, errno=0 |
| L1-FULL-API-ACTIONS::order.submit | L1 | passed | P2 | status=200, errno=500 |
| L1-FULL-API-ACTIONS::order.update | L1 | passed | P2 | status=200, errno=404 |
| L1-FULL-API-ACTIONS::pay.notify | L1 | passed | P2 | status=200 non-json allowed |
| L1-FULL-API-ACTIONS::pay.preWeixinPay | L1 | passed | P2 | status=200, errno=500 |
| L1-FULL-API-ACTIONS::pay.preWeixinPaya | L1 | passed | P2 | status=200, errno=404 |
| L1-FULL-API-ACTIONS::qrcode.getBase64 | L1 | passed | P2 | status=200, errno=0 |
| L1-FULL-API-ACTIONS::region.code | L1 | passed | P2 | status=200, errno=500 |
| L1-FULL-API-ACTIONS::region.data | L1 | passed | P2 | status=200, errno=500 |
| L1-FULL-API-ACTIONS::region.info | L1 | passed | P2 | status=200, errno=500 |
| L1-FULL-API-ACTIONS::region.list | L1 | passed | P2 | status=200, errno=0 |
| L1-FULL-API-ACTIONS::search.clearHistory | L1 | passed | P2 | status=200, errno=0 |
| L1-FULL-API-ACTIONS::search.helper | L1 | passed | P2 | status=200, errno=0 |
| L1-FULL-API-ACTIONS::search.index | L1 | passed | P2 | status=200, errno=0 |
| L1-FULL-API-ACTIONS::settings.save | L1 | passed | P2 | status=200, errno=400 |
| L1-FULL-API-ACTIONS::settings.showSettings | L1 | passed | P2 | status=200, errno=0 |
| L1-FULL-API-ACTIONS::settings.userDetail | L1 | passed | P2 | status=200, errno=0 |
| L1-FULL-API-ACTIONS::upload.deleteFile | L1 | passed | P2 | status=200, errno=404 |
| L1-FULL-API-ACTIONS::upload.uploadAvatar | L1 | passed | P2 | status=200, errno=1000 |
| L1-FULL-API-ACTIONS::weChat.notify | L1 | passed | P2 | status=200, errno=500 |
| L1-FULL-API-ACTIONS::weChat.receive | L1 | passed | P2 | status=200, errno=500 |
| L2-AD-MESSAGE-FLOW | L2 | passed | P2 | before=0, after=0, user_ad_read_before=2, user_ad_read_after=2 |
| L2-INVITE-FLOW | L2 | passed | P2 | schema_ready=1, invite_total=0 |
| L2-OPERATIONS-FLOW | L2 | passed | P2 | import_script=passed; operations_audit=passed |
| L2-SEARCH-FOOTPRINT | L2 | passed | P2 | keyword=qa-search-1773062187, footprint_id=15678 |
| L3-AD-CROSS-END | L3 | passed | P2 | ad_id=0, popup_id=34, unread_before=0, unread_after=0 |
| L3-ADMIN-AUTH-PREREQ | L3 | passed | P2 | admin token acquired |
| L4-MINI-SYNTAX-SMOKE | L4 | passed | P2 | syntax checks passed |
