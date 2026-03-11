# Cross-Generation Upgrade Compatibility Contract

This document defines the non-breaking behavior that must hold during and after the upgrade.

## API Contract (Server)

- Preserve existing request headers and auth semantics:
  - `X-Hioshop-Token` remains the access token header.
- Preserve top-level response structure for existing endpoints:
  - `errno`, `errmsg`, `data`.
- Keep critical route paths unchanged:
  - `/api/order/*`, `/api/cart/*`, `/api/pay/*`, `/api/coupon/*`
  - `/admin/auth/login`, `/admin/order/*`, `/admin/coupon/*`, `/admin/goods/*`
- Keep current error code semantics for key flows:
  - unauthenticated access: `401`
  - forbidden resource access: `403`
  - missing resource: `404`

## Admin-Web Contract

- Keep route names used by permission map unchanged.
- Keep Axios auth injection via `X-Hioshop-Token`.
- Keep API base URL configurable through env variables in build/runtime.
- Keep key pages and route entry points stable:
  - login, dashboard/welcome, goods, order, coupon, promotion, invite.

## Miniprogram Contract

- Keep API endpoints and payload conventions unchanged.
- Keep token storage key and request header conventions unchanged.
- Keep key pages functional:
  - index, goods, cart, ucenter, order list/detail, invite.

## Regression Gates (Must Pass)

- `hioshop-server`: compile/build step, lint, coupon/security smoke.
- `hioshop-admin-web`: lint, unit tests, production build.
- `hioshop-miniprogram`: syntax checks + request smoke.
- Root PR gate / nightly suite:
  - order + coupon + payment notify + admin login + cross-end consistency.
