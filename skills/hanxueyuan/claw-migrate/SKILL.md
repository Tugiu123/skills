---
name: claw-migrate
description: OpenClaw workspace backup & restore - simple tar-based guide
homepage: https://github.com/hanxueyuan/claw-migrate
metadata:
  {"openclaw":{"emoji":"🔄","requires":{"bins":["tar"]}}}
---

# claw-migrate - OpenClaw Backup & Restore Guide

> **Simple & Safe**: No code, no automation, just clear instructions

---

## 🎯 What Is This?

claw-migrate is a **pure guidance skill** - no installation needed, no code to run.

Just follow the instructions below to backup and restore your OpenClaw workspace.

---

## 📁 Path 1: Backup

### Quick Backup (Recommended)

```bash
# Backup core files only (fast)
tar -czf openclaw-backup-$(date +%Y%m%d_%H%M%S).tar.gz \
  -C /workspace/projects/workspace \
  AGENTS.md SOUL.md IDENTITY.md USER.md TOOLS.md HEARTBEAT.md \
  memory/ .learnings/ docs/ scripts/ templates/
```

### Full Backup (Include Skills)

```bash
# Backup everything including skills
tar -czf openclaw-full-backup-$(date +%Y%m%d_%H%M%S).tar.gz \
  -C /workspace/projects/workspace \
  AGENTS.md SOUL.md IDENTITY.md USER.md TOOLS.md HEARTBEAT.md \
  memory/ .learnings/ docs/ scripts/ templates/ skills/ agents/
```

### What to Backup ✅

| Category | Files | Backup? |
|----------|-------|---------|
| Core Config | AGENTS.md, SOUL.md, IDENTITY.md, USER.md | ✅ Yes |
| Tools | TOOLS.md, HEARTBEAT.md | ✅ Yes |
| Memory | memory/*.md | ✅ Yes |
| Learnings | .learnings/*.md | ✅ Yes |
| Docs | docs/ | ✅ Yes |
| Scripts | scripts/ | ✅ Yes |
| Templates | templates/ | ✅ Yes |
| Skills | skills/ | ⚠️ Optional (large) |
| Agents | agents/ | ⚠️ Optional |

### What NOT to Backup ❌

| Files | Reason |
|-------|--------|
| `.env` | Contains API keys |
| `openclaw.json` | Contains secrets |
| `credentials/` | Pairing tokens |
| `identity/` | Device auth |
| `devices/` | Paired devices |
| `feishu/` | Channel config |
| `browser/` | Browser data (large) |

---

## 🔄 Path 2: Restore

### Restore from Backup

```bash
# Extract backup to workspace
tar -xzf openclaw-backup-YYYYMMDD_HHMMSS.tar.gz \
  -C /workspace/projects/workspace/
```

### Restore Steps

1. **Stop OpenClaw** (if running)
   ```bash
   openclaw gateway stop
   ```

2. **Extract Backup**
   ```bash
   tar -xzf your-backup.tar.gz -C /workspace/projects/workspace/
   ```

3. **Verify Files**
   ```bash
   ls -la /workspace/projects/workspace/
   ```

4. **Re-pair Channels** (required)
   ```bash
   openclaw pairing
   ```

5. **Restart OpenClaw**
   ```bash
   openclaw gateway restart
   ```

### Restore Notes ⚠️

| Item | Action |
|------|--------|
| API Keys | Re-add to `.env` |
| Channel Pairing | Re-pair all channels |
| Device Auth | Re-authenticate devices |
| Memory Files | Merged automatically |
| Skills | Preserved (no re-install needed) |

---

## 📤 Path 3: Share to ClawTalent

### Prepare for Sharing

1. **Sanitize Sensitive Info**
   ```bash
   # Remove .env, credentials, etc.
   rm -rf .env credentials/ identity/ devices/
   ```

2. **Create Manifest**
   ```json
   {
     "name": "my-openclaw-config",
     "version": "1.0.0",
     "description": "My OpenClaw workspace config",
     "openclaw_version": "2026.3.13",
     "skills": ["coze-web-search", "agent-browser"],
     "agents": ["main", "life", "work"]
   }
   ```

3. **Upload to GitHub**
   ```bash
   git add .
   git commit -m "Share OpenClaw config"
   git push origin main
   ```

### Share via ClawTalent Platform

Visit: https://clawtalent.shop

1. Create account
2. Upload sanitized config
3. Get CT-XXXX ID
4. Share ID with others

---

## 🔍 Path 4: Discover Configs

### Browse ClawTalent

Visit: https://clawtalent.shop

Search for:
- Multi-agent setups
- Specific skills
- Industry templates

### Deploy from ClawTalent

```bash
# Get config from CT-XXXX ID
git clone https://github.com/hanxueyuan/clawtalent-CT-XXXX.git
cd clawtalent-CT-XXXX
tar -xzf config.tar.gz -C /workspace/projects/workspace/
```

### Verify Before Deploy

1. Check OpenClaw version compatibility
2. Review skills list
3. Check agent configurations
4. Verify no sensitive data included

---

## 🔐 Security Best Practices

### Always ✅

- Store backups in **private** GitHub repos
- Use environment variables for API keys
- Re-pair channels after restore
- Sanitize before sharing

### Never ❌

- Share `.env` files
- Commit API keys to Git
- Share pairing tokens
- Backup browser data (privacy)

---

## 📋 Quick Reference

### Backup Commands

```bash
# Quick backup (core files only)
tar -czf backup.tar.gz -C /workspace/projects/workspace \
  AGENTS.md SOUL.md memory/ .learnings/

# Full backup (include skills)
tar -czf full-backup.tar.gz -C /workspace/projects/workspace \
  AGENTS.md SOUL.md memory/ .learnings/ skills/ agents/
```

### Restore Commands

```bash
# Extract backup
tar -xzf backup.tar.gz -C /workspace/projects/workspace/

# Verify
ls -la /workspace/projects/workspace/
```

### Storage Options

| Option | Command |
|--------|---------|
| Local | `cp backup.tar.gz ~/backups/` |
| GitHub | `git push origin main` |
| Cloud | Upload to Google Drive / Dropbox |

---

## 🆘 Troubleshooting

### "Permission denied"

```bash
# Fix permissions
chmod -R 755 /workspace/projects/workspace/
chmod 600 /workspace/projects/workspace/.env
```

### "Missing files after restore"

Check `.gitignore` - some files are excluded from backup by design.

### "Channel not working after restore"

Re-pair channels:
```bash
openclaw pairing
```

### "Skills not found"

Skills are in `skills/` directory. Verify:
```bash
ls /workspace/projects/workspace/skills/
```

---

## 📚 Resources

- **GitHub**: https://github.com/hanxueyuan/claw-migrate
- **ClawTalent**: https://clawtalent.shop
- **OpenClaw Docs**: https://docs.openclaw.ai

---

## 📄 License

MIT License - Free to use and share (but sanitize first!)
