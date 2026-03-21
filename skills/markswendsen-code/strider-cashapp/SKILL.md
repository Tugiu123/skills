---
name: strider-cashapp
description: Send and receive money via Cash App using Strider Labs MCP connector. Send payments, request money, buy Bitcoin, manage Cash Card. Complete autonomous P2P payments for your AI agent.
metadata:
  openclaw:
    requires:
      bins: ["npx"]
    category: "finance"
    author: "Strider Labs"
    homepage: "https://striderlabs.ai"
---

# Strider Cash App Connector

MCP connector for P2P payments through Cash App — send money, request payments, buy/sell Bitcoin, and manage your Cash Card. Part of the Strider Labs action execution layer for AI agents.

## Installation

```bash
npm install @striderlabs/mcp-cashapp
```

## MCP Configuration

Add to your MCP client configuration (Claude Desktop, Cursor, etc.):

```json
{
  "mcpServers": {
    "cashapp": {
      "command": "npx",
      "args": ["-y", "@striderlabs/mcp-cashapp"]
    }
  }
}
```

## Available Tools

### cashapp.send_payment
Send money to a Cash App user.

**Input Schema:**
```json
{
  "recipient": "string ($cashtag, phone, or email)",
  "amount": "number",
  "note": "string (optional: payment description)"
}
```

**Output:**
```json
{
  "payment_id": "string",
  "status": "string (pending, completed)",
  "recipient": "string",
  "amount": "number"
}
```

### cashapp.request_payment
Request money from a Cash App user.

### cashapp.get_balance
Check Cash App balance.

**Output:**
```json
{
  "balance": "number",
  "bitcoin_balance": "number",
  "bitcoin_value_usd": "number"
}
```

### cashapp.get_transactions
Get recent transaction history.

### cashapp.buy_bitcoin
Purchase Bitcoin with Cash App balance.

**Input Schema:**
```json
{
  "amount_usd": "number"
}
```

### cashapp.sell_bitcoin
Sell Bitcoin for USD.

### cashapp.cash_out
Transfer balance to linked bank account.

**Input Schema:**
```json
{
  "amount": "number",
  "speed": "string (standard or instant)"
}
```

### cashapp.enable_boosts
Activate Cash Card boosts for discounts.

## Authentication

First use triggers OAuth with Cash App account. Cash Card required for some features. Tokens stored encrypted per-user.

## Usage Examples

**Pay someone:**
```
Send $25 to $johnsmith on Cash App for lunch
```

**Request payment:**
```
Request $40 from $sarah on Cash App for the tickets
```

**Buy Bitcoin:**
```
Buy $100 of Bitcoin on Cash App
```

**Cash out:**
```
Transfer my Cash App balance to my bank with instant deposit
```

## Error Handling

| Code | Meaning | Action |
|------|---------|--------|
| AUTH_EXPIRED | Session expired | Re-authenticate |
| INSUFFICIENT_FUNDS | Balance too low | Add funds |
| USER_NOT_FOUND | Invalid $cashtag | Verify recipient |
| INSTANT_LIMIT | Instant deposit limit | Use standard |

## Use Cases

- Quick payments: instant P2P transfers
- Bitcoin: simple crypto buying and selling
- Boosts: save money with Cash Card discounts
- Bill splitting: request from multiple people

## Links

- npm: https://npmjs.com/package/@striderlabs/mcp-cashapp
- Strider Labs: https://striderlabs.ai
