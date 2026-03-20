---
version: "3.0.0"
name: Liquidity Monitor
description: "Monitor DEX pools in real time with impermanent loss and LP yield estimates. Use when tracking pool depth, estimating IL, comparing yields across DEXes."
author: BytesAgain
homepage: https://bytesagain.com
source: https://github.com/bytesagain/ai-skills
---

# Liquidity Monitor

Liquidity Monitor is a data processing and analysis toolkit for querying, importing, exporting, transforming, validating, and visualizing datasets from the terminal. It provides 10 core commands for working with structured data, plus built-in history logging for full traceability. All operations are local — no external APIs or network connections required.

## Commands

| Command | Description |
|---------|-------------|
| `liquidity-monitor query <args>` | Query data from the local data store. Logs the query to history for auditing. |
| `liquidity-monitor import <file>` | Import a data file into the local store. Accepts any file path as input. |
| `liquidity-monitor export <dest>` | Export processed results to a specified destination (defaults to stdout). |
| `liquidity-monitor transform <src> <dst>` | Transform data from one format/structure to another. |
| `liquidity-monitor validate <args>` | Validate data against the built-in schema. Reports schema compliance status. |
| `liquidity-monitor stats <args>` | Display basic statistics — total record count from the data log. |
| `liquidity-monitor schema <args>` | Show the current data schema. Default fields: `id, name, value, timestamp`. |
| `liquidity-monitor sample <args>` | Preview the first 5 records from the data store, or "No data" if empty. |
| `liquidity-monitor clean <args>` | Clean and deduplicate the data store. |
| `liquidity-monitor dashboard <args>` | Quick dashboard showing total record count and summary metrics. |
| `liquidity-monitor help` | Show help with all available commands. |
| `liquidity-monitor version` | Print version string (`liquidity-monitor v2.0.0`). |

## Data Storage

All data is stored locally in `~/.local/share/liquidity-monitor/` (override with `LIQUIDITY_MONITOR_DIR` or `XDG_DATA_HOME` environment variables).

**Directory structure:**
```
~/.local/share/liquidity-monitor/
├── data.log         # Main data store (line-based records)
└── history.log      # Unified activity log with timestamps
```

Every command logs its action to `history.log` with a timestamp (`MM-DD HH:MM`) for full traceability. The main data file `data.log` holds all imported and queried records.

## Requirements

- Bash (with `set -euo pipefail`)
- Standard Unix utilities: `date`, `wc`, `head`, `du`, `echo`
- No external dependencies, databases, or API keys required
- Optional: Set `LIQUIDITY_MONITOR_DIR` to customize the data directory location

## When to Use

1. **Importing and querying datasets** — Pull in CSV, log, or structured data files and run quick queries against them from the terminal without spinning up a database.
2. **Data validation workflows** — Validate incoming data against the built-in schema before processing to catch format issues early.
3. **Data transformation pipelines** — Transform data between formats or structures as part of an ETL-like workflow, all within bash.
4. **Quick dashboard views** — Get instant record counts and summary metrics via `dashboard` or `stats` without writing custom scripts.
5. **Data cleanup and deduplication** — Use `clean` to remove duplicate records and normalize the data store before exporting or further analysis.

## Examples

```bash
# Import a data file
liquidity-monitor import sales_data.csv

# Query the data store
liquidity-monitor query "region=APAC"

# View schema
liquidity-monitor schema

# Preview first 5 records
liquidity-monitor sample

# Get basic statistics
liquidity-monitor stats

# Transform data
liquidity-monitor transform raw.csv cleaned.csv

# Validate data integrity
liquidity-monitor validate

# Quick dashboard
liquidity-monitor dashboard

# Export results
liquidity-monitor export results.json

# Clean and deduplicate
liquidity-monitor clean
```

---

Powered by BytesAgain | bytesagain.com | hello@bytesagain.com
