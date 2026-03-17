---
name: portfolio
description: "Track investment holdings. Analyze allocation, calculate returns, and generate rebalance suggestions."
version: "3.2.0"
author: BytesAgain
homepage: https://bytesagain.com
source: https://github.com/bytesagain/ai-skills
tags:
  - portfolio
  - investment
  - finance
  - stocks
  - allocation
  - rebalance
---

# Portfolio Skill

Manage investment holdings, analyze allocation, rebalance, and track performance.

## Commands

### add

Add a position to the portfolio.

```bash
bash scripts/script.sh add <ticker> <quantity> <price> [--date YYYY-MM-DD]
```

### remove

Remove a position from the portfolio.

```bash
bash scripts/script.sh remove <ticker> [--quantity <num>]
```

### list

Display all current holdings.

```bash
bash scripts/script.sh list [--format table|json|csv]
```

### analyze

Analyze portfolio allocation by asset.

```bash
bash scripts/script.sh analyze [--by ticker|sector] [--format table|json]
```

### rebalance

Generate rebalance suggestions against target weights.

```bash
bash scripts/script.sh rebalance [--target <ticker:weight,...>] [--threshold <pct>]
```

### performance

Calculate portfolio returns.

```bash
bash scripts/script.sh performance [--period 1d|1w|1m|3m|1y|all] [--format table|json]
```

## Output

All commands print to stdout. Portfolio data is stored in `~/.portfolio/holdings.json`. Use `--format json` for machine-readable output where supported.


## Requirements
- bash 4+
- python3 (standard library only)

## Feedback

Questions or suggestions? → [https://bytesagain.com/feedback/](https://bytesagain.com/feedback/)

---

Powered by BytesAgain | bytesagain.com
