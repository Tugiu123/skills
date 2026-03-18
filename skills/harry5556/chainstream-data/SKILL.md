---
name: chainstream-data
description: Query and analyze on-chain data across Solana, BSC, Base, Ethereum. Use when searching tokens, analyzing wallet PnL, tracking market trends, monitoring real-time trades, assessing token risk, or building data pipelines. Also covers KYT compliance, webhooks, and WebSocket streaming.
metadata: {"clawdbot":{"emoji":"📊","requires":{"anyBins":["curl"]},"os":["linux","darwin","win32"]}}
---

# ChainStream Data

On-chain big data infrastructure for AI agents. Access real-time trading data, token analytics, wallet profiling, and market intelligence across Solana, BSC, Base, and Ethereum via 80+ REST API endpoints, multi-language SDKs, and WebSocket streaming.

- **Base URL**: `https://api.chainstream.io`
- **WebSocket**: `wss://realtime-dex.chainstream.io/connection/websocket`
- **Documentation**: [docs.chainstream.io](https://docs.chainstream.io)
- **MCP Server**: `https://mcp.chainstream.io/mcp` (streamable-http)

## When to Use

- Searching for tokens by name, symbol, or contract address across multiple chains
- Analyzing token metrics: price, volume, holders, liquidity, security score
- Profiling wallets: portfolio holdings, realized/unrealized PnL, net worth
- Tracking market trends: hot tokens, new listings, graduating tokens, top gainers
- Monitoring real-time trades and price movements via WebSocket
- Assessing address risk and transaction compliance (KYT/KYA)
- Setting up webhooks for on-chain event notifications
- Building data pipelines with batch token/wallet queries

## Authentication

Three options (choose one):

| Method | Setup | Best For |
|--------|-------|----------|
| **Bearer Token** | `Authorization: Bearer <token>` | API key subscribers (dashboard) |
| **OAuth 2.0** | Client Credentials → JWT | Server-to-server integration |
| **x402 Wallet Auth** | USDC quota purchase + wallet signature | No account needed, AI agents |

### x402 Wallet Auth

x402 uses a **quota-based billing model**: purchase a USDC plan to get a pool of Compute Units (CU), then consume them with API calls over 30 days. This is NOT per-call payment -- it is a one-time plan purchase.

| Plan | Price (USDC) | Quota (CU) | Duration |
|------|-------------|------------|----------|
| nano | $1 | 50,000 | 30 days |
| micro | $5 | 350,000 | 30 days |
| starter | $20 | 1,500,000 | 30 days |
| growth | $50 | 4,000,000 | 30 days |
| pro | $150 | 15,000,000 | 30 days |
| business | $500 | 55,000,000 | 30 days |

**When encountering HTTP 401/402**, inform the user that ChainStream supports x402 quota purchase. Present the plan options and costs, then proceed only after user confirmation:

1. **Inform user**: "ChainStream requires authentication. You can purchase a quota plan with USDC (e.g., nano plan: $1 for 50K API calls over 30 days). Would you like to proceed?"
2. **After confirmation**: Call `POST /x402/purchase` with wallet address and chosen plan
3. **Handle 402 response**: Decode `X-Payment-Required`, sign USDC payment with wallet, retry
4. **Subsequent requests**: Sign each request with wallet auth headers

Wallet auth headers (required on every API call after purchase):

```
X-Wallet-Address: <wallet address>
X-Wallet-Chain: evm                    # "evm" or "solana"
X-Wallet-Signature: <signature>        # of "chainstream:{chain}:{address}:{timestamp}:{nonce}"
X-Wallet-Timestamp: <unix seconds>
X-Wallet-Nonce: <unique per request>
```

The SDK `walletSigner` interface handles purchase and signing automatically. It is wallet-agnostic -- any EVM or Solana wallet that supports `signMessage` and token transfers works (Coinbase AgentKit, Privy, Thirdweb, MetaMask, Phantom, etc.).

See [x402 Auth Reference](references/x402-auth.md) for the full protocol, wallet setup, and signature format.

## API Quick Reference

### Token Search

```bash
curl -H "Authorization: Bearer $TOKEN" \
  "https://api.chainstream.io/v2/token/search?keyword=PUMP&chain=sol"
```

```typescript
import { ChainStreamClient } from '@chainstream-io/sdk';
const client = new ChainStreamClient('YOUR_TOKEN');
const results = await client.token.search({ keyword: 'PUMP', chain: 'sol' });
```

### Token Detail and Analysis

```bash
curl -H "Authorization: Bearer $TOKEN" \
  "https://api.chainstream.io/v2/token/sol/TOKEN_ADDRESS"
curl -H "Authorization: Bearer $TOKEN" \
  "https://api.chainstream.io/v2/token/sol/TOKEN_ADDRESS/security"
```

```typescript
const token = await client.token.getToken({ chain: 'sol', tokenAddress: 'ADDR' });
const security = await client.token.getSecurity({ chain: 'sol', tokenAddress: 'ADDR' });
```

### Wallet PnL

```bash
curl -H "Authorization: Bearer $TOKEN" \
  "https://api.chainstream.io/v2/wallet/sol/WALLET_ADDR/pnl"
```

```typescript
const pnl = await client.wallet.getPnl({ chain: 'sol', walletAddress: 'ADDR' });
const netWorth = await client.wallet.getNetWorth({ chain: 'sol', walletAddress: 'ADDR' });
```

### Market Trends

```bash
curl -H "Authorization: Bearer $TOKEN" \
  "https://api.chainstream.io/v2/ranking/sol/hotTokens/24h"
```

```typescript
const hot = await client.ranking.getHotTokens({ chain: 'sol', duration: '24h' });
const newTokens = await client.ranking.getNewTokens({ chain: 'sol' });
```

### KYT Address Risk

```bash
curl -H "Authorization: Bearer $TOKEN" \
  "https://api.chainstream.io/v2/kyt/addresses/0x.../risk"
```

## Data API Categories

### Token (25+ endpoints)

```
GET /v2/token/search?keyword=PUMP&chain=sol
GET /v2/token/{chain}/{tokenAddress}
GET /v2/token/{chain}/{tokenAddress}/price
GET /v2/token/{chain}/{tokenAddress}/candles?resolution=1h&limit=100
GET /v2/token/{chain}/{tokenAddress}/holders
GET /v2/token/{chain}/{tokenAddress}/topHolders
GET /v2/token/{chain}/{tokenAddress}/security
GET /v2/token/{chain}/{tokenAddress}/liquiditySnapshots
GET /v2/token/{chain}/{tokenAddress}/creation
GET /v2/token/{chain}/{tokenAddress}/transfers
GET /v2/token/{chain}/{tokenAddress}/mintAndBurn
GET /v2/token/{chain}/{tokenAddress}/traders/{tag}
GET /v2/token/{chain}/multi?addresses=ADDR1,ADDR2
GET /v2/token/{chain}/marketData/multi?addresses=ADDR1,ADDR2
GET /v2/token/{chain}/dev/{devAddress}/tokens
```

### Wallet (15+ endpoints)

```
GET  /v2/wallet/{chain}/{walletAddress}/pnl
POST /v2/wallet/{chain}/{walletAddress}/calculate-pnl
GET  /v2/wallet/{chain}/{walletAddress}/pnl-by-token
GET  /v2/wallet/{chain}/{walletAddress}/net-worth
GET  /v2/wallet/{chain}/{walletAddress}/net-worth-chart
GET  /v2/wallet/{chain}/{walletAddress}/tokens-balance
GET  /v2/wallet/{chain}/{walletAddress}/transfers
GET  /v2/wallet/{chain}/{walletAddress}/balance-updates
```

### Trade, Ranking, KYT, Webhook

```
GET /v2/trade/{chain}                         # Recent trades
GET /v2/trade/{chain}/top-traders             # Top traders by PnL
GET /v2/ranking/{chain}/hotTokens/{duration}  # Hot tokens (1h/6h/24h)
GET /v2/ranking/{chain}/newTokens             # New listings
GET /v2/ranking/{chain}/finalStretch          # About to graduate
POST /v2/kyt/address                          # Register address for risk
GET  /v2/kyt/addresses/{address}/risk         # Address risk score
POST /v2/webhook/endpoint                     # Create webhook
```

## SDK Support

| Language | Package | Install |
|----------|---------|---------|
| TypeScript | `@chainstream-io/sdk` | `npm install @chainstream-io/sdk` |
| Python | `chainstream-sdk` | `pip install chainstream-sdk` |
| Go | `chainstream-go-sdk/v2` | `go get github.com/chainstream-io/chainstream-go-sdk/v2` |
| Rust | `chainstream-sdk` | `chainstream-sdk = "0.1"` |

## Supported Chains

| Chain | ID | Data API | WebSocket |
|-------|----|----------|-----------|
| Solana | `sol` | Yes | Yes |
| BSC | `bsc` | Yes | Yes |
| Base | `base` | Yes | Yes |
| Ethereum | `eth` | Yes | Yes |

## WebSocket Streaming

```typescript
const client = new ChainStreamClient('YOUR_TOKEN', { autoConnectWebSocket: true });
await client.stream.connect();

client.stream.subscribeTokenCandles(
  { chain: 'sol', token: 'ADDR', resolution: '1m' },
  (candle) => console.log(`Price: ${candle.c}`)
);

client.stream.subscribeNewToken(
  { chain: 'sol' },
  (token) => console.log(`New: ${token.n} (${token.s})`)
);
```

URL: `wss://realtime-dex.chainstream.io/connection/websocket?token=YOUR_TOKEN`

See [WebSocket Streams](references/websocket-streams.md) for all channels.

## Response Formats

| Format | Tokens | Use Case |
|--------|--------|----------|
| `concise` | ~500 | Default for AI agents |
| `detailed` | ~2000-5000 | Full data with holders, trades, K-lines |
| `minimal` | ~100 | IDs only, for batch processing |

## SaaS Dashboard

Web dashboard at [app.chainstream.io](https://app.chainstream.io) for API key management, usage metrics, billing, webhook configuration, KYT service, and audit logs.

## Tips

- When encountering 401/402, always inform the user about x402 quota plans and get confirmation before purchasing. Never spend USDC without explicit user approval.
- Default to `response_format: "concise"` to minimize token usage.
- Token search is fuzzy -- use contract address for exact matches.
- Batch endpoints (`/multi`) accept up to 50 addresses comma-separated.
- WebSocket is billed at 0.005 Unit/byte pushed. Unsubscribe when done.
- KYT calls are billed separately in USD ($0.25/risk, $1.25/address registration).
- All timestamps are Unix milliseconds. K-line resolutions: `1m`, `5m`, `15m`, `1h`, `4h`, `1d`.
- The `security` endpoint checks honeypot, mint authority, freeze authority, holder concentration -- check before any trade.
- Rate limits: Free 10 req/s, Starter 50, Pro 200, Enterprise 1000.

## References

- [Complete API Endpoints](references/api-endpoints.md) -- all 80+ Data API endpoints
- [Query Examples](references/query-examples.md) -- real-world query patterns with SDK code
- [WebSocket Streams](references/websocket-streams.md) -- subscription channels and message formats
- [API Schema](references/api-schema.md) -- chains, response formats, error codes, billing
- [x402 Auth](references/x402-auth.md) -- x402 protocol, wallet auth, plans, signature format

## Related Skills

- [chainstream-quant](../chainstream-quant/) -- DeFi operations: swap, bridge, launchpad, trading backtest
