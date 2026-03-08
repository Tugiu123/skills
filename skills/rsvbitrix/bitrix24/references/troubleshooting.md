# Troubleshooting

Use this file when webhook setup is broken, the agent cannot reach the portal, or a user asks for help configuring access.

## Default Behavior

Do the first diagnosis yourself before asking the user to copy env vars, confirm internet access, or rerun the same command manually.

Preferred order:

1. inspect current `BITRIX24_WEBHOOK_URL`
2. inspect nearby `.env` files if needed
3. validate webhook format
4. resolve DNS for the host
5. probe `user.current.json`
6. report concrete findings and the next fix

Prefer the bundled script:

```bash
python3 <path-to-skill>/scripts/check_webhook.py --json
```

## Typical Failure: curl Exit Code 6

`curl` exit code `6` usually means the host could not be resolved.

Likely causes:

- malformed `BITRIX24_WEBHOOK_URL`
- typo in the portal domain
- env var not loaded in the current shell/session
- stale or missing `.env`
- local DNS or network issue

When you see this:

1. run the webhook check script
2. verify whether the URL came from the environment or an env file
3. mask the secret and show only the host and source
4. if DNS fails, say that clearly instead of vaguely saying "JSON formatting problem"

## Typical Failure: Missing Env

If `BITRIX24_WEBHOOK_URL` is missing:

- check `.env`
- check `.env.local`
- check the current workspace root
- only ask the user for the webhook if no local source exists

Do not ask the user to retype the webhook until you have checked those places.

## Typical Failure: Bad Format

Expected format:

```text
https://your-portal.bitrix24.ru/rest/<user_id>/<webhook>/
```

Common mistakes:

- missing trailing slash
- copied portal URL instead of webhook URL
- extra quotes or spaces
- wrong user ID segment

## Typical Failure: HTTP 401 or Auth Errors

Usually indicates:

- revoked webhook
- wrong secret
- expired OAuth token
- invalid app auth context

Next actions:

- probe `user.current.json`
- if OAuth is used, verify token freshness and scope
- if webhook is used, ask the user to regenerate or verify the webhook in Bitrix24

## Typical Failure: `ACCESS_DENIED` or `insufficient_scope`

Usually indicates missing permissions.

Tell the user exactly which scope family is likely missing:

- CRM
- Tasks
- Calendar
- Disk
- IM
- `imbot`

Do not just say "permissions issue" without naming the likely scope.

## User-Facing Style

Prefer:

- what you checked
- what failed
- what is already confirmed working
- one next action

Avoid:

- long generic lists of shell commands for the user
- asking for confirmation before a simple retry you can do yourself
- exposing the full webhook secret
