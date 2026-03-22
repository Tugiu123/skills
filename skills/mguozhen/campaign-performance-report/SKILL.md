---
name: campaign-performance-report
description: "Multi-channel marketing performance agent. Pulls together Meta, Google, email, and organic data into a unified weekly report with AI executive commentary — eliminating manual cross-platform data assembly. Triggers: campaign report, marketing report, multi channel report, weekly marketing report, meta report, google ads report, performance report, marketing performance, channel report, ad performance, weekly report marketing, paid media report"
allowed-tools: Bash
metadata:
  openclaw:
    homepage: https://github.com/mguozhen/campaign-performance-report
---

# Campaign Performance Report

AI-powered multi-channel marketing performance agent — unifies Meta, Google, email, and organic data into a single weekly report with executive-level AI commentary.

Paste your numbers from each platform dashboard, describe your results verbally, or upload CSV exports. The agent normalizes metrics across channels, surfaces anomalies, compares week-over-week, and delivers a 3-bullet executive summary: win, miss, and action.

## Commands

```
report setup                       # configure channels, KPIs, and report preferences
report weekly                      # generate full unified weekly performance report
report by channel                  # break down performance per channel side-by-side
report compare weeks               # compare current week vs. prior week or custom date range
report meta                        # focus report on Meta (Facebook/Instagram) data only
report google                      # focus report on Google Ads data only
report email                       # focus report on email campaign metrics only
report organic                     # focus report on organic search and social metrics only
report save                        # save this week's report to ~/campaign-reports/
```

## What Data to Provide

The agent works with:
- **Manual paste** — copy numbers directly from Meta Ads Manager, Google Ads, Klaviyo, GA4, etc.
- **CSV export** — paste rows from platform exports (impressions, clicks, spend, conversions)
- **Verbal description** — "Meta spend $4,200, 180 conversions, ROAS 3.2; Google $3,100, 210 conversions, ROAS 4.1"
- **Partial data** — report on whichever channels you have; agent flags missing channels

No API keys needed. No integrations required.

## Workspace

Creates `~/campaign-reports/` containing:
- `memory.md` — saved channel configs, KPI targets, and account baselines
- `reports/` — weekly reports saved as markdown (weekly-YYYY-MM-DD.md)
- `data/` — raw channel data snapshots for trend tracking

## Analysis Framework

### 1. Channel Data Input and Normalization
- Accept raw numbers from Meta Ads Manager, Google Ads, email platform (Klaviyo/Mailchimp), GA4 organic
- Normalize to unified metric set: impressions, clicks, spend, conversions, revenue, CTR, CVR, CPC, ROAS
- Flag mismatched attribution windows across platforms (Meta 7-day click vs. Google last-click)
- Handle zero-spend channels (organic, email) using CPM-equivalent cost estimates when available

### 2. Cross-Channel ROAS Comparison
- Calculate blended ROAS across all paid channels: Total Revenue / Total Paid Spend
- Rank channels by ROAS, CVR, and CPA
- Identify highest and lowest efficiency channels
- Flag channels where ROAS is below break-even threshold (1.0 for revenue, varies by margin)

### 3. Spend Allocation Efficiency
- Show spend distribution across channels as percentages
- Compare spend share vs. conversion share per channel (over/under-indexed channels)
- Flag channels absorbing budget without proportional returns
- Suggest reallocation direction (not specific amounts — flag for human review)

### 4. Week-over-Week Trend Analysis
- Calculate delta for every key metric vs. prior week
- Display direction arrows (up/down) and percentage change
- Compute 4-week rolling average as baseline for trend context
- Flag metrics moving in opposite direction from spend (spend up, conversions down = efficiency drop)

### 5. Anomaly Flagging
- Flag any metric with greater than 20% week-over-week delta (positive or negative)
- CPM spikes greater than 30% may signal audience saturation or auction pressure
- CTR drops greater than 20% with stable spend may indicate creative fatigue
- Conversion rate drops greater than 15% with stable traffic may indicate landing page issues

### 6. Budget Pacing Check
- Compare actual spend-to-date vs. expected pacing for the month
- Flag overpace (greater than 110% of expected) and underpace (less than 90% of expected)
- Estimate end-of-month projected spend at current run rate

### 7. AI Executive Summary
- 3-bullet format always: Win (best performance signal this week), Miss (biggest underperformance), Action (single highest-priority recommendation)
- Keep each bullet to one sentence — built for executive skimming
- Cite specific numbers in each bullet (no vague language)

## Output Format

Every weekly report outputs:
1. **Executive Summary** — Win / Miss / Action (3 bullets, one sentence each)
2. **Channel Scorecard** — table with all channels, all key metrics, week-over-week delta
3. **Anomalies** — flagged metrics exceeding 20% delta with likely cause
4. **Budget Pacing** — spend status vs. monthly plan
5. **Top Performers** — best-performing campaigns or content across all channels
6. **Actions Queue** — prioritized list of items requiring human decisions
7. **Next Week Focus** — 2-3 optimization priorities for the coming week

## Rules

1. Never fabricate platform data — if a channel's data is missing, mark it as "not provided" rather than estimating
2. Always note attribution window differences between platforms when comparing ROAS across channels
3. Flag anomalies with a likely cause hypothesis, not just the raw number
4. Distinguish between spend-driven metric changes (more budget = more impressions) vs. efficiency changes (same spend, fewer results)
5. Save reports to `~/campaign-reports/reports/` using the filename format `weekly-YYYY-MM-DD.md`
6. When comparing weeks, require at least 7 full days of data per period before drawing trend conclusions
7. Never recommend pausing a channel based on a single week of data — flag for review instead
