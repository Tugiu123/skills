---
name: context-compression
version: 3.3.0
description: "OpenClaw session context compression and hierarchical memory management. Use when: (1) configuring compaction strategies (2) setting up session summaries (3) managing layered memory architecture (4) preventing context exceed errors. Triggers on questions about compression config, memory management, context optimization, or context overflow issues."
---

# Context Compression - Complete Solution

A comprehensive context management system that ensures:
1. **Never exceeds model context limit**
2. **Remembers all previous conversations** through hierarchical memory

---

## 🚀 Quick Start: Interactive Setup

When this skill is first loaded, **proactively guide the user through configuration**:

### Step 0: Check Existing Configuration

```bash
# Check if already configured
cat ~/.openclaw/workspace/.context-compression-config.json 2>/dev/null

# Check current system crontab
crontab -l | grep truncate
```

If already configured, ask: "Existing configuration detected. Reconfigure?"

### Step 1: Ask Configuration Questions (One at a Time)

**Question 1: Context Preservation**
> "How much context should be preserved for each new session? (1 token ≈ 3-4 Chinese characters)"
> - Default (40000 tokens) → Recommended, balances history retention with context safety
> - Conservative (60000 tokens) → Keeps more history
> - Aggressive (20000 tokens) → Minimizes context
> - Custom → Enter token count (10000-100000)

**Question 2: Truncation Frequency**
> "How often should context be truncated to prevent overflow?"
> - Every 10 minutes (Default) → Recommended
> - Every 30 minutes → Low frequency
> - Every hour → Lowest frequency
> - Custom → Enter minutes

**Question 3: Skip Active Sessions**
> "Should active sessions be skipped during truncation to prevent corruption of sessions being written?"
> - Yes (Default) → Recommended, prevents data corruption
> - No → May truncate sessions currently being written to

**Question 4: Daily Summary Generation**
> "Should daily session summaries be generated automatically?"
> - Yes → Generate compressed summaries from daily notes every 4 hours
> - No (Default) → Rely on real-time memory writes

### Step 2: Save Configuration

Create config file and update scripts:

```bash
# Save configuration
cat > ~/.openclaw/workspace/.context-compression-config.json << 'EOF'
{
  "version": "2.0",
  "maxTokens": <user_choice>,
  "frequencyMinutes": <user_choice>,
  "skipActive": <user_choice>,
  "enableSummaries": <user_choice>,
  "configuredAt": "$(date -Iseconds)"
}
EOF
```

### Step 3: Update System Crontab

```bash
# Remove old truncation cron
crontab -l | grep -v "truncate-sessions" | crontab -

# Add new truncation cron with user config
MINUTES="*/<user_frequency>"
CRON_CMD="<workspace>/skills/context-compression/scripts/truncate-sessions-safe.sh"
(crontab -l 2>/dev/null; echo "$MINUTES * * * * $CRON_CMD") | crontab -
```

### Step 4: Update Script Parameters

Update `truncate-sessions-safe.sh` with user config:

```bash
# Create config env file for the script
cat > ~/.openclaw/workspace/skills/context-compression/scripts/.config << 'EOF'
export MAX_TOKENS=<user_max_tokens>
export SKIP_ACTIVE=<user_skip_active>
EOF
```

### Step 5: Confirm Configuration

Tell user:
```
✅ Configuration complete!

Truncation settings:
- Token limit: X tokens (~Y Chinese characters)
- Check frequency: Every Z minutes
- Skip active sessions: Yes/No

Next steps:
1. Real-time memory writes ensure continuity
2. System will auto-truncate session files
3. Run check-context-health.sh to check status
```

---

## 🎯 Design Goals

| Goal | Solution |
|------|----------|
| Never exceed context limit | Pre-load truncation + context window management |
| Remember history | Hierarchical memory: short window + compressed summaries |
| Reliable | No dependency on agent context for critical operations |

---

## 🏗️ Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         Context Assembly Pipeline                            │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  Total Context Budget: 80k tokens                                          │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ L4: Long-term Memory (MEMORY.md)                    ~5k tokens      │   │
│  │     - User preferences, important decisions, key facts              │   │
│  │     - Loaded first, always present                                  │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ L3: Compressed Summaries (memory/summaries/)        ~10k tokens     │   │
│  │     - Daily summaries of older conversations                        │   │
│  │     - Compressed but semantically complete                          │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ L2: Short-term Window (recent sessions)             ~25k tokens     │   │
│  │     - Last N sessions, full conversation history                    │   │
│  │     - Loaded from session files directly                            │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ L1: Current Session                                  ~40k tokens     │   │
│  │     - Active conversation, full detail                              │   │
│  │     - Real-time writing to memory                                   │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  Reserved for system: ~10k tokens                                          │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 🔧 Implementation

### Part 1: System-Level Session Truncation

**Problem**: Truncation must happen BEFORE context is loaded.

**Solution**: External process (system crontab) that runs outside agent context.

```bash
# /root/.openclaw/workspace/skills/context-compression/scripts/truncate-sessions-safe.sh
# Runs every 10 minutes via system crontab

# Key parameters:
MAX_TOKENS=40000       # Keep last 40000 tokens per session
SKIP_ACTIVE=true       # Don't truncate sessions with .lock files
```

**Installation**:
```bash
# Add to system crontab
(crontab -l 2>/dev/null; echo "*/10 * * * * /root/.openclaw/workspace/skills/context-compression/scripts/truncate-sessions-safe.sh") | crontab -
```

---

### Part 2: Session Startup Sequence

**Every session must execute this sequence BEFORE loading full context:**

```
Step 1: Read MEMORY.md (long-term memory)
Step 2: Read memory/YYYY-MM-DD.md (today + yesterday notes)
Step 3: Load recent session files (limited by window size)
Step 4: Assemble context within budget
Step 5: Begin conversation
```

**Implementation in AGENTS.md**:
```markdown
## Every Session

1. Read MEMORY.md — long-term memory
2. Read memory/YYYY-MM-DD.md (today + yesterday)
3. Session files are auto-truncated by system cron
4. Begin conversation
5. **Real-time memory writing**: Important info → write to memory files immediately
```

---

### Part 3: Real-Time Memory Writing

**Critical**: Memory must be written during conversation, not after.

```
During Conversation:
│
├─→ User mentions preference → IMMEDIATELY update MEMORY.md
├─→ Important decision made → IMMEDIATELY update MEMORY.md
├─→ Task completed → IMMEDIATELY write to daily notes
└─→ Key information learned → IMMEDIATELY update relevant file
```

**Why immediate?**
- Session may be truncated at any time
- Summaries are unreliable (fail when context exceeded)
- Only guaranteed way to preserve memory

---

### Part 4: Hierarchical Memory Structure

#### L4: Long-term Memory (MEMORY.md)

```markdown
# MEMORY.md

## User Profile
- Name: ...
- Preferences: ...
- Goals: ...

## Important Decisions
- [Date] Decision: ...

## Key Information
- ...
```

**Update trigger**: Immediately when important info is mentioned.

#### L3: Daily Summaries (memory/summaries/YYYY-MM-DD.md)

```markdown
# Summary - YYYY-MM-DD

## Key Events
1. Event 1: ...
2. Event 2: ...

## Decisions
- Decision 1

## Tasks
- ✅ Completed: ...
- 🔄 In Progress: ...

## Tokens: ~500 (compressed from ~10k original)
```

**Generation**: Run daily via cron (but don't depend on it for critical memory).

#### L2: Recent Sessions (session files)

- Last 2000 lines per session
- Auto-truncated by system cron
- Full conversation detail for recent history

#### L1: Current Session

- Active conversation
- Write to memory files in real-time

---

## 📊 Context Budget Management

### Token Allocation

| Layer | Budget | Source |
|-------|--------|--------|
| System messages | ~10k | OpenClaw internal |
| Long-term memory (L4) | ~5k | MEMORY.md |
| Daily summaries (L3) | ~10k | memory/summaries/*.md |
| Recent sessions (L2) | ~25k | Session files (limited) |
| Current session (L1) | ~30k | Active conversation |
| **Total** | ~80k | |

### Overflow Handling

```
If context > 80k tokens:
│
├─→ Step 1: Skip older summaries (L3)
├─→ Step 2: Reduce recent sessions window (L2)
├─→ Step 3: Compress current session (handled by OpenClaw safeguard mode)
└─→ Always preserve: L4 (MEMORY.md) + L1 (current session)
```

---

## 🚀 Scripts

### 1. truncate-sessions-safe.sh

Safe truncation that preserves JSONL integrity.

```bash
#!/bin/bash
# Truncates session files to last N lines
# Preserves JSONL line integrity
# Skips active sessions (with .lock files)
```

### 2. generate-daily-summary.sh

Generates compressed summary from daily notes (not from session context).

```bash
#!/bin/bash
# Reads memory/YYYY-MM-DD.md
# Compresses to ~500 tokens
# Writes to memory/summaries/YYYY-MM-DD.md
```

### 3. check-context-health.sh

Reports current context status.

```bash
#!/bin/bash
# Reports:
# - Total session file sizes
# - Memory file sizes
# - Estimated context usage
# - Recommendations
```

---

## ⚙️ Configuration

### openclaw.json

```json
{
  "agents": {
    "defaults": {
      "contextTokens": 80000,
      "compaction": {
        "mode": "safeguard",
        "reserveTokens": 25000,
        "reserveTokensFloor": 30000,
        "keepRecentTokens": 10000,
        "maxHistoryShare": 0.5
      }
    }
  }
}
```

### System Crontab

```bash
# Session truncation (every 10 minutes)
*/10 * * * * /root/.openclaw/workspace/skills/context-compression/scripts/truncate-sessions-safe.sh

# Daily summary generation (every 4 hours)
0 */4 * * * /root/.openclaw/workspace/skills/context-compression/scripts/generate-daily-summary.sh
```

---

## ✅ Verification Checklist

After setup, verify:

- [ ] System crontab is running: `crontab -l`
- [ ] Truncation script is executable: `ls -la scripts/truncate-sessions-safe.sh`
- [ ] Memory directories exist: `ls -la memory/ memory/summaries/`
- [ ] MEMORY.md exists and is up to date
- [ ] AGENTS.md includes real-time memory writing instructions

---

## 🔍 Troubleshooting

### Context Still Exceeded

1. Check truncation is running: `cat /root/.openclaw/logs/truncation.log`
2. Reduce MAX_LINES in truncation script
3. Reduce contextTokens in openclaw.json

### Memory Not Persisting

1. Check AGENTS.md has real-time writing instructions
2. Verify memory files are being updated: `ls -la memory/`
3. Ensure important info is written immediately, not at end of session

### Summaries Not Generated

1. Check daily notes exist: `ls -la memory/YYYY-MM-DD.md`
2. Run summary script manually to test
3. Check cron logs: `grep CRON /var/log/syslog`

---

## 📚 References

- [OpenClaw Compaction Docs](https://docs.openclaw.ai)
- [Hierarchical Memory Architecture](references/memory-architecture.md)
- [Token Estimation Guide](references/token-estimation.md)
