# CRM

Use this file for deals, contacts, companies, leads, activities, and modern CRM item APIs.

## Core Families

Classic entities:

- `crm.deal.list`
- `crm.deal.get`
- `crm.deal.add`
- `crm.deal.update`
- `crm.deal.delete`
- `crm.contact.add`
- `crm.company.add`
- `crm.lead.add`
- `crm.activity.list`
- `crm.activity.add`
- `crm.activity.update`

Relationship and metadata helpers:

- `crm.deal.contact.add`
- `crm.deal.contact.items.get`
- `crm.company.contact.add`
- `crm.contact.company.add`
- `crm.contact.company.items.get`
- `crm.contact.company.items.set`
- `crm.deal.fields`
- `crm.lead.fields`
- `crm.deal.userfield.list`
- `crm.dealcategory.fields`
- `crm.category.fields`

Modern generalized APIs:

- `crm.item.list`
- `crm.item.delete`
- `crm.item.batchImport`

Use `crm.item.*` for smart processes, dynamic types, or generalized CRM object flows.

## Working Rules

- Read `*.fields` before writing custom or portal-specific fields.
- Do not hardcode stage names across portals. Pipelines and categories vary.
- Use classic `crm.deal.*` and related methods for common built-in entities.
- Use `crm.item.*` only after confirming the target object type and field schema.

## Minimal Examples

Create a deal:

```bash
curl -s "${BITRIX24_WEBHOOK_URL}crm.deal.add.json" \
  -d 'fields[TITLE]=New Deal&fields[OPPORTUNITY]=50000&fields[CURRENCY_ID]=RUB'
```

Add an activity to a deal:

```bash
curl -s "${BITRIX24_WEBHOOK_URL}crm.activity.add.json" \
  -d 'fields[OWNER_TYPE_ID]=2&fields[OWNER_ID]=123&fields[TYPE_ID]=2&fields[SUBJECT]=Meeting'
```

List deals with a server-side filter:

```bash
curl -s "${BITRIX24_WEBHOOK_URL}crm.deal.list.json" \
  -d 'filter[>OPPORTUNITY]=10000&select[]=ID&select[]=TITLE&select[]=OPPORTUNITY'
```

## Good MCP Queries

- `crm deal add update stage category`
- `crm contact company relation`
- `crm lead fields`
- `crm activity`
- `crm smart process item`
