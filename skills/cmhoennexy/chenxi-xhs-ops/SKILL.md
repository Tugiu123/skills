---
name: xhs-ops
description: >
  Xiaohongshu (小红书) end-to-end operations skill: hot topic research, post writing
  with built-in audit, automated commenting with rate limiting, and cover image
  generation. Powered by xiaohongshu-mcp for native platform API access.
  Use when: searching Xiaohongshu trends, writing posts, automating comments,
  generating cover images, or any Xiaohongshu content workflow.
  Triggers: "搜热点", "找选题", "写一篇", "出内容", "发评论", "做封面",
  "xiaohongshu", "小红书", "XHS", "search hot topics", "write post",
  "auto comment", "generate cover".
---

# XHS-Ops — Xiaohongshu Operations Toolkit

4 tools for Xiaohongshu content operations, all backed by [xiaohongshu-mcp](https://github.com/xpzouying/xiaohongshu-mcp).

## Prerequisites

1. **xiaohongshu-mcp** binary running at `http://localhost:18060/mcp`
2. **Playwright Chromium** installed (for cover generation)
3. Run `bash scripts/setup.sh` for one-click dependency install

```bash
# Quick start
bash scripts/setup.sh
# Verify MCP is running
curl -s http://localhost:18060/mcp
```

## Tools

### 🔥 search-hot — Find trending topics

```bash
python3 scripts/search_hot.py                        # Use default keywords from config
python3 scripts/search_hot.py "Claude Code" "AI写代码" # Custom keywords
```

Returns Top 10 posts sorted by likes: title, author, likes/collects/comments, source keyword.
Saves results to `/tmp/xhs-search-results.json` for other tools to consume.

### 📝 write-post — Generate post content

Agent workflow — not a standalone script. Use the prompt and audit functions:

```python
from scripts.write_post import get_write_prompt, audit_post, format_audit_report

# 1. Generate writing prompt
prompt = get_write_prompt("3个AI Agent每晚自动开会", reference="optional context")

# 2. Send prompt to LLM, get back title + body + tags

# 3. Audit before publishing
result = audit_post(title="标题", body="正文", tags="#tag1 #tag2")
print(format_audit_report(result))
```

Audit checks: sensitive words, title length (≤20), body length (≤500), trailing question, numeric specificity, tag count (5-8).

### 💬 comment — Automated commenting

```bash
python3 scripts/comment.py --dry-run --count 5   # Preview only
python3 scripts/comment.py --count 10             # Post comments
```

Requires search-hot results. Random interval 3-8 min between comments. Daily limit configurable.

For single comment via Agent:

```python
from scripts.comment import post_single_comment
result = post_single_comment(feed_id, xsec_token, "评论内容")
# Returns {"status": "ok"} or {"status": "blocked", "reason": "敏感词: ..."}
```

### 🎨 cover — Generate cover images

```bash
python3 scripts/cover.py "主标题" "副标题" -o ~/covers/output.png
```

Uses hand-drawn notebook style template. Playwright screenshots at 2x scale → 1200×1600 PNG.
Replace `assets/cover_template.html` to change visual style.

## Configuration

Edit `scripts/config.json`:

```json
{
  "keywords": ["Claude Code 实战", "AI写代码 程序员"],
  "mcp_url": "http://localhost:18060/mcp",
  "comment_interval_min": 180,
  "comment_interval_max": 480,
  "daily_comment_limit": 15
}
```

## Content Rules

See `references/content_rules.md` for:
- Writing style guide (接地气、短句、移动端友好)
- Sensitive word blacklist (platform names, absolute claims, solicitation)
- Post structure template (hook → points → details → CTA)
- Comment generation guidelines

## Oral Script Template

See `references/koubo.md` for converting posts to video narration scripts.

## MCP Session Notes

- Each tool call requires a fresh `initialize` to get a Session ID
- `xsec_token` from search results cannot be reused across sessions
- Cookie expires ~30 days; re-login: `./xiaohongshu-login-darwin-arm64`
