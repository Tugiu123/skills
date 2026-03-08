---
name: polymarket-arbitrage-finder
description: 发现 Polymarket 与其他交易所（Kalshi等）之间的套利机会。每次调用自动扣费 0.001 USDT
version: 1.0.0
author: moson
tags:
  - polymarket
  - arbitrage
  - trading
  - kalshi
  - defi
homepage: https://github.com/moson/polymarket-arbitrage-finder
metadata:
  clawdbot:
    requires:
      env:
        - SKILLPAY_API_KEY
triggers:
  - "polymarket arbitrage"
  - "find arbitrage opportunities"
  - "arbitrage finder"
config:
  SKILLPAY_API_KEY:
    type: string
    required: true
    secret: true
  MIN_PROFIT_THRESHOLD:
    type: number
    required: false
    default: 0.02
---

# Polymarket Arbitrage Finder

## 功能
- 扫描 Polymarket 市场与 Kalshi 之间的价差
- 计算理论套利利润
- 过滤低流动性市场
- 支持自定义利润阈值

## 使用
```js
{ action: 'scan' }
{ action: 'scan', threshold: 0.05 }
```
