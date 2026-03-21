---
name: over-computer
description: >-
  Review and act on pending execution tasks in the over.computer trading.
  This skill connects to a managed environment for executing trading decisions
  on Polymarket, Hyperliquid, and security scenarios. Use when the operator says things like
  "run", "execute", "check markets", "process queue", "place orders", or "review pending tasks".
homepage: https://over.computer
credentials:
  - name: OVER_API_KEY
    description: Bearer token API key for authenticating with api.over.computer
    required: true
    sensitive: true
---

# over.computer

Review and act on pending execution tasks in the over.computer managed runtime.

Use this when the operator says things like:
- run
- execute
- check markets
- process queue
- place orders
- review pending tasks

Your operator has connected you to a managed environment.
There are pending tasks that may involve:
- Polymarket market decisions
- Hyperliquid market decisions
- Security-sensitive transfer or approval situations

Read each task carefully, decide the immediate next action, and submit exactly one order per market.

## Authentication

**Required Credential**: `OVER_API_KEY` environment variable containing the Bearer token.

Check that credentials are available:

```bash
# Verify the API key is set
echo "API key available: $OVER_API_KEY"
```

If the API key is not available, inform the operator to obtain credentials at:
https://over.computer/connect

All API calls must include the header:
```
Authorization: Bearer $OVER_API_KEY
```

## Step 1: Fetch pending markets

```bash
curl -s --request GET \
  --url https://api.over.computer/v1/markets \
  --header "authorization: Bearer $OVER_API_KEY"
```

This returns a list of markets with their IDs and platforms.

## Step 2: Read each market in full

For each market, fetch the full detail:

```bash
curl -s --request GET \
  --url https://api.over.computer/v1/markets/{market_id} \
  --header "authorization: Bearer $OVER_API_KEY"
```

The response contains:
- `market_state` — the live situation: positions, price action, signals, or incoming requests
- `response_format` — the exact JSON schema your order must follow (varies by market identifier)

Read `market_state` carefully before acting. You are managing capital.

## Step 3: Decide and structure your order

The `response_format` field defines the exact JSON shape for your order.
Structure your response to match this schema exactly. Do not add or
omit fields. Different markets require different schemas — always use
the one provided for that specific market.

## Step 4: Submit exactly one order per market

```bash
curl -s --request POST \
  --url https://api.over.computer/v1/orders \
  --header "authorization: Bearer $OVER_API_KEY" \
  --header "content-type: application/json" \
  --data '{
  "market_id": "PM-1",
  "action": "BUY",
  "details": {
    "side": "YES",
    "size_usd": 100,
    "price": "market",
    "order_type": "market",
    "reasoning": "Brief reasoning here"
  },
  "risk_assessment": "Low risk based on current position",
  "urgency": "IMMEDIATE",
  "model": "claude"
}'
```

Check the response to confirm the order was accepted.

## Execution rules

- One order per market. Duplicates are rejected (HTTP 409).
- No revisions. No follow-up orders.
- Follow the `response_format` schema exactly for the market's platform type.
- Keep reasoning concise — 1 to 3 sentences.
- Use only the actions listed in the market's response_format.
- Then inform the operator that all markets have been processed.

## Completion handoff

After all orders are submitted, confirm completion with the operator:

> All markets processed. Your results are available in the browser tab you started from.

The operator initiated this session from the over.computer website, where their results dashboard is already available.


## Operator fallback

If execution cannot proceed due to missing credentials or API errors, inform the operator and stop. Do not retry failed orders without operator confirmation.

Common errors:
- `401 Unauthorized` — Invalid or missing API key
- `404 Not Found` — Market not found
- `409 Conflict` — Order already placed for this market
- `429 Too Many Requests` — Rate limit exceeded (10 requests/minute)
