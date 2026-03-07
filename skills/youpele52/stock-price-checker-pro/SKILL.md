---
name: stock-price-checker-pro
description: Check stock prices using yfinance library. No API key required.
homepage: https://finance.yahoo.com
metadata: {"clawdbot":{"emoji":"📈","requires":{"bins":["uv"]}}}
---

# Skill: Stock Price Checker


## Prerequisites

- `uv` is installed (the script will automatically handle dependency installation and execution)


## When to use
- The user wants to check the current stock price of a company, ETF, or index.
- The user wants related market data (previous close, market cap, volume) and recent news or corporate events.

## Step-by-step approach
- When given a company name, first locate the corresponding stock ticker symbol using Yahoo Finance or another reliable service.
- If the user doesn't specify a currency, assume USD for stock prices. For stocks listed on other exchanges (e.g., German exchanges), use the appropriate ticker (e.g., `NOV.DE`) rather than converting currencies.
- Once the ticker is identified, use the ticker as input to the `src/main.py` script. The script will fetch the current price and related information using the `yfinance` library (for example, `uv run src/main.py AAPL`).

## Usage Examples

**Check NVIDIA stock:**
```bash
uv run src/main.py NVDA
```

**Check VOO (S&P 500 ETF):**
```bash
uv run src/main.py VOO
```

**Check any stock symbol:**
```bash
uv run src/main.py TSLA
uv run src/main.py MSFT
uv run src/main.py AAPL
```

## Output Format

The script prints a human-readable market snapshot to stdout.

### Example Output
```text
NVDA: NVIDIA Corporation
$189.52 ▲$3.05 (1.64%), Prev Close: $186.47
Vol: 112.4M Avg: 98.0M | 115% of avg | Mkt Cap: $4.61T

Today High: $190.10
Today Low:  $185.00

2W High: $195.00
2W Low:  $172.50

1M High: $195.00
1M Low:  $160.00

6M High: $210.00
6M Low:  $120.00

52W High: $212.19
52W Low:  $86.62

Recent News:
1. NVIDIA reports record data center revenue
   Link: https://www.reuters.com/...

Upcoming Events:
1. Earnings Call: 2026-05-01 20:00:00 GMT
```

## Technical Notes
- Uses the `yfinance` library to fetch data from Yahoo Finance.
- No API key required.
- The Python implementation lives under `src/` and is split into `src/main.py`, `src/service.py`, `src/utils.py`, and `src/constants.py` to separate orchestration, data retrieval, formatting helpers, and configuration.
- The script prints formatted text rather than JSON.
- `market_cap`, `volume`, and `avg_volume` may be unavailable for some tickers depending on Yahoo Finance coverage.

## Troubleshooting
- If the stock symbol is invalid or not found, the script will return an error message.
- Some data (like market cap) may be delayed or unavailable for certain tickers (e.g., OTC or very small-cap symbols).
- For international tickers, specify the exchange suffix (e.g., `BMW.DE`) to ensure data is pulled from the correct market.
- If `news` or `events` are empty arrays, it means the script could not find recent items for that symbol.
