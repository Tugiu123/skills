# 📈 OpenClaw Research Analyst v1.3.0
# 📈 OpenClaw 研究分析师 v1.3.0

**English** | [中文](#中文版本)

> AI-powered stock & crypto research with 8-dimension analysis, **AI news monitoring**, **one-click brief**, **smart scheduling**, **Feishu push**, portfolio tracking, and trend detection.

## ✨ What's New in v1.3.0

**🎉 Major Update: AI News Monitoring System**

#### Real-time Financial News (实时财经新闻)
- **Auto-Collection** - 财联社 + 东方财富 (60-300s interval)
- **AI Classification** - BULLISH/BEARISH/NEUTRAL (100% test accuracy)
- **Smart Push** - Auto-push major news (importance ≥4) to Feishu
- **Fast Mode** - 30-40s end-to-end latency (60s interval)

#### Quick Start (快速开始)
```bash
# Keyword mode (no AI required, recommended)
./scripts/quick_start_ai.sh monitor-keyword

# Fast mode (60s interval)
python3 scripts/news_monitor_fast.py --no-ai --interval 60 --threshold 4
```

#### API Testing Suite (API 测试套件)
- **9-Point Tests** - Functional, performance, reliability, end-to-end
- **Test Results** - 66.7% pass rate, 100% keyword accuracy
- **Automated Reports** - JSON format with detailed metrics

#### New Docs (新文档)
- **AI_NEWS_SYSTEM_GUIDE.md** - Complete workflow (4 stages)
- **API_TESTING_GUIDE.md** - Testing methodology
- **API_TEST_RESULTS_ANALYSIS.md** - Performance analysis

**📚 Full Release Notes:** [RELEASE_NOTES_v1.3.0.md](https://github.com/ZhenRobotics/openclaw-research-analyst/blob/main/RELEASE_NOTES_v1.3.0.md)

---

## 🔙 Previous Updates

**v1.2.0:**

**🎉 New Features:**
- **📊 One-Click Brief** - Ultra-fast market summary (≤140 chars, ~2 seconds)
- **⏰ Smart Scheduling** - Intelligent trading-hours cron jobs
  - Intraday: Every 10 min (Mon-Fri 09:30-15:00)
  - EOD report: Once at 15:05
  - Auto-skip weekends

**📚 Docs:** [SMART_SCHEDULING.md](https://github.com/ZhenRobotics/openclaw-research-analyst/blob/main/SMART_SCHEDULING.md)

---

**v1.1.0:**
- **📱 Feishu Push Integration** - Auto-push to Feishu (飞书推送集成)
- **🚀 Async Optimization** - 70-90% faster (异步优化，性能提升 70-90%)

[![ClawHub Downloads](https://img.shields.io/badge/ClawHub-1500%2B%20downloads-blue)](https://clawhub.ai)
[![OpenClaw Skill](https://img.shields.io/badge/OpenClaw-Skill-green)](https://openclaw.ai)
[![GitHub](https://img.shields.io/badge/GitHub-openclaw--research--analyst-black)](https://github.com/ZhenRobotics/openclaw-research-analyst)

---

## Features

| Feature | Description |
|---------|-------------|
| **8-Dimension Analysis** | Earnings, fundamentals, analysts, momentum, sentiment, sector, market, history |
| **🆕 Feishu Push** | Auto-push China market reports to Feishu private chat or group (飞书推送) |
| **🆕 Async Reports** | 70-90% faster with parallel data fetching (异步并行优化) |
| **Crypto Support** | Top 20 cryptos with market cap, BTC correlation, momentum |
| **Portfolio Management** | Track holdings, P&L, concentration warnings |
| **Watchlist + Alerts** | Price targets, stop losses, signal changes |
| **Dividend Analysis** | Yield, payout, growth, safety score |
| **Hot Scanner** | Multi-source viral trend detection (CoinGecko, Google News, Twitter/X) |
| **Rumor Detector** | Early signal detection for M&A, insider trades, analyst actions |
| **Risk Detection** | Geopolitical, earnings timing, overbought, risk-off |
| **China Markets** | A-share & Hong Kong stock data (东方财富, 新浪, 财联社, 腾讯, 同花顺) |
| **Breaking News** | Crisis keyword scanning (last 24h) |

## Quick Start

### Analyze Stocks
```bash
uv run scripts/stock_analyzer.py AAPL
uv run scripts/stock_analyzer.py AAPL MSFT GOOGL
uv run scripts/stock_analyzer.py AAPL --fast  # Skip slow analyses
```

### Analyze Crypto
```bash
uv run scripts/stock_analyzer.py BTC-USD
uv run scripts/stock_analyzer.py ETH-USD SOL-USD
```

### Dividend Analysis
```bash
uv run scripts/dividend_analyzer.py JNJ PG KO
```

### Watchlist
```bash
uv run scripts/watchlist_manager.py add AAPL --target 200 --stop 150
uv run scripts/watchlist_manager.py list
uv run scripts/watchlist_manager.py check --notify
```

### Portfolio
```bash
uv run scripts/portfolio_manager.py create "My Portfolio"
uv run scripts/portfolio_manager.py add AAPL --quantity 100 --cost 150
uv run scripts/portfolio_manager.py show
```

### 🔥 Hot Scanner
```bash
# Full scan with all sources
python3 scripts/trend_scanner.py

# Fast scan (skip social media)
python3 scripts/trend_scanner.py --no-social

# JSON output for automation
python3 scripts/trend_scanner.py --json
```

### 🔮 Rumor Scanner
```bash
# Find early signals before mainstream news
python3 scripts/rumor_detector.py
```

## Analysis Dimensions

### Stocks (8 dimensions)
1. **Earnings Surprise** (30%) — EPS beat/miss
2. **Fundamentals** (20%) — P/E, margins, growth, debt
3. **Analyst Sentiment** (20%) — Ratings, price targets
4. **Historical Patterns** (10%) — Past earnings reactions
5. **Market Context** (10%) — VIX, SPY/QQQ trends
6. **Sector Performance** (15%) — Relative strength
7. **Momentum** (15%) — RSI, 52-week range
8. **Sentiment** (10%) — Fear/Greed, shorts, insiders

### Crypto (3 dimensions)
- Market Cap & Category
- BTC Correlation (30-day)
- Momentum (RSI, range)

## Dividend Metrics

| Metric | Description |
|--------|-------------|
| Yield | Annual dividend / price |
| Payout Ratio | Dividend / EPS |
| 5Y Growth | CAGR of dividend |
| Consecutive Years | Years of increases |
| Safety Score | 0-100 composite |
| Income Rating | Excellent → Poor |

## Risk Detection

- ⚠️ Pre-earnings warning (< 14 days)
- ⚠️ Post-earnings spike (> 15% in 5 days)
- ⚠️ Overbought (RSI > 70 + near 52w high)
- ⚠️ Risk-off mode (GLD/TLT/UUP rising)
- ⚠️ Geopolitical keywords (Taiwan, China, etc.)
- ⚠️ Breaking news alerts

## Performance Options

| Flag | Speed | Description |
|------|-------|-------------|
| (default) | 60-120s | Full analysis with all data sources |
| `--no-insider` | 50-90s | Skip SEC EDGAR insider trading |
| `--fast` | 45-75s | Skip insider trading + breaking news |

## Data Sources

- [Yahoo Finance](https://finance.yahoo.com) — Prices, fundamentals, movers
- [CoinGecko](https://coingecko.com) — Crypto trending, market data
- [CNN Fear & Greed](https://money.cnn.com/data/fear-and-greed/) — Sentiment
- [SEC EDGAR](https://www.sec.gov/edgar) — Insider trading
- [Google News RSS](https://news.google.com) — Breaking news
- [Twitter/X](https://x.com) — Social sentiment (via bird CLI)

## ⏰ Automated Push Configuration

### Cron Job Setup

Automate real-time market updates and news monitoring with scheduled tasks:

#### 1. Major News Real-time Monitoring

**Frequency**: Every 5 minutes
**Command**: `python3 scripts/news_monitor_fast.py --no-ai --interval 300 --threshold 4`
**Push Target**: Feishu private chat
**Trigger Condition**: Importance ≥ 4

```bash
# OpenClaw Gateway cron configuration
{
  "schedule": {
    "kind": "every",
    "everyMs": 300000  # 5 minutes
  },
  "delivery": {
    "mode": "none"  # Script handles push internally
  }
}
```

#### 2. A-Share Market Hourly Updates

**Frequency**: Every hour (on the hour)
**Command**: `python3 scripts/cn_market_brief.py --push`
**Push Target**: Feishu private chat
**Content**: ≤140 char market brief

```bash
# OpenClaw Gateway cron configuration
{
  "schedule": {
    "kind": "cron",
    "expr": "0 * * * *"  # Every hour at minute 0
  },
  "delivery": {
    "mode": "none"  # Script handles push internally
  }
}
```

### Configuration Notes

- ✅ **delivery.mode = "none"** — Scripts handle Feishu push directly
- ✅ **Ensure `.env.feishu` is configured** with:
  - `FEISHU_APP_ID`
  - `FEISHU_APP_SECRET`
  - `FEISHU_USER_OPEN_ID` or `FEISHU_WEBHOOK_URL`
- ✅ **Feishu bot must be added** to target user/group
- ✅ **Working directory** should be the skill installation path

### Manual Testing

```bash
# Test news monitoring (runs once)
python3 scripts/news_monitor_fast.py --no-ai --interval 60 --threshold 4

# Test market brief
python3 scripts/cn_market_brief.py --push
```

## Installation

### Prerequisites
- Python 3.10+
- [uv](https://github.com/astral-sh/uv) package manager

### Install via npm
```bash
npm install -g openclaw-research-analyst
```

### Install from source
```bash
git clone https://github.com/ZhenRobotics/openclaw-research-analyst.git
cd openclaw-research-analyst
```

## Disclaimer

⚠️ **NOT FINANCIAL ADVICE.** For informational purposes only. Consult a licensed financial advisor before making investment decisions.

---

## 📞 Support & Contact

### Official Maintenance Partner | 官方维护合作伙伴

For technical support, feature requests, or collaboration inquiries:

技术支持、功能需求或合作咨询，请联系：

**闲鱼ID: 专注人工智能的黄纪恩学长**

---

Built for [OpenClaw](https://openclaw.ai) 🦞 | [ClawHub](https://clawhub.ai)

---

# 中文版本

[English](#-openclaw-research-analyst-v63) | **中文**

> AI 驱动的股票与加密货币研究工具，提供 8 维度分析、投资组合追踪和趋势检测。

[![ClawHub 下载](https://img.shields.io/badge/ClawHub-1500%2B%20下载-blue)](https://clawhub.ai)
[![OpenClaw Skill](https://img.shields.io/badge/OpenClaw-Skill-green)](https://openclaw.ai)
[![GitHub](https://img.shields.io/badge/GitHub-openclaw--research--analyst-black)](https://github.com/ZhenRobotics/openclaw-research-analyst)

---

## 功能特性

| 功能 | 描述 |
|------|------|
| **8 维度分析** | 盈利、基本面、分析师、动量、情绪、板块、市场、历史 |
| **加密货币支持** | 前 20 大加密货币，包含市值、BTC 相关性、动量 |
| **投资组合管理** | 追踪持仓、盈亏、集中度警告 |
| **监控列表 + 警报** | 目标价、止损、信号变化 |
| **股息分析** | 收益率、派息、增长、安全评分 |
| **热点扫描器** | 多源病毒式趋势检测（CoinGecko、Google News、Twitter/X）|
| **传闻检测器** | M&A、内部交易、分析师行动的早期信号检测 |
| **风险检测** | 地缘政治、盈利时机、超买、风险规避 |
| **中国市场** | A 股和港股数据（东方财富、新浪、财联社、腾讯、同花顺）|
| **突发新闻** | 危机关键词扫描（最近 24 小时）|

## 快速开始

### 分析股票
```bash
uv run scripts/stock_analyzer.py AAPL
uv run scripts/stock_analyzer.py AAPL MSFT GOOGL
uv run scripts/stock_analyzer.py AAPL --fast  # 跳过慢速分析
```

### 分析加密货币
```bash
uv run scripts/stock_analyzer.py BTC-USD
uv run scripts/stock_analyzer.py ETH-USD SOL-USD
```

### 股息分析
```bash
uv run scripts/dividend_analyzer.py JNJ PG KO
```

### 监控列表
```bash
uv run scripts/watchlist_manager.py add AAPL --target 200 --stop 150
uv run scripts/watchlist_manager.py list
uv run scripts/watchlist_manager.py check --notify
```

### 投资组合
```bash
uv run scripts/portfolio_manager.py create "我的投资组合"
uv run scripts/portfolio_manager.py add AAPL --quantity 100 --cost 150
uv run scripts/portfolio_manager.py show
```

### 🔥 热点扫描器
```bash
# 包含所有来源的完整扫描
python3 scripts/trend_scanner.py

# 快速扫描（跳过社交媒体）
python3 scripts/trend_scanner.py --no-social

# JSON 输出用于自动化
python3 scripts/trend_scanner.py --json
```

### 🔮 传闻扫描器
```bash
# 在主流新闻之前发现早期信号
python3 scripts/rumor_detector.py
```

## 分析维度

### 股票（8 个维度）
1. **盈利惊喜** (30%) — EPS 超预期/低于预期
2. **基本面** (20%) — 市盈率、利润率、增长率、债务
3. **分析师情绪** (20%) — 评级、目标价
4. **历史模式** (10%) — 过往盈利反应
5. **市场背景** (10%) — VIX、SPY/QQQ 趋势
6. **板块表现** (15%) — 相对强度
7. **动量** (15%) — RSI、52 周区间
8. **情绪** (10%) — 恐惧贪婪、空头、内部交易

### 加密货币（3 个维度）
- 市值与分类
- BTC 相关性（30 天）
- 动量（RSI、区间）

## 股息指标

| 指标 | 描述 |
|------|------|
| 收益率 | 年度股息 / 价格 |
| 派息比率 | 股息 / 每股收益 |
| 5 年增长率 | 股息的复合年增长率 |
| 连续年数 | 连续增长的年数 |
| 安全评分 | 0-100 综合评分 |
| 收益评级 | 优秀 → 差 |

## 风险检测

- ⚠️ 盈利前警告（< 14 天）
- ⚠️ 盈利后飙升（5 天内 > 15%）
- ⚠️ 超买（RSI > 70 + 接近 52 周高点）
- ⚠️ 风险规避模式（GLD/TLT/UUP 上涨）
- ⚠️ 地缘政治关键词（台湾、中国等）
- ⚠️ 突发新闻警报

## 性能选项

| 参数 | 速度 | 描述 |
|------|------|------|
| (默认) | 60-120 秒 | 包含所有数据源的完整分析 |
| `--no-insider` | 50-90 秒 | 跳过 SEC EDGAR 内部交易 |
| `--fast` | 45-75 秒 | 跳过内部交易 + 突发新闻 |

## 数据来源

- [Yahoo Finance](https://finance.yahoo.com) — 价格、基本面、涨跌幅
- [CoinGecko](https://coingecko.com) — 加密货币热门榜、市场数据
- [CNN Fear & Greed](https://money.cnn.com/data/fear-and-greed/) — 情绪指数
- [SEC EDGAR](https://www.sec.gov/edgar) — 内部交易
- [Google News RSS](https://news.google.com) — 突发新闻
- [Twitter/X](https://x.com) — 社交情绪（通过 bird CLI）

## ⏰ 自动化推送配置

### 定时任务设置

通过定时任务实现实时市场更新和新闻监控：

#### 1. 重大新闻实时监控

**频率**：每 5 分钟
**命令**：`python3 scripts/news_monitor_fast.py --no-ai --interval 300 --threshold 4`
**推送目标**：飞书私聊
**触发条件**：重要性 ≥ 4

```bash
# OpenClaw Gateway cron 配置
{
  "schedule": {
    "kind": "every",
    "everyMs": 300000  # 5 分钟
  },
  "delivery": {
    "mode": "none"  # 脚本内部处理推送
  }
}
```

#### 2. A 股市场每小时更新

**频率**：每小时整点
**命令**：`python3 scripts/cn_market_brief.py --push`
**推送目标**：飞书私聊
**内容**：≤140 字市场简报

```bash
# OpenClaw Gateway cron 配置
{
  "schedule": {
    "kind": "cron",
    "expr": "0 * * * *"  # 每小时第 0 分钟
  },
  "delivery": {
    "mode": "none"  # 脚本内部处理推送
  }
}
```

### 配置说明

- ✅ **delivery.mode = "none"** — 脚本自行处理飞书推送
- ✅ **确保 `.env.feishu` 已配置**，包含：
  - `FEISHU_APP_ID`
  - `FEISHU_APP_SECRET`
  - `FEISHU_USER_OPEN_ID` 或 `FEISHU_WEBHOOK_URL`
- ✅ **飞书机器人已添加**到目标用户/群组
- ✅ **工作目录**应为 skill 安装路径

### 手动测试

```bash
# 测试新闻监控（运行一次）
python3 scripts/news_monitor_fast.py --no-ai --interval 60 --threshold 4

# 测试市场简报
python3 scripts/cn_market_brief.py --push
```

## 安装

### 前置要求
- Python 3.10+
- [uv](https://github.com/astral-sh/uv) 包管理器

### 通过 npm 安装
```bash
npm install -g openclaw-research-analyst
```

### 从源码安装
```bash
git clone https://github.com/ZhenRobotics/openclaw-research-analyst.git
cd openclaw-research-analyst
```

## 免责声明

⚠️ **非投资建议。** 仅供参考。投资前请咨询持牌财务顾问。

---

为 [OpenClaw](https://openclaw.ai) 🦞 | [ClawHub](https://clawhub.ai) 构建
