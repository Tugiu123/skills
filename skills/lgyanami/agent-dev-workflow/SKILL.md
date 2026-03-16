---
name: dev-workflow
description: Orchestrate coding agents (Claude Code, Codex, etc.) to implement coding tasks through a structured workflow. Use when the user gives a coding requirement, feature request, bug fix, or GitHub issue to implement. Includes requirement analysis, document generation (requirement doc + verification doc), agent dispatch, monitoring, verification, and delivery. NOT for simple one-line fixes or reading code. Triggers on coding tasks, feature requests, bug reports, GitHub issues, or "implement/build/fix this".
---

# Dev Workflow — Orchestrated Coding Agent Dispatch

Structured workflow for driving coding agents to implement requirements with quality control.

## Prerequisites

- Claude Code (`claude` CLI) installed with `--permission-mode bypassPermissions --print`
- [cc-plugin](https://github.com/TokenRollAI/cc-plugin) installed in Claude Code (provides llmdoc read/write, investigator/scout/recorder sub-agents)
- Global `~/.claude/CLAUDE.md` configured with cc-plugin settings

## Workflow

### Phase 1: Environment Check

Before any work, check the target project:

1. **`llmdoc/` exists?**
   - Yes → read `llmdoc/index.md` + overview files to understand project
   - No → dispatch Claude Code with `/tr:initDoc` to generate it first
2. **`CLAUDE.md` in project root?** — verify cc-plugin config is present; fix if missing
3. **`git status`** — ensure working tree is clean enough to work on

### Phase 2: Spec Document

Generate a structured implementation spec using the **spec-writer** skill.

1. Activate `spec-writer` skill — read its SKILL.md and follow its workflow
2. It will gather project context, draft a spec using its template, and present to the user
3. The spec covers: objectives, user stories, technical plan, boundaries, verification criteria, and task breakdown
4. **Do not proceed until the user confirms the spec.**

The confirmed spec replaces the old requirement-doc + verification-doc pair — everything is in one document now.

> **Fallback:** If spec-writer skill is not installed, use the templates in `references/` (requirement-template.md + verification-template.md) as before.

### Phase 3: Task Decomposition & Agent Dispatch

After user confirms documents:

1. **Decompose** — break the requirement into ordered steps with dependencies
2. **For each step**, dispatch Claude Code:

```bash
claude --permission-mode bypassPermissions --print '<task prompt>' 2>&1
```

**Task prompt must include:**
- Clear description of what to do
- Relevant context (affected files, patterns to follow, constraints)
- "不要 git commit" (do not commit)
- "完成后执行 /update-doc 更新 llmdoc" (update llmdoc when done)
- Wake notification: `openclaw system event --text "Done: <summary>" --mode now`

**Use `workdir` to scope the agent** to the project directory.
**Use `background: true`** for long-running tasks, monitor with `process` tool.

**Execution rules:**
- Run steps with dependencies serially
- Independent steps may run in parallel (use git worktrees if needed)
- Monitor agent progress via `process action:log`
- Small errors (syntax, typos): re-prompt the agent to fix without bothering user
- Design-level issues or ambiguity: **stop and ask the user**

### Phase 4: Verification

After all steps complete, verify against the verification document:

1. **Automated verification** — run tests, build, lint as specified
2. **Functional verification** — execute test scenarios from the verification doc
3. **Code quality check** — style consistency, no stray files, no hardcoded secrets

### Phase 5: Delivery

Present results to the user with:

1. **All changed files** — every file touched, including llmdoc updates, config changes, everything
2. **Suggested commit message** — conventional commits format
3. **Verification results** — what passed, any caveats
4. **Items for human review** — what needs the user's attention

**Never commit.** The user handles all git commits.

## Agent Selection

Default: **Claude Code** (`claude --permission-mode bypassPermissions --print`)

| Agent | Use when |
|-------|----------|
| Claude Code | Default for all tasks; complex reasoning, architecture |
| Codex | User explicitly requests; batch/parallel tasks (`pty:true`, `--full-auto`) |
| OpenCode/Pi | User explicitly requests |

## Key Constraints

- **Never commit** — code changes only, user commits
- **Never run agents in `~/.openclaw/`** — agents will read soul/identity files
- **Always update llmdoc** — every agent run should end with doc update
- **Always list all changed files** on delivery
- **Always provide commit message** on delivery
- **Interrupt on design issues** — don't let agents drift on wrong assumptions
