---
name: chonkie-deepresearch
description: "Run deep research queries using Chonkie DeepResearch. Returns comprehensive research reports with citations — useful for market analysis, competitive intelligence, technical deep dives, and any research-heavy task."
homepage: https://chonkie.ai
metadata:
  {
    "openclaw":
      {
        "emoji": "🔬",
        "requires": { "bins": ["chdr"] },
        "tags": ["research", "deep-research", "analysis", "reports", "chonkie"]
      }
  }
---

# Chonkie DeepResearch

Run deep research queries from your agent and get comprehensive reports with citations.

## Setup

Before using, check if `chdr` is installed (`which chdr`). If not:

1. Install: `cargo install chdr`
   - If `cargo` isn't available, install Rust first: `curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh`
2. Authenticate: `chdr auth login` (opens browser to get an API key)
   - Or set `CHONKIE_API_KEY` environment variable
   - Get a key at https://labs.chonkie.ai/settings/api-keys

## Usage

When the user asks you to research something, or when you need to gather information for a task:

### Running research

```bash
# Run research and save JSON output (takes 2-10 minutes)
chdr research --type report --no-stream --json "<query>" > /tmp/chdr-research.json

# Extract markdown body for reading
python3 -c "
import json
data = json.load(open('/tmp/chdr-research.json'))
print(data.get('content', {}).get('body', ''))
" > /tmp/chdr-research.md
```

Run the research command in the background since it takes several minutes. Inform the user it's running.

### After research completes

1. Extract the `id` and `title` from the JSON
2. Give the user the web URL: `https://labs.chonkie.ai/research/{id}`
3. Read only the first 100 lines of the `.md` file for a summary
4. Tell the user you can answer questions — you'll read specific sections on demand

### Answering follow-up questions

- Grep the `.md` file to find relevant sections before reading
- Use offset/limit to read only the matching section
- NEVER read the entire file into context — reports can be 20,000+ lines

### Other commands

```bash
chdr ls                    # List recent research
chdr ls --limit 20         # List more
chdr view <id>             # View a report (supports partial ID prefix)
chdr open <id>             # Open in browser
chdr delete <id>           # Delete a report
```

All commands that take an ID support prefix matching — `chdr view 3a6b` works if unambiguous.
