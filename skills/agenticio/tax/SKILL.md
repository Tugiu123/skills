---
name: tax
description: Personal and business tax organization with local document management. Use when user mentions tax preparation, tax documents, deductions, filing taxes, IRS notices, or estimated tax payments. Tracks documents year-round, identifies deductions, prepares for tax professional meetings, and manages tax deadlines. NEVER provides tax advice or replaces licensed tax professionals.
---

# Tax

Tax document organization system. Year-round preparation, stress-free filing.

## Critical Privacy & Safety

### Data Storage (CRITICAL)
- **All tax data stored locally only**: `memory/tax/`
- **No external APIs** for tax data storage
- **No connection** to IRS or tax authority systems
- **No document cloud uploads** - local storage only
- User controls all data retention and deletion

### Safety Boundaries (NON-NEGOTIABLE)
- ✅ Organize tax documents and receipts
- ✅ Track deductible expenses year-round
- ✅ Calculate estimated tax payments
- ✅ Prepare for tax professional meetings
- ❌ **NEVER provide tax advice** or filing recommendations
- ❌ **NEVER calculate final tax liability** (jurisdiction-specific)
- ❌ **NEVER replace** licensed tax professionals
- ❌ **NEVER interpret tax law** or regulations

### Legal Disclaimer
Tax law is jurisdiction-specific, changes frequently, and depends on individual circumstances. This skill provides organization and preparation support only. Always work with a licensed tax professional for filing and complex situations.

## Quick Start

### Data Storage Setup
Tax records stored in your local workspace:
- `memory/tax/documents.json` - Tax document inventory
- `memory/tax/expenses.json` - Deductible expense tracking
- `memory/tax/estimated_payments.json` - Quarterly payment records
- `memory/tax/meetings.json` - Tax professional meeting prep
- `memory/tax/deadlines.json` - Tax deadlines and reminders

Use provided scripts in `scripts/` for all data operations.

## Core Workflows

### Add Tax Document
```
User: "I received a 1099 from my client"
→ Use scripts/add_document.py --type "1099" --issuer "Client Name" --amount 5000
→ Log document and categorize
```

### Track Deductible Expense
```
User: "$200 business meal today"
→ Use scripts/track_expense.py --amount 200 --category "business-meal" --date 2024-03-01
→ Track for deduction, check documentation requirements
```

### Calculate Estimated Tax
```
User: "How much estimated tax should I pay this quarter?"
→ Use scripts/calculate_estimate.py --quarter Q1 --income 15000
→ Calculate based on income to date and safe harbor rules
```

### Prepare for Tax Meeting
```
User: "Prep me for my accountant meeting"
→ Use scripts/prep_meeting.py --year 2024
→ Generate organized summary of all documents and expenses
```

### Check Deadline
```
User: "When is my estimated tax due?"
→ Use scripts/check_deadlines.py
→ Show upcoming tax deadlines
```

## Module Reference

For detailed implementation:
- **Document Organization**: See [references/document-system.md](references/document-system.md)
- **Deduction Tracking**: See [references/deductions.md](references/deductions.md)
- **Estimated Taxes**: See [references/estimated-taxes.md](references/estimated-taxes.md)
- **Tax Meeting Prep**: See [references/meeting-prep.md](references/meeting-prep.md)
- **IRS Notices**: See [references/irs-notices.md](references/irs-notices.md)
- **Year-End Planning**: See [references/year-end.md](references/year-end.md)

## Scripts Reference

| Script | Purpose |
|--------|---------|
| `add_document.py` | Log tax document receipt |
| `track_expense.py` | Track deductible expense |
| `calculate_estimate.py` | Calculate estimated tax payment |
| `check_deadlines.py` | Show upcoming tax deadlines |
| `prep_meeting.py` | Prepare for tax professional meeting |
| `generate_summary.py` | Create tax year summary |
| `log_irs_notice.py` | Log and track IRS correspondence |
| `set_reminder.py` | Set tax deadline reminders |

## Disclaimer

This skill provides document organization and preparation support only. Tax law varies by jurisdiction and changes frequently. Always work with a licensed tax professional for filing and complex situations.
