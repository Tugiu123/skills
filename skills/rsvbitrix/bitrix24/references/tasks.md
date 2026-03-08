# Tasks

Use this file for task CRUD, delegation, checklists, comments, planner data, and task API migration notes.

## Preferred Modern APIs

Core task methods:

- `tasks.task.list`
- `tasks.task.get`
- `tasks.task.add`
- `tasks.task.update`
- `tasks.task.complete`
- `tasks.task.renew`
- `tasks.task.delegate`
- `tasks.task.delete`
- `tasks.task.favorite.add`

Checklist methods:

- `task.checklistitem.add`
- `task.checklistitem.getlist`
- `task.checklistitem.complete`
- `task.checklistitem.renew`
- `task.checklistitem.delete`

Comment methods:

- `task.commentitem.add`
- `task.commentitem.getlist`

Planner:

- `task.planner.getlist`

## Deprecated APIs

The MCP server still knows about `task.item.*`, but it marks methods like `task.item.list` and `task.item.addtofavorite` as deprecated. Prefer `tasks.task.*` when there is a modern equivalent.

## Statuses

Useful legacy status values from the earlier skill baseline:

- `1` new
- `2` waiting
- `3` in progress
- `4` supposedly completed
- `5` completed
- `6` deferred

Verify with live docs if the portal or plan changes behavior.

## Minimal Examples

Create a task:

```bash
curl -s "${BITRIX24_WEBHOOK_URL}tasks.task.add.json" \
  -d 'fields[TITLE]=Task title&fields[RESPONSIBLE_ID]=1&fields[PRIORITY]=2'
```

Add a checklist item:

```bash
curl -s "${BITRIX24_WEBHOOK_URL}task.checklistitem.add.json" \
  -d 'TASKID=456&FIELDS[TITLE]=Subtask text'
```

Add a comment:

```bash
curl -s "${BITRIX24_WEBHOOK_URL}task.commentitem.add.json" \
  -d 'TASKID=456&FIELDS[POST_MESSAGE]=Comment text'
```

## Good MCP Queries

- `tasks checklist comments planner`
- `tasks favorite`
- `task item deprecated`
