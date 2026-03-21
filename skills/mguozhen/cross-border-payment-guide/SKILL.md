---
name: cross-border-payment-guide
description: "Cross-border payment solution guide for Amazon and e-commerce sellers. Compare Payoneer, WorldFirst (Airwallex), PingPong, XTransfer, and LianLian on fees, FX rates, withdrawal limits, and account features. Calculate currency conversion costs and choose the best collection account for your market. Triggers: cross-border payment, payoneer, worldfirst, pingpong, xtransfer, amazon payment, currency collection, fx rate, foreign currency, amazon settlement, lianlian, airwallex, cross-border collection, currency exchange, amazon payout, seller payment account"
allowed-tools: Bash
metadata:
  openclaw:
    homepage: https://github.com/mguozhen/cross-border-payment-guide
---

# Cross-Border Payment Solution Guide

Choose the right payment collection account for your Amazon business. Compare fees, FX rates, withdrawal speed, and features — keep more of your hard-earned revenue.

## Commands

```
payment compare                 # compare all major payment platforms
payment fees [platform] [amount]  # calculate exact fees for a transfer
payment fx [currency] [amount]  # compare FX rates across platforms
payment recommend [profile]     # get personalized recommendation
payment setup [platform]        # account setup requirements
payment tax [country]           # tax reporting requirements
payment multi                   # multi-currency account strategy
payment save [setup]            # save payment configuration
```

## What Data to Provide

- **Amazon marketplaces** — where you sell (US, UK, DE, JP, etc.)
- **Monthly revenue** — to calculate which platform saves most
- **Home currency** — what you want to withdraw to (CNY, USD, etc.)
- **Withdrawal frequency** — daily, weekly, monthly
- **Business type** — individual, company, Chinese entity

## Platform Comparison

### Payoneer
| Feature | Details |
|---------|---------|
| Receiving fee | 0% (from Amazon) |
| Withdrawal fee | 2% (to local bank) |
| FX spread | 2–3.5% above mid-market |
| Withdrawal speed | 2–5 business days |
| Min withdrawal | $50 |
| Supported markets | 200+ countries |
| Best for | Global sellers, non-Chinese sellers |
| Weakness | Higher FX spread, slow for large amounts |

### WorldFirst (now Airwallex in some markets)
| Feature | Details |
|---------|---------|
| Receiving fee | 0% |
| Withdrawal fee | 0.3–0.5% |
| FX spread | 0.5–1.5% above mid-market |
| Withdrawal speed | Same day to 2 days |
| Min withdrawal | None |
| Supported markets | 40+ currencies |
| Best for | High-volume sellers, competitive FX needs |
| Weakness | Stricter compliance checks |

### PingPong
| Feature | Details |
|---------|---------|
| Receiving fee | 0% |
| Withdrawal fee | 1% (USD→CNY) |
| FX spread | 1–2% |
| Withdrawal speed | 1–3 business days |
| Min withdrawal | $200 |
| Best for | Chinese sellers, small-medium volume |
| Weakness | Limited non-Chinese withdrawal options |

### XTransfer
| Feature | Details |
|---------|---------|
| Receiving fee | 0% |
| Withdrawal fee | 0% |
| FX spread | 0.3–0.8% (competitive) |
| Withdrawal speed | Same day (CNY) |
| Min withdrawal | None |
| Best for | Chinese manufacturing companies, B2B |
| Weakness | Newer platform, less brand recognition |

### LianLian Pay
| Feature | Details |
|---------|---------|
| Receiving fee | 0% |
| Withdrawal fee | 0.7–1% |
| FX spread | 1–2% |
| Withdrawal speed | 1–3 business days |
| Best for | Chinese individual sellers |
| Weakness | Limited to CNY withdrawal primarily |

## FX Cost Calculator

**Monthly revenue**: $10,000 USD → CNY

| Platform | FX Spread | Withdrawal Fee | Total Cost | You Receive (approx) |
|----------|-----------|---------------|------------|---------------------|
| XTransfer | 0.5% | 0% | $50 | ¥71,892 |
| WorldFirst | 1.0% | 0.3% | $130 | ¥71,012 |
| PingPong | 1.5% | 1.0% | $250 | ¥70,096 |
| Payoneer | 2.5% | 2.0% | $450 | ¥68,544 |

*Based on approximate USD/CNY rate of 7.25. Actual rates vary daily.*

**Annual savings** (XTransfer vs Payoneer at $10k/month): ~$4,800/year

## Multi-Currency Strategy

For sellers on multiple Amazon marketplaces:

```
Amazon US (USD) ──────────────────────→ WorldFirst/XTransfer USD account
Amazon UK (GBP) ──────────────────────→ WorldFirst GBP account (hold & convert at best rate)
Amazon DE (EUR) ──────────────────────→ WorldFirst EUR account
Amazon JP (JPY) ──────────────────────→ Payoneer JPY → convert when rate is favorable
                                                    ↓
                              Convert to CNY when exchange rate peaks
                              Withdraw to Chinese business bank account
```

**Key Strategy**: Hold in foreign currency, convert when rate is favorable. Don't auto-convert every withdrawal.

## Platform Selection by Seller Profile

| Seller Type | Recommended Platform | Why |
|-------------|---------------------|-----|
| New seller, <$5k/month | PingPong or LianLian | Easy setup, low minimum |
| Chinese seller, $5k–$50k/month | XTransfer or WorldFirst | Best FX rates |
| Global seller (non-CN) | Payoneer or WorldFirst | Wider coverage |
| High volume >$50k/month | WorldFirst or Airwallex | Volume discounts, dedicated support |
| B2B factory/manufacturer | XTransfer | Purpose-built for manufacturers |
| Multi-marketplace seller | WorldFirst | Best multi-currency account |

## Tax Reporting Considerations

### For Chinese Sellers (人民币提现)
- Withdrawals >$50,000/person/year require State Administration of Foreign Exchange (SAFE) documentation
- Company accounts have higher limits than personal accounts
- Keep all transaction records for VAT filing
- Use company account vs. personal account — different tax treatment

### VAT Registration (EU/UK Sellers)
If selling in EU/UK, you may need VAT registration:
- UK: Register if selling >£85,000/year or using Amazon FBA in UK
- Germany: Register before first sale (no threshold for non-EU sellers)
- Use platforms like Avalara or Taxjar for automated VAT compliance

## Setup Requirements by Platform

### Payoneer
- Valid passport or national ID
- Proof of address
- Bank account details
- Business documentation (if business account)

### WorldFirst
- Company registration documents
- Director/shareholder ID
- Business bank account
- Proof of Amazon seller account

### PingPong / XTransfer / LianLian
- Chinese ID card (for individuals)
- Business license (for companies)
- Amazon seller account verification

## Output Format

1. **Platform Recommendation** — best fit based on your profile
2. **Annual Cost Comparison** — exact savings vs. your current platform
3. **Multi-Currency Strategy** — when to convert, which accounts to use
4. **Setup Checklist** — documents needed for recommended platform
5. **Tax Reminders** — jurisdiction-specific compliance notes
