# Access and Auth

## Legacy Baseline Used For This Update

- Previous OpenClaw repository: `https://github.com/rsvbitrix/openclaw-bitrix24`
- Previous skill entrypoint: `skills/bitrix24/SKILL.md`
- Previous access notes came from the old project README and plugin config

Use those legacy notes as historical context only. Prefer current MCP docs when there is any doubt.

## Fastest Setup: Inbound Webhook

1. In Bitrix24 open `Developer resources -> Other -> Inbound webhook`.
2. Create a webhook and copy its URL.
3. Store it in `BITRIX24_WEBHOOK_URL`.

Expected format:

```text
https://your-portal.bitrix24.ru/rest/<user_id>/<webhook>/
```

Use that value as the base prefix for REST calls:

```bash
curl -s "${BITRIX24_WEBHOOK_URL}user.current.json"
```

## Agent Setup Behavior

When a user asks for setup help or a REST call fails, do not immediately push manual shell steps back to the user.

Instead:

1. inspect the current `BITRIX24_WEBHOOK_URL` value yourself
2. check nearby `.env` files if the environment variable is missing
3. normalize the webhook URL to ensure it ends with `/`
4. probe `user.current.json`
5. only then ask the user for missing information or blocked access

Mask the webhook secret in user-facing output.

## Permissions

Grant the permission groups that match the methods you will call.

Recommended full-coverage set for this skill:

- CRM
- Tasks
- Calendar
- Disk or Drive
- IM or Chat
- user and department related access

If you are also using the historical OpenClaw messenger plugin flow from `openclaw-bitrix24`, keep `imbot`, `im`, and `disk` enabled as well. That recommendation comes from the previous plugin README and plugin manifest, not from the MCP server itself.

## `CLIENT_ID` For Bot Integrations

For `imbot` integrations, Bitrix24 bot registration requires `CLIENT_ID`.

Operational rule:

- provide `CLIENT_ID` when registering the bot
- persist it as part of the bot credentials
- pass the same `CLIENT_ID` into all later `imbot.*` calls

Treat `CLIENT_ID` as a secret. It is part of the control boundary that prevents unrelated callers from operating someone else's bot.

Historical implementation note from the earlier Claw integration:

- `CLIENT_ID` was derived deterministically from `md5(webhook)`

That is acceptable as an integration strategy when all of the following are true:

- the resulting value is stable for the same bot
- the underlying webhook secret is not exposed
- the integration stores and reuses the same derived value consistently

## Official MCP Docs Endpoint

Bitrix24 documentation is exposed through:

```text
https://mcp-dev.bitrix24.tech/mcp
```

Observed endpoint behavior on March 8, 2026:

- `GET` without `Accept: text/event-stream` returned `406 Not Acceptable`
- `initialize` succeeded with protocol version `2025-03-26`
- server info reported `b24-dev-mcp` version `0.2.0`

Current tools exposed by the server:

- `bitrix-search`
- `bitrix-app-development-doc-details`
- `bitrix-method-details`
- `bitrix-article-details`
- `bitrix-event-details`

## When To Use OAuth Instead Of A Webhook

Use a webhook when:

- you are connecting one portal quickly
- the integration is admin-managed
- you want the shortest setup path

Use OAuth when:

- your service lives outside Bitrix24
- users connect their own portals to your service
- you need renewable tokens instead of a fixed webhook secret

The official Bitrix24 app-development doc says the full OAuth flow is for external services and does not apply to local webhooks.

Key official docs:

- Full OAuth: `https://apidocs.bitrix24.ru/settings/oauth/index.html`
- REST call overview: `https://apidocs.bitrix24.ru/sdk/bx24-js-sdk/how-to-call-rest-methods/index.html`
- Install callback: `https://apidocs.bitrix24.ru/settings/app-installation/mass-market-apps/installation-callback.html`

## OAuth Facts Confirmed From MCP Docs

- The authorization server is `https://oauth.bitrix24.tech/`
- Authorization starts by sending the user to `https://portal.bitrix24.com/oauth/authorize/`
- The temporary authorization `code` is valid for 30 seconds
- Token exchange happens at `https://oauth.bitrix24.tech/oauth/token/`
- Successful token exchange returns `access_token`, `refresh_token`, `client_endpoint`, `server_endpoint`, and `scope`

Useful exact MCP titles for app/auth topics:

- `Полный протокол авторизации OAuth 2.0`
- `Упрощенный вариант получения токенов OAuth 2.0`
- `Вызов методов REST`
- `Callback установки`

## Install Callback For UI-Less Apps

If you build a local or UI-less app, Bitrix24 can POST OAuth credentials to an install callback URL immediately after installation. That flow is documented in `Callback установки`.

For that scenario:

- save the received `access_token` and `refresh_token`
- refresh access tokens on your backend
- do not rely on browser-side JS install helpers for the callback flow

## Quick Probe

For fast diagnosis, prefer the bundled script:

```bash
python3 <path-to-skill>/scripts/check_webhook.py
```

Useful variants:

```bash
python3 <path-to-skill>/scripts/check_webhook.py --json
python3 <path-to-skill>/scripts/check_webhook.py --env-file .env --json
python3 <path-to-skill>/scripts/check_webhook.py --url "https://portal.bitrix24.ru/rest/1/secret/"
```
