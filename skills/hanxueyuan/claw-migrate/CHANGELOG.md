# ClawMigrate Changelog

## [3.0.0] - 2026-03-20

### 🎉 Complete Redesign - Pure Guidance Skill

**Philosophy**: Simple > Complex, Guide > Automation

#### What Changed
- ❌ **Removed**: All code (4613 lines across 13 modules)
- ❌ **Removed**: `src/` directory (backup.js, restore.js, setup.js, etc.)
- ❌ **Removed**: `tests/` directory
- ❌ **Removed**: `package.json`, `package-lock.json`, `node_modules/`
- ✅ **Kept**: SKILL.md, README.md, CHANGELOG.md, .clawhub.json
- ✅ **Added**: Clear, simple instructions

#### Why v3.0.0?
- Major breaking change: from tool to guide
- No backward compatibility needed (just follow new instructions)
- Fresh start with lessons learned

#### New Structure
```
claw-migrate/
├── SKILL.md          # Full instructions (6KB)
├── README.md         # Quick start (2KB)
├── CHANGELOG.md      # Version history
├── .clawhub.json     # ClawHub metadata
└── .github/          # GitHub workflows (optional)
```

**Total size**: ~15KB (was: 4613 lines of code + dependencies)

#### Benefits
- ✅ Zero maintenance cost
- ✅ Zero security risks (no GITHUB_TOKEN needed)
- ✅ Zero dependencies
- ✅ User in full control
- ✅ Works with any OpenClaw version

#### Migration from v2.x
No migration needed! Just:
1. Delete old claw-migrate skill
2. Install v3.0.0
3. Follow instructions in SKILL.md

---

## [2.8.2] - 2026-03-20

### Clarified Two Modes

- Personal Migration (full backup with sensitive info)
- Community Sharing (auto-sanitized)

---

## [2.8.1] - 2026-03-20

### Selective Restore

- Added `--categories` option
- Fallback to default backup list if no setup

---

## [2.8.0] - 2026-03-20

### Restored Executable Functionality

- Now actually backs up and restores
- Automated backup with file scanning
- Automated restore with validation

---

## [2.7.7] - 2026-03-19

### Attempted Pure Guide Conversion

**Note**: This conversion was incomplete. Code remained but documentation claimed "no code".
This was addressed in v3.0.0 with complete removal of all code.

---

## [2.7.6] - 2026-03-19

### Full English Localization

- All documentation rewritten in English
- All code output in English
- Bug fixes

---

## [2.7.0] - 2026-03-19

### ClawTalent Platform Integration

#### New Commands
- `share` - Share to ClawTalent platform
- `deploy` - Deploy from ClawTalent (CT-XXXX)
- `search` - Search ClawTalent marketplace

#### Features
- Sensitive info detection
- Template desensitization
- Manifest generation
- Smart merge strategies

---

## [2.2.0] - 2026-03-15

### Configuration Management & Scheduled Backups

#### New Modules
- `src/setup.js` - Interactive configuration wizard
- `src/backup.js` - Backup execution
- `src/restore.js` - Restore execution
- `src/merger.js` - Merge engine
- `src/config-manager.js` - Configuration management
- `src/scheduler.js` - Scheduled backup tasks

#### Test Coverage
- 131 test cases, 100% pass rate
- 68.8% code coverage

---

## [2.0.0] - 2026-03-10

### Initial Automated Version

- Automated backup to GitHub
- Automated restore from backup
- Interactive setup wizard

---

## [1.0.0] - 2026-03-01

### First Release

- Basic backup instructions
- Simple restore guide
- Manual process
