# claw-migrate - OpenClaw Backup & Restore Guide

> 🔄 **Pure Guidance Skill** - No code, no installation, just follow the instructions

[![Version](https://img.shields.io/github/package-json/v/hanxueyuan/claw-migrate)](https://github.com/hanxueyuan/claw-migrate)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## 🎯 What Is This?

**claw-migrate is NOT a tool - it's a guide.**

No installation needed. No code to run. Just follow the instructions in [SKILL.md](SKILL.md).

---

## 🚀 Quick Start

### I Want to Backup

```bash
# Quick backup (core files)
tar -czf backup.tar.gz -C /workspace/projects/workspace \
  AGENTS.md SOUL.md IDENTITY.md USER.md TOOLS.md \
  memory/ .learnings/ docs/ scripts/

# Full backup (include skills)
tar -czf full-backup.tar.gz -C /workspace/projects/workspace \
  AGENTS.md SOUL.md memory/ .learnings/ skills/ agents/
```

### I Want to Restore

```bash
# Extract backup
tar -xzf backup.tar.gz -C /workspace/projects/workspace/

# Re-pair channels
openclaw pairing
```

### I Want to Share

1. Sanitize sensitive files (`.env`, `credentials/`, etc.)
2. Upload to GitHub or ClawTalent
3. Share the repo link or CT-XXXX ID

### I Want to Discover

Visit: https://clawtalent.shop

Search for configs shared by the community.

---

## 📋 Full Instructions

See **[SKILL.md](SKILL.md)** for:
- ✅ Detailed backup checklist
- ✅ Restore step-by-step guide
- ✅ Security best practices
- ✅ Troubleshooting tips
- ✅ Quick reference commands

---

## 🔐 Security Tips

### Always ✅
- Store backups in **private** repos
- Use environment variables for API keys
- Re-pair channels after restore
- Sanitize before sharing

### Never ❌
- Share `.env` files
- Commit API keys to Git
- Share pairing tokens
- Backup browser data

---

## 📊 What's Included

| File | Size | Type |
|------|------|------|
| SKILL.md | ~6KB | Full instructions |
| README.md | ~2KB | Quick start |
| CHANGELOG.md | ~6KB | Version history |
| .clawhub.json | ~1KB | ClawHub metadata |

**Total: ~15KB** (no code, no dependencies!)

---

## 🌐 Links

- **[Full Instructions](SKILL.md)** - Complete backup/restore guide
- **[ClawTalent](https://clawtalent.shop)** - Share & discover configs
- **[GitHub](https://github.com/hanxueyuan/claw-migrate)** - Source & examples
- **[OpenClaw Docs](https://docs.openclaw.ai)** - Official documentation

---

## 📄 License

MIT License - Free to use and share (but remember to sanitize first!)
