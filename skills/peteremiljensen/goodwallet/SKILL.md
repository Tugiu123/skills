---
name: goodwallet
description: >
  Skill for using the goodwallet tool to manage MPC agentic wallets. Use this skill whenever
  the user wants to authenticate, send ETH via the their goodwallet.
  Trigger when the user mentions "goodwallet", "send ETH", "wallet auth", "wallet authorize", "goodwallet authorize",
  "MPC wallet", "agentic wallet", or wants to interact with their wallet
  from the command line.
---

# Goodwallet

Use goodwallet cli to manage their agentic goodwallet to — authenticate, send ETH.
All commands are run via `npx goodwallet`.

## Setup

Before using any commands, configure your credentials:

```bash
npx goodwallet auth --api-key <your-api-key> --share <your-key-share> --address <your-0x-address>
```

This saves credentials to `~/.config/goodwallet/config.json`. You can set them independently:

```bash
npx goodwallet auth --api-key <key>
npx goodwallet auth --share <share>
npx goodwallet auth --address <0x-address>
```

All three (`--api-key`, `--share`, and `--address`) are required before you can sign transactions.

## Commands

### auth — Configure credentials

```bash
npx goodwallet auth --api-key <key> [--share <share>] [--address <0x-address>]
```

| Flag | Short | Required | Description |
|------|-------|----------|-------------|
| `--api-key <key>` | `-k` | At least one | API key for the signing service |
| `--share <share>` | `-s` | At least one | Cryptographic key share for MPC signing |
| `--address <address>` | — | At least one | EVM address (0x-prefixed, 40 hex chars) |

### send — Send ETH

Builds, MPC-signs, and broadcasts an ETH transaction.

```bash
npx goodwallet send --to <address> --amount <ether>
```

| Flag | Short | Required | Default | Description |
|------|-------|----------|---------|-------------|
| `--to <address>` | `-t` | Yes | — | Recipient Ethereum address |
| `--amount <ether>` | `-a` | Yes | — | Amount in ETH (e.g. `0.1`) |

Example:

```bash
npx goodwallet send --to 0x742d35Cc6634C0532925a3b844Bc9e7595f2bD18 --amount 0.05
```

The command will:
1. Load your credentials from config
2. Query the chain for nonce and gas price
3. Construct the transaction
4. Sign via MPC (threshold ECDSA with the signing service)
5. Broadcast and print the transaction hash

```

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `SIGN_URL` | `sign.goodwallet.dev` | Override the signing service endpoint |

Example:

```bash
SIGN_URL=sign.goodwallet.etoro.com npx goodwallet send --to 0x... --amount 0.1
```

## Typical Workflow

```bash
# 1. Authenticate
npx goodwallet auth --api-key mykey123 --share myshare456 --address 0x742d35Cc6634C0532925a3b844Bc9e7595f2bD18

# 2. Send a transaction
npx goodwallet send --to 0x742d35Cc6634C0532925a3b844Bc9e7595f2bD18 --amount 0.1

