---
name: gauntletscore
version: 1.0.0
description: Trust verification for AI output — verify any document or code before you act on it
author: Genstrata, Inc.
license: proprietary
homepage: https://gauntletscore.com
api_base: https://api.gauntletscore.com
tags:
  - trust
  - verification
  - security
  - code-safety
  - fact-checking
  - hallucination-detection
  - compliance
---

# GauntletScore — The Trust Layer for AI

Verify any AI-generated document or code before you trust it. Seven adversarial AI agents independently analyze your content, verify every checkable claim against authoritative sources, and produce a cryptographically signed trust score.

## What It Does

Submit a document or code and get:

- **Gauntlet Score** (0-100) with letter grade (A-F)
- **Claim-by-claim verification** against CourtListener (legal), eCFR (regulatory), PubMed (scientific), EDGAR (SEC), and computational math verification
- **Code safety analysis** detecting reverse shells, credential theft, prompt injection, data exfiltration, and obfuscated payloads
- **Unanimous vote** from 6 independent AI agents (PROCEED / PROCEED WITH CONDITIONS / DO NOT PROCEED)
- **Cryptographic certificate** proving the score is genuine and untampered
- **Full debate transcript** showing every agent's reasoning

## Quick Start

Your first analysis is free. Get an API key at [gauntletscore.com](https://gauntletscore.com).

### Verify a document by pasting content:
```
POST https://api.gauntletscore.com/v1/analyze
Authorization: Bearer YOUR_API_KEY
Content-Type: application/json

{
  "document": "Your document text here...",
  "topic": "Verify the claims in this document"
}
```

### Verify a ClawHub skill by URL:
```
POST https://api.gauntletscore.com/v1/analyze
Authorization: Bearer YOUR_API_KEY
Content-Type: application/json

{
  "source_url": "https://clawhub.ai/skills/some-skill/SKILL.md",
  "topic": "Evaluate the safety of this ClawHub skill before installation"
}
```

### Check results:
```
GET https://api.gauntletscore.com/v1/jobs/{job_id}
Authorization: Bearer YOUR_API_KEY
```

Results include score, grade, vote, verified claims, and a cryptographic certificate.

## What It Catches

### In documents:
- Fabricated legal citations (hallucinated case law)
- Misapplied regulations (wrong CFR section for the situation)
- Mathematical errors (wrong totals, incorrect percentages)
- Internal contradictions
- Unsupported conclusions

### In code:
- Reverse shells and remote code execution
- Credential theft and data exfiltration
- Download-and-execute attacks (curl | bash)
- Prompt injection ("ignore previous instructions")
- Documentation-vs-behavior mismatches (code does things the README doesn't mention)
- Dangerous operation combinations that pass individual checks

## How It Works

Seven AI personas from four different providers (Anthropic, OpenAI, Google, xAI) independently analyze your submission:

1. **Round 0** — Each agent conducts independent research, verifying claims against authoritative databases
2. **Rounds 1-3** — Structured adversarial debate where agents challenge each other's findings
3. **Round 4** — Final positions and votes
4. **Scoring** — Six-component rubric produces the Gauntlet Score
5. **Certification** — Ed25519 cryptographic signature proves the result is genuine

All analysis is **read-only**. Submitted code is never executed. Documents are processed in memory and not stored.

## Pricing

- First analysis: **Free**
- Credit packs available at [gauntletscore.com](https://gauntletscore.com)
- Enterprise and Sovereign Edition: [sales@genstrata.com](mailto:sales@genstrata.com)

## Verify a Certificate

Anyone can verify a Gauntlet Score is genuine:
```
GET https://api.gauntletscore.com/v1/verify/{certificate_id}
```

No authentication required. Public key available at:
```
GET https://api.gauntletscore.com/.well-known/gauntlet-public-key.pem
```

## Links

- [API Documentation](https://gauntletscore.com/docs)
- [Terms of Service](https://gauntletscore.com/terms)
- [Privacy Policy](https://gauntletscore.com/privacy)
- [Acceptable Use Policy](https://gauntletscore.com/acceptable-use)

## About

GauntletScore is built by [Genstrata, Inc.](https://genstrata.com) The Gauntlet's adversarial multi-agent verification architecture is patent-pending (USPTO #63/967,169).

For organizations that cannot send data to cloud services, the **Sovereign Edition** runs entirely on your hardware with zero data egress. Contact [sales@genstrata.com](mailto:sales@genstrata.com).
