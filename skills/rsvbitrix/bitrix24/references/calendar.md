# Calendar

Use this file for personal calendars, group calendars, meetings, sections, recurrence, and availability checks.

## Core Methods

- `calendar.section.get`
- `calendar.section.add`
- `calendar.section.delete`
- `calendar.event.get`
- `calendar.event.getbyid`
- `calendar.event.add`
- `calendar.event.update`
- `calendar.event.delete`
- `calendar.accessibility.get`
- `calendar.meeting.status.get`

The current MCP server also surfaced user and resource settings methods, but the list above covers the most common agent workflows.

## Working Rules

- Pass calendar type explicitly, usually `user`, `group`, or `company_calendar`.
- Use `ownerId` with the correct owner for that calendar type.
- Use `calendar.event.getbyid` when you already know the event ID.
- For attendee conflicts or meeting scheduling, check `calendar.accessibility.get` before proposing a slot.
- Keep time zone handling explicit in date-time values.

## Minimal Examples

Create an event:

```bash
curl -s "${BITRIX24_WEBHOOK_URL}calendar.event.add.json" \
  -d 'type=user&ownerId=1&name=Team Meeting&from=2026-03-01T10:00:00&to=2026-03-01T11:00:00'
```

List events in a range:

```bash
curl -s "${BITRIX24_WEBHOOK_URL}calendar.event.get.json" \
  -d 'type=user&ownerId=1&from=2026-03-01&to=2026-03-31'
```

Get a single event:

```bash
curl -s "${BITRIX24_WEBHOOK_URL}calendar.event.getbyid.json" \
  -d 'id=123'
```

Check availability:

```bash
curl -s "${BITRIX24_WEBHOOK_URL}calendar.accessibility.get.json" \
  -d 'users[]=1&users[]=2&from=2026-03-01&to=2026-03-02'
```

## Recurrence

Recurring rules are carried in `rrule[...]`. Re-check exact supported fields with `bitrix-method-details calendar.event.add` before generating complicated recurrence payloads.

## Good MCP Queries

- `calendar event section`
- `calendar accessibility`
- `calendar recurrence`
