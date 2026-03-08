---
name: bitrix24
description: Work with Bitrix24 (Битрикс24) via REST API and the official Bitrix24 MCP documentation server. Use when OpenClaw or Codex needs to manage CRM deals, contacts, leads, companies, tasks, checklists, comments, calendar events, drive files and folders, chats, notifications, users, departments, webhook setup, OAuth setup, or when it must find the exact Bitrix24 method, event, or article before making a call.
metadata:
  openclaw:
    requires:
      env:
        - BITRIX24_WEBHOOK_URL
      bins:
        - curl
      mcp:
        - url: https://mcp-dev.bitrix24.tech/mcp
          transport: streamable_http
          tools:
            - bitrix-search
            - bitrix-app-development-doc-details
            - bitrix-method-details
            - bitrix-article-details
            - bitrix-event-details
    primaryEnv: BITRIX24_WEBHOOK_URL
    emoji: "B24"
    homepage: https://github.com/rsvbitrix/openclaw-bitrix24
    aliases:
      - Bitrix24
      - bitrix24
      - Bitrix
      - bitrix
      - b24
      - Битрикс24
      - битрикс24
      - Битрикс
      - битрикс
    tags:
      - bitrix24
      - bitrix
      - b24
      - crm
      - tasks
      - calendar
      - drive
      - chat
      - messenger
      - im
      - webhook
      - oauth
      - mcp
      - Битрикс24
      - CRM
      - задачи
      - чат
---

# Bitrix24

Use this skill to work with Bitrix24 through two channels:

- direct REST calls through `BITRIX24_WEBHOOK_URL`
- official live documentation lookup through the Bitrix24 MCP server at `https://mcp-dev.bitrix24.tech/mcp`

The baseline used for this update is the previous OpenClaw project at `https://github.com/rsvbitrix/openclaw-bitrix24`, especially its old `skills/bitrix24` module split and setup notes.

## Start Here

1. If the user needs setup, credentials, webhook, or OAuth guidance, read `references/access.md`.
2. If webhook calls fail, env vars look wrong, or setup is unclear, read `references/troubleshooting.md` and run `scripts/check_webhook.py` before asking the user to debug manually.
3. If the exact Bitrix24 method, event, or article is unknown, read `references/mcp-workflow.md` and search before calling anything.
4. Then read the domain file that matches the task:
   - `references/crm.md`
   - `references/tasks.md`
   - `references/chat.md`
   - `references/calendar.md`
   - `references/drive.md`
   - `references/users.md`

## REST Call Pattern

Use the webhook URL as a prefix and append `<method>.json`:

```bash
curl -s "${BITRIX24_WEBHOOK_URL}<method>.json" -d '<params>'
```

Example:

```bash
curl -s "${BITRIX24_WEBHOOK_URL}crm.deal.list.json" \
  -d 'select[]=ID&select[]=TITLE&select[]=STAGE_ID'
```

`BITRIX24_WEBHOOK_URL` should look like:

```text
https://your-portal.bitrix24.ru/rest/<user_id>/<webhook>/
```

If the task is documentation-only and you only need live lookup through MCP, the MCP server still works even before a webhook is configured.

## MCP Workflow

Use the official MCP docs server in this order:

1. `bitrix-search` to find the exact method, event, or article title.
2. `bitrix-method-details` for REST methods.
3. `bitrix-event-details` for event docs.
4. `bitrix-article-details` for regular documentation articles.
5. `bitrix-app-development-doc-details` for OAuth, install callbacks, BX24 SDK, and app-development topics.

Important: do not guess method names from memory when the task is sensitive or the method family is large. Search first, then request exact details.

## Shared Rules

- Prefer server-side filtering with `filter[...]` and narrow output with `select[]`.
- Use `*.fields` or user-field discovery methods before writing custom fields.
- Expect pagination on list methods via `start` or method-specific `START`.
- Use ISO 8601 date-time strings when a method expects a date-time value.
- Treat `ACCESS_DENIED`, `insufficient_scope`, `QUERY_LIMIT_EXCEEDED`, and `expired_token` as normal operational cases.
- For `imbot.*`, persist and reuse the same `CLIENT_ID`; do not treat it as a public bot identifier.
- When a webhook call fails, do first-line diagnosis yourself: inspect `BITRIX24_WEBHOOK_URL`, check nearby `.env` files, normalize the URL, probe `user.current.json`, and summarize concrete findings instead of telling the user to run generic checks first.
- Never echo the full webhook secret back to the user; mask it in diagnostics.
- When the portal-specific configuration matters, verify the exact field names and examples with `bitrix-method-details`.
- For large or cross-entity operations, prefer batch or dedicated import methods only after checking current docs in MCP.

## Domain References

- `references/access.md` for webhook, OAuth, install callback, and legacy source notes.
- `references/troubleshooting.md` for webhook setup, DNS failures, env loading, and self-diagnostics.
- `references/mcp-workflow.md` for live docs discovery and tool selection.
- `references/crm.md` for deals, contacts, leads, companies, activities, and modern `crm.item.*` notes.
- `references/tasks.md` for tasks, checklists, comments, planner, and deprecated task APIs.
- `references/chat.md` for `im.*`, `imbot.*`, notifications, dialog history, and file-to-chat flows.
- `references/calendar.md` for sections, events, attendees, recurrence, and availability checks.
- `references/drive.md` for storage, folder, file, and external-link workflows.
- `references/users.md` for users, departments, org-structure lookups, and messenger-side search methods.

Read only the reference file that matches the current task.
