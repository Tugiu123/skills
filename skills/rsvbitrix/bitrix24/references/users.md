# Users and Structure

Use this file for user lookup, department structure, messenger-side org search, and colleague or manager resolution.

## Core Methods

Users:

- `user.current`
- `user.get`
- `user.search`

Departments:

- `department.get`
- `department.add`
- `department.update`
- `department.delete`
- `department.fields`

Messenger-side org helpers:

- `im.department.get`
- `im.department.employees.get`
- `im.department.managers.get`
- `im.department.colleagues.list`
- `im.search.user.list`
- `im.search.department.list`

UI-only helper surfaced by search:

- `BX24.selectUsers`

Treat `BX24.selectUsers` as a frontend helper, not a server-side agent method.

## Working Rules

- Use `user.current` to verify which identity the webhook or token is acting as.
- Use `user.search` for fast fuzzy person lookups.
- Use `department.get` for structure data and tree traversal.
- Use `im.department.*` when the task is clearly messenger or org-navigation oriented.
- Verify field names like `UF_DEPARTMENT` with live docs if the portal has custom behavior.

## Minimal Examples

Get the current identity:

```bash
curl -s "${BITRIX24_WEBHOOK_URL}user.current.json"
```

Search users:

```bash
curl -s "${BITRIX24_WEBHOOK_URL}user.search.json" \
  -d 'FILTER[NAME]=Ivan'
```

List departments:

```bash
curl -s "${BITRIX24_WEBHOOK_URL}department.get.json"
```

Get employees of a department:

```bash
curl -s "${BITRIX24_WEBHOOK_URL}im.department.employees.get.json" \
  -d 'ID[]=5'
```

## Good MCP Queries

- `user department structure intranet`
- `im department employees managers`
- `user search`
