---
name: research-analyst
description: AI-powered US/China/HK stock & crypto research with 8-dimension analysis, China market reports (东方财富/新浪/财联社/腾讯/同花顺), real-time news monitoring with AI, Feishu push, one-click brief, smart scheduling, portfolio tracking, and trend detection | AI 驱动的美股/A股/港股/加密货币研究工具，提供 8 维度分析、中国市场多源报告（东方财富/新浪/财联社/腾讯/同花顺）、AI实时新闻监控、飞书推送、一键简报、智能定时、投资组合追踪和趋势检测
version: 1.3.0
verified_commit: e90cc7f  # v1.3.0 - AI News Monitoring System (real-time, keyword-based, API testing)
homepage: https://finance.yahoo.com
commands:
  - /stock - Analyze a stock or crypto (分析股票或加密货币)
  - /stock_compare - Compare multiple tickers (比较多个代码)
  - /stock_dividend - Analyze dividend metrics (分析股息指标)
  - /stock_watch - Add/remove from watchlist (添加/移除监控列表)
  - /stock_alerts - Check triggered alerts (检查触发的警报)
  - /stock_hot - Find trending stocks & crypto (发现热门股票和加密货币)
  - /stock_rumors - Find early signals, M&A rumors (发现早期信号、并购传闻)
  - /cn_market - China A-share & Hong Kong market report (中国市场报告)
  - /cn_brief - One-click brief market summary (一键精简市场简报)
  - /cn_rankings - Market rankings from 东方财富 (榜单数据)
  - /cn_quotes - Stock quotes from 新浪财经 (实时行情)
  - /cn_news - Financial news from 财联社 (财经快讯)
  - /cn_moneyflow - Money flow analysis from 腾讯财经 (资金流向)
  - /cn_diagnosis - Stock diagnosis from 同花顺 (个股诊断)
  - /portfolio - Show portfolio summary (显示投资组合摘要)
  - /portfolio_add - Add asset to portfolio (添加资产到投资组合)
metadata: {"clawdbot":{"emoji":"📈","requires":{"bins":["python3","uv"],"env":["AUTH_TOKEN","CT0"]},"install":[{"id":"python3-check","kind":"shell","command":"python3 --version","bins":["python3"],"label":"Verify Python 3.10+ installed"},{"id":"uv-brew","kind":"brew","formula":"uv","bins":["uv"],"label":"Install uv package manager"},{"id":"bird-npm","kind":"shell","command":"npm install -g @steipete/bird","bins":["bird"],"label":"Install bird CLI (optional, for Twitter/X)"}]}}
---

# OpenClaw Research Analyst v1.3.0
# OpenClaw 研究分析师 v1.3.0

**⚠️ Installation Required**: This skill requires Python 3.10+, uv package manager, and optional dependencies. See installation instructions below.

**📦 Source Code**: https://github.com/ZhenRobotics/openclaw-research-analyst

**English** | [中文](#中文版本)

---

## ✨ What's New in v1.3.0

### 🎉 Major Update: AI News Monitoring System

#### Real-time Financial News Monitoring
- **Automatic News Collection**
  - Multi-source: 财联社 (CLS) + 东方财富 (Eastmoney)
  - Configurable interval: 60-300 seconds
  - Smart deduplication
  - SQLite database storage

- **Intelligent Classification**
  - Keyword-based sentiment analysis (BULLISH/BEARISH/NEUTRAL)
  - Importance scoring (1-5 scale)
  - **100% accuracy** on test cases
  - Confidence tracking

- **Event-Driven Push**
  - Automatic Feishu push for major news (importance ≥4)
  - Customizable threshold
  - Push history logging
  - Retry mechanism

#### Fast Monitoring Mode
- **60-second interval** (vs 300s default)
- **30-40 seconds end-to-end latency**
- Incremental fetching (latest 20 items only)
- Time-based filtering

#### Interactive Labeling & AI Training
- **CLI Labeling Tool** - Manual annotation interface
- **BERT Training Pipeline** - Fine-tune chinese-roberta-wwm-ext
- **Auto-labeling** - Keyword-based pre-labeling
- **4-Stage Workflow** - collect → label → train → monitor

#### Comprehensive API Testing
- **9-Point Test Suite**
  - Functional testing (APIs, database, push)
  - Performance testing (P95 < 200ms target)
  - Reliability testing (error handling)
  - End-to-end workflow testing

- **Test Results**
  - 66.7% overall pass rate
  - 100% keyword matching accuracy
  - 10/10 concurrent requests success
  - 19s end-to-end latency

#### New Commands
```bash
# Quick start (keyword mode, no AI required)
./scripts/quick_start_ai.sh monitor-keyword

# AI workflow (4 stages)
./scripts/quick_start_ai.sh collect
./scripts/quick_start_ai.sh label
./scripts/quick_start_ai.sh train
./scripts/quick_start_ai.sh monitor

# Fast mode (60s interval)
python3 scripts/news_monitor_fast.py --no-ai --interval 60 --threshold 4

# API testing
python3 tests/api_test_suite.py
```

#### New Documentation
- **AI_NEWS_SYSTEM_GUIDE.md** - Complete workflow guide
- **API_TESTING_GUIDE.md** - Testing methodology
- **API_TEST_RESULTS_ANALYSIS.md** - Performance analysis
- **REALTIME_WEBSOCKET_DESIGN.md** - Architecture design

---

## 🔙 Previous Updates (v1.2.1)

### 🔧 Feishu Push Optimizations
- **Detailed Return Values** - Push methods now return comprehensive status
  - Message ID, timestamp, method, error details
  - Example: `result['message_ids']`, `result['success']`, `result['error']`

- **Auto-Retry Mechanism** - Network requests retry up to 2 times
  - Exponential backoff: 1s, 2s
  - Handles Timeout and ConnectionError

- **Push History Logging** - Track all push attempts
  - Log file: `logs/feishu_push_history.log`
  - JSON format with message preview, status, timestamp

- **Clear Error Messages** - Distinguish configuration vs network errors
  - "User Open ID not configured"
  - "Timeout: Connection timeout after 10 seconds"

### 📚 Documentation
- **FEISHU_PUSH_v1.2.1_GUIDE.md** - Complete guide with examples
- **OPTIMIZATION_v1.2.1.md** - Implementation details

---

## 🔙 Previous Updates (v1.2.0)

### 🎉 New Features
- **📊 One-Click Brief** - Ultra-fast market summary generation
  - Command: `python3 scripts/cn_market_brief.py`
  - Output: ≤140 chars, top 3 gainers/losers/volume leaders
  - Auto-save to `reports/cn_market_brief_YYYY-MM-DD_HHMM.txt`
  - JSON output support for automation
  - Optional Feishu push: `--push` flag

- **⏰ Smart Scheduling** - Intelligent cron jobs for trading hours
  - Intraday push: Every 10 minutes (Mon-Fri 09:30-15:00)
  - End-of-day report: Once after market close (15:05)
  - Auto-skip weekends and non-trading hours
  - One-command installation: `./scripts/cn_market_schedule.sh install`
  - Comprehensive logging and status monitoring

### 🔧 Improvements
- Enhanced `--brief` flag: Now saves to independent file with clean output
- Improved error handling for network timeouts
- Better documentation with SMART_SCHEDULING.md guide

### 📚 Documentation
- [SMART_SCHEDULING.md](https://github.com/ZhenRobotics/openclaw-research-analyst/blob/main/SMART_SCHEDULING.md) - Complete scheduling guide
- [OPTIMIZATION_COMPLETE.md](https://github.com/ZhenRobotics/openclaw-research-analyst/blob/main/OPTIMIZATION_COMPLETE.md) - Implementation report

---

## 🔙 Previous Updates (v1.1.0)

### 🎉 Major Features
- **📱 Feishu Push Integration** - Auto-push China market reports to Feishu private chat or group
  - Private chat push with Open ID
  - Group webhook support
  - Auto-push every 10 minutes via system cron
  - Configuration wizard: `python3 scripts/feishu_setup.py`

- **🚀 Async Architecture Optimization** - 70-90% performance improvement
  - Parallel data fetching with `aiohttp`
  - 5 data sources fetched concurrently
  - Reduced report generation time from 2.5s to 700ms
  - Use: `python3 scripts/cn_market_report.py --async`

### 🔧 Improvements
- **📊 One-Click Brief** - Instant market summary with `cn_market_brief.py`
- **⏰ Smart Scheduling** - Intelligent cron jobs for trading hours
  - Intraday push: Every 10 minutes (Mon-Fri 09:30-15:00)
  - End-of-day report: Once after market close (15:05)
  - Auto-skip weekends and non-trading hours
- Brief summary generation (`--brief` flag)
- Environment variable configuration support
- Comprehensive Feishu setup documentation

### 📚 Documentation
- [FEISHU_QUICKSTART.md](https://github.com/ZhenRobotics/openclaw-research-analyst/blob/main/FEISHU_QUICKSTART.md) - 5-minute setup guide
- [IMPLEMENTATION_COMPLETE.md](https://github.com/ZhenRobotics/openclaw-research-analyst/blob/main/IMPLEMENTATION_COMPLETE.md) - Async architecture details

---

Analyze **US stocks, China A-shares, Hong Kong stocks**, and **cryptocurrencies** with 8-dimension analysis, **China market multi-source reports** (东方财富/新浪/财联社/腾讯/同花顺), portfolio management, watchlists, alerts, dividend analysis, and **viral trend detection**.

---

## Core Features

- 📊 **8-Dimension Analysis** — Comprehensive stock scoring (earnings, fundamentals, analysts, momentum, sentiment, sector, market, history)
- 💰 **Dividend Analysis** — Yield, payout ratio, 5-year growth, safety score
- 📈 **Portfolio Management** — Track holdings, P&L, concentration warnings
- ⏰ **Watchlist + Alerts** — Price targets, stop losses, signal changes
- 🔥 **Hot Scanner** — Multi-source viral trend detection (CoinGecko, Google News, Twitter/X)
- 🔮 **Rumor Detector** — Early signals for M&A, insider trades, analyst actions
- 🌏 **China Markets** — A-share & Hong Kong data (东方财富, 新浪, 财联社, 腾讯, 同花顺)
- 🪙 **Crypto Support** — Top 20 cryptos with BTC correlation
- ⚡ **Fast Mode** — Skip slow analyses for quick checks

## Quick Commands

### Stock Analysis
```bash
# Basic analysis
uv run {baseDir}/scripts/stock_analyzer.py AAPL

# Fast mode (skips insider trading & breaking news)
uv run {baseDir}/scripts/stock_analyzer.py AAPL --fast

# Compare multiple
uv run {baseDir}/scripts/stock_analyzer.py AAPL MSFT GOOGL

# Crypto
uv run {baseDir}/scripts/stock_analyzer.py BTC-USD ETH-USD
```

### Dividend Analysis
```bash
# Analyze dividends
uv run {baseDir}/scripts/dividend_analyzer.py JNJ

# Compare dividend stocks
uv run {baseDir}/scripts/dividend_analyzer.py JNJ PG KO MCD --output json
```

**Dividend Metrics:**
- Dividend Yield & Annual Payout
- Payout Ratio (safe/moderate/high/unsustainable)
- 5-Year Dividend Growth (CAGR)
- Consecutive Years of Increases
- Safety Score (0-100)
- Income Rating (excellent/good/moderate/poor)

### Watchlist + Alerts
```bash
# Add to watchlist
uv run {baseDir}/scripts/watchlist_manager.py add AAPL

# With price target alert
uv run {baseDir}/scripts/watchlist_manager.py add AAPL --target 200

# With stop loss alert
uv run {baseDir}/scripts/watchlist_manager.py add AAPL --stop 150

# Check for triggered alerts
uv run {baseDir}/scripts/watchlist_manager.py check
```

**Alert Types:**
- 🎯 **Target Hit** — Price >= target
- 🛑 **Stop Hit** — Price <= stop
- 📊 **Signal Change** — BUY/HOLD/SELL changed

### Portfolio Management
```bash
# Create portfolio
uv run {baseDir}/scripts/portfolio_manager.py create "Tech Portfolio"

# Add assets
uv run {baseDir}/scripts/portfolio_manager.py add AAPL --quantity 100 --cost 150

# View portfolio
uv run {baseDir}/scripts/portfolio_manager.py show
```

### 🌏 China Market Reports
```bash
# Complete China market report (all sources)
python3 {baseDir}/scripts/cn_market_report.py

# Market rankings from 东方财富
python3 {baseDir}/scripts/cn_market_rankings.py

# Stock quotes from 新浪财经
python3 {baseDir}/scripts/cn_stock_quotes.py 600519  # 贵州茅台

# Financial news from 财联社
python3 {baseDir}/scripts/cn_cls_telegraph.py

# Money flow analysis from 腾讯财经
python3 {baseDir}/scripts/cn_tencent_moneyflow.py

# Stock diagnosis from 同花顺
python3 {baseDir}/scripts/cn_ths_diagnosis.py 600519
```

**China Data Sources (5 Major Platforms):**
- 📊 **东方财富 (East Money)** — Market rankings, sector analysis, hot stocks
- 💹 **新浪财经 (Sina Finance)** — Real-time quotes, A-share & Hong Kong
- 📰 **财联社 (CLS)** — Breaking financial news, market telegraph
- 💰 **腾讯财经 (Tencent Finance)** — Money flow analysis, capital tracking
- 🔍 **同花顺 (THS)** — Stock diagnosis, technical analysis

**What You Get:**
- A-share (沪深) and Hong Kong stock data
- Market hot lists and sector rotations
- Real-time capital flow tracking
- Breaking financial news and announcements
- Individual stock technical diagnosis

### 📱 One-Click Brief (一键精简简报)
```bash
# Generate brief summary (≤120 chars)
python3 {baseDir}/scripts/cn_market_brief.py

# Generate and push to Feishu
python3 {baseDir}/scripts/cn_market_brief.py --push

# JSON output format
python3 {baseDir}/scripts/cn_market_brief.py --json
```

**Output Example:**
```
📊 14:33 市场快报

【A股】涨:中复神鹰+20.0% 跌:亨通光电-8.49% 额:兆易创新118亿
【港股】涨:毅高国际控股+98.0% 额:耀才证券金84亿

📄 已保存: reports/cn_market_brief_2026-03-18_1433.txt
```

**Features:**
- ⚡ Ultra-fast generation (~1 second)
- 📊 Top 3 gainers/losers and volume leaders
- 💾 Auto-save to reports folder
- 📱 Optional Feishu push integration

### 🔥 Hot Scanner
```bash
# Full scan - find what's trending NOW
python3 {baseDir}/scripts/trend_scanner.py

# Fast scan (skip social media)
python3 {baseDir}/scripts/trend_scanner.py --no-social

# JSON output for automation
python3 {baseDir}/scripts/trend_scanner.py --json
```

**Data Sources:**
- 📊 CoinGecko Trending — Top 15 trending coins
- 📈 CoinGecko Movers — Biggest gainers/losers
- 📰 Google News — Finance & crypto headlines
- 📉 Yahoo Finance — Gainers, losers, most active
- 🐦 Twitter/X — Social sentiment (requires auth)

### 🔮 Rumor Scanner
```bash
# Find early signals, M&A rumors, insider activity
python3 {baseDir}/scripts/rumor_detector.py
```

**What it finds:**
- 🏢 **M&A Rumors** — Merger, acquisition, takeover bids
- 👔 **Insider Activity** — CEO/Director buying/selling
- 📊 **Analyst Actions** — Upgrades, downgrades, price target changes
- 🐦 **Twitter Whispers** — "hearing that...", "sources say...", "rumor"
- ⚖️ **SEC Activity** — Investigations, filings

## Analysis Dimensions

### Stocks (8 dimensions)
| Dimension | Weight | Description |
|-----------|--------|-------------|
| Earnings Surprise | 30% | EPS beat/miss |
| Fundamentals | 20% | P/E, margins, growth |
| Analyst Sentiment | 20% | Ratings, price targets |
| Historical | 10% | Past earnings reactions |
| Market Context | 10% | VIX, SPY/QQQ trends |
| Sector | 15% | Relative strength |
| Momentum | 15% | RSI, 52-week range |
| Sentiment | 10% | Fear/Greed, shorts, insiders |

### Crypto (3 dimensions)
- Market Cap & Category
- BTC Correlation (30-day)
- Momentum (RSI, range)

## Performance Options

| Flag | Effect | Speed |
|------|--------|-------|
| (default) | Full analysis | 60-120s |
| `--no-insider` | Skip SEC EDGAR | 50-90s |
| `--fast` | Skip insider + news | 45-75s |

## Supported Cryptos (Top 20)

BTC, ETH, BNB, SOL, XRP, ADA, DOGE, AVAX, DOT, MATIC, LINK, ATOM, UNI, LTC, BCH, XLM, ALGO, VET, FIL, NEAR

(Use `-USD` suffix: `BTC-USD`, `ETH-USD`)

## ⏰ Automated Push Configuration

### Cron Job Setup

Automate real-time market updates and news monitoring with scheduled tasks:

#### 1. Major News Real-time Monitoring

**Frequency**: Every 5 minutes
**Command**: `python3 scripts/news_monitor_fast.py --no-ai --interval 300 --threshold 4`
**Push Target**: Feishu private chat
**Trigger**: Importance ≥ 4

```json
{
  "schedule": {"kind": "every", "everyMs": 300000},
  "delivery": {"mode": "none"}
}
```

#### 2. A-Share Market Hourly Updates

**Frequency**: Every hour (on the hour)
**Command**: `python3 scripts/cn_market_brief.py --push`
**Push Target**: Feishu private chat
**Content**: ≤140 char brief

```json
{
  "schedule": {"kind": "cron", "expr": "0 * * * *"},
  "delivery": {"mode": "none"}
}
```

### Configuration Notes

- ✅ **delivery.mode = "none"** — Scripts handle Feishu push directly
- ✅ **Ensure `.env.feishu` is configured** with FEISHU_APP_ID, FEISHU_APP_SECRET, FEISHU_USER_OPEN_ID
- ✅ **Feishu bot must be added** to target user/group

### Manual Testing

```bash
python3 scripts/news_monitor_fast.py --no-ai --interval 60 --threshold 4
python3 scripts/cn_market_brief.py --push
```

## Disclaimer

⚠️ **NOT FINANCIAL ADVICE.** For informational purposes only. Consult a licensed financial advisor before making investment decisions.

---

# 中文版本

**⚠️ 需要安装**: 本技能需要 Python 3.10+、uv 包管理器和可选依赖。详见下方安装说明。

**📦 源代码**: https://github.com/ZhenRobotics/openclaw-research-analyst

[English](#openclaw-research-analyst-v10) | **中文**

使用 8 维度分析系统分析**美股、A 股、港股**和**加密货币**，提供**中国市场多源报告**（东方财富/新浪/财联社/腾讯/同花顺）、投资组合管理、监控列表、警报、股息分析和**病毒式趋势检测**。

---

## 📦 安装与依赖

### 必需
- **Python 3.10+** - 核心运行环境
- **uv** - Python 包管理器 (`brew install uv` 或访问 https://github.com/astral-sh/uv)
- **Git** - 用于克隆仓库

### 可选
- **bird CLI** - Twitter/X 集成 (`npm install -g @steipete/bird`)
- **环境变量** (仅 Twitter/X 功能需要):
  - `AUTH_TOKEN` - X.com 认证令牌
  - `CT0` - X.com CT0 令牌

### 安装步骤
```bash
# 从 GitHub 克隆
git clone https://github.com/ZhenRobotics/openclaw-research-analyst.git
cd openclaw-research-analyst

# 安装 Python 依赖
uv sync

# 验证安装
uv run scripts/stock_analyzer.py --help
```

### 安全说明
- ✅ 所有源代码可在 GitHub 查看（已验证）
- ✅ 核心功能无需凭证
- ✅ Twitter/X 凭证仅存储在本地 .env 文件
- ✅ 所有 API 调用使用公开端点（Yahoo Finance、CoinGecko 等）

## 核心功能

- 📊 **8 维度分析** — 综合股票评分（盈利、基本面、分析师、动量、情绪、板块、市场、历史）
- 💰 **股息分析** — 收益率、派息比率、5 年增长率、安全评分
- 📈 **投资组合管理** — 追踪持仓、盈亏、集中度警告
- ⏰ **监控列表 + 警报** — 目标价、止损、信号变化
- 🔥 **热点扫描器** — 多源病毒式趋势检测（CoinGecko、Google News、Twitter/X）
- 🔮 **传闻检测器** — M&A、内部交易、分析师行动的早期信号
- 🌏 **中国市场** — A 股和港股数据（东方财富、新浪、财联社、腾讯、同花顺）
- 🪙 **加密货币支持** — 前 20 大加密货币，含 BTC 相关性
- ⚡ **快速模式** — 跳过慢速分析以快速检查

## 快速命令

### 股票分析
```bash
# 基础分析
uv run {baseDir}/scripts/stock_analyzer.py AAPL

# 快速模式（跳过内部交易和突发新闻）
uv run {baseDir}/scripts/stock_analyzer.py AAPL --fast

# 比较多个股票
uv run {baseDir}/scripts/stock_analyzer.py AAPL MSFT GOOGL

# 加密货币
uv run {baseDir}/scripts/stock_analyzer.py BTC-USD ETH-USD
```

### 股息分析
```bash
# 分析股息
uv run {baseDir}/scripts/dividend_analyzer.py JNJ

# 比较股息股票
uv run {baseDir}/scripts/dividend_analyzer.py JNJ PG KO MCD --output json
```

**股息指标：**
- 股息率与年度派息
- 派息比率（安全/适中/高/不可持续）
- 5 年股息增长率（CAGR）
- 连续增长年数
- 安全评分（0-100）
- 收益评级（优秀/良好/适中/差）

### 监控列表 + 警报
```bash
# 添加到监控列表
uv run {baseDir}/scripts/watchlist_manager.py add AAPL

# 设置目标价警报
uv run {baseDir}/scripts/watchlist_manager.py add AAPL --target 200

# 设置止损警报
uv run {baseDir}/scripts/watchlist_manager.py add AAPL --stop 150

# 检查触发的警报
uv run {baseDir}/scripts/watchlist_manager.py check
```

**警报类型：**
- 🎯 **目标价触发** — 价格 >= 目标价
- 🛑 **止损触发** — 价格 <= 止损价
- 📊 **信号变化** — 买入/持有/卖出信号改变

### 投资组合管理
```bash
# 创建投资组合
uv run {baseDir}/scripts/portfolio_manager.py create "科技投资组合"

# 添加资产
uv run {baseDir}/scripts/portfolio_manager.py add AAPL --quantity 100 --cost 150

# 查看投资组合
uv run {baseDir}/scripts/portfolio_manager.py show
```

### 🌏 中国市场报告
```bash
# 完整中国市场报告（所有数据源）
python3 {baseDir}/scripts/cn_market_report.py

# 东方财富榜单数据
python3 {baseDir}/scripts/cn_market_rankings.py

# 新浪财经实时行情
python3 {baseDir}/scripts/cn_stock_quotes.py 600519  # 贵州茅台

# 财联社财经快讯
python3 {baseDir}/scripts/cn_cls_telegraph.py

# 腾讯财经资金流向
python3 {baseDir}/scripts/cn_tencent_moneyflow.py

# 同花顺个股诊断
python3 {baseDir}/scripts/cn_ths_diagnosis.py 600519
```

**中国数据来源（5 大平台）：**
- 📊 **东方财富** — 市场排行榜、板块分析、热门股票
- 💹 **新浪财经** — 实时行情、A 股与港股
- 📰 **财联社** — 突发财经新闻、市场电报
- 💰 **腾讯财经** — 资金流向分析、资金追踪
- 🔍 **同花顺** — 个股诊断、技术分析

**获取内容：**
- A 股（沪深）和港股数据
- 市场热点榜单和板块轮动
- 实时资金流向追踪
- 突发财经新闻和公告
- 个股技术诊断报告

### 🔥 热点扫描器
```bash
# 完整扫描 - 发现当前热门
python3 {baseDir}/scripts/trend_scanner.py

# 快速扫描（跳过社交媒体）
python3 {baseDir}/scripts/trend_scanner.py --no-social

# JSON 输出用于自动化
python3 {baseDir}/scripts/trend_scanner.py --json
```

**数据来源：**
- 📊 CoinGecko 热门榜 — 前 15 名热门币种
- 📈 CoinGecko 涨跌榜 — 最大涨幅/跌幅
- 📰 Google News — 财经和加密货币新闻
- 📉 Yahoo Finance — 涨幅榜、跌幅榜、最活跃
- 🐦 Twitter/X — 社交媒体情绪（需要认证）

### 🔮 传闻扫描器
```bash
# 发现早期信号、并购传闻、内部交易
python3 {baseDir}/scripts/rumor_detector.py
```

**发现内容：**
- 🏢 **并购传闻** — 合并、收购、收购要约
- 👔 **内部交易** — CEO/董事买入/卖出
- 📊 **分析师行动** — 升级、降级、目标价变化
- 🐦 **Twitter 传言** — "据说..."、"有消息称..."、"传闻"
- ⚖️ **SEC 活动** — 调查、文件

## 分析维度

### 股票（8 个维度）
| 维度 | 权重 | 描述 |
|------|------|------|
| 盈利惊喜 | 30% | EPS 超预期/低于预期 |
| 基本面 | 20% | 市盈率、利润率、增长率 |
| 分析师情绪 | 20% | 评级、目标价 |
| 历史模式 | 10% | 过往盈利反应 |
| 市场背景 | 10% | VIX、SPY/QQQ 趋势 |
| 板块 | 15% | 相对强度 |
| 动量 | 15% | RSI、52 周区间 |
| 情绪 | 10% | 恐惧贪婪、空头、内部交易 |

### 加密货币（3 个维度）
- 市值与分类
- BTC 相关性（30 天）
- 动量（RSI、区间）

## 性能选项

| 参数 | 效果 | 速度 |
|------|------|------|
| (默认) | 完整分析 | 60-120 秒 |
| `--no-insider` | 跳过 SEC EDGAR | 50-90 秒 |
| `--fast` | 跳过内部交易 + 新闻 | 45-75 秒 |

## 支持的加密货币（前 20）

BTC, ETH, BNB, SOL, XRP, ADA, DOGE, AVAX, DOT, MATIC, LINK, ATOM, UNI, LTC, BCH, XLM, ALGO, VET, FIL, NEAR

（使用 `-USD` 后缀：`BTC-USD`、`ETH-USD`）

## ⏰ 自动化推送配置

### 定时任务设置

通过定时任务实现实时市场更新和新闻监控：

#### 1. 重大新闻实时监控

**频率**：每 5 分钟
**命令**：`python3 scripts/news_monitor_fast.py --no-ai --interval 300 --threshold 4`
**推送目标**：飞书私聊
**触发条件**：重要性 ≥ 4

```json
{
  "schedule": {"kind": "every", "everyMs": 300000},
  "delivery": {"mode": "none"}
}
```

#### 2. A 股市场每小时更新

**频率**：每小时整点
**命令**：`python3 scripts/cn_market_brief.py --push`
**推送目标**：飞书私聊
**内容**：≤140 字市场简报

```json
{
  "schedule": {"kind": "cron", "expr": "0 * * * *"},
  "delivery": {"mode": "none"}
}
```

### 配置说明

- ✅ **delivery.mode = "none"** — 脚本自行处理飞书推送
- ✅ **确保 `.env.feishu` 已配置**，包含 FEISHU_APP_ID、FEISHU_APP_SECRET、FEISHU_USER_OPEN_ID
- ✅ **飞书机器人已添加**到目标用户/群组

### 手动测试

```bash
python3 scripts/news_monitor_fast.py --no-ai --interval 60 --threshold 4
python3 scripts/cn_market_brief.py --push
```

## 免责声明

⚠️ **非投资建议。** 仅供参考。投资前请咨询持牌财务顾问。

---

## 📞 Support & Contact | 技术支持与联系方式

### Official Maintenance Partner | 官方维护合作伙伴

For technical support, feature requests, or collaboration inquiries:

技术支持、功能需求或合作咨询，请联系：

**闲鱼ID: 专注人工智能的黄纪恩学长**
