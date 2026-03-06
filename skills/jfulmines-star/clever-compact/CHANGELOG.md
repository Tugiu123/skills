# Clever Compact — Changelog

## v1.2.0 — March 4, 2026
**Framing update — now speaks the language of the problem**
- Reframed the opening around the three failure modes: `/new` amnesia, compaction loss, memory drift
- Language mirrors how power users actually describe the problem — makes it immediately recognizable
- No functional changes to the skill itself

## v1.1.0 — March 3, 2026
**Reduce compaction frequency**
- Added `reserveTokens` tuning guide — lower from 50,000 to 15,000 to push compaction to ~185k/200k context
- Roughly 3–4× fewer compactions per heavy session
- Updated urgency language: compaction takes up to 10 minutes, not seconds. Real discovery from live power-user sessions.

## v1.0.0 — March 1, 2026
**Initial release**
- Core pre-compact scan: active workstreams, key decisions, open tasks, credentials, relationship context, remember flags
- State file written to `memory/compact-state-YYYY-MM-DD-HH.md`
- Post-compact restore hook via AGENTS.md
- State file format spec (Markdown + embedded JSON)
- Pro tier placeholder ($9/mo — feature-gated)
