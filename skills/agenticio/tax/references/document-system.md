# Tax Document System

## The Year-Round System

Tax season arrives on schedule every year. The difference between stress and calm is whether documents were organized as they arrived or scrambled together under deadline pressure.

### The Core Principle
Information needed for taxes exists throughout your year — in bank statements, receipts, payroll records, donation confirmations. The problem is not that information doesn't exist. It's that nobody organized it as it arrived.

### Document Categories

| Category | Examples | When to Log |
|----------|----------|-------------|
| Income | W-2s, 1099s, K-1s | When received (Jan-Feb) |
| Expenses | Receipts, invoices | When incurred |
| Investments | 1099-B, 1099-DIV | When received |
| Property | Tax statements, mortgage interest | When received |
| Donations | Receipts, acknowledgments | When made |
| Medical | Bills, insurance statements | When paid |
| Business | Separate tracking for business expenses | Ongoing |

## Data Structure

```json
{
  "documents": [
    {
      "id": "DOC-123",
      "category": "income",
      "type": "1099-NEC",
      "issuer": "Client Corp",
      "amount": 15000,
      "date_received": "2024-01-31",
      "tax_year": 2024,
      "location": "filed",
      "notes": "Freelance project payments"
    }
  ],
  "expenses": [
    {
      "id": "EXP-456",
      "category": "business-meal",
      "amount": 85.50,
      "date": "2024-03-15",
      "merchant": "Business Lunch Spot",
      "deductible": true,
      "documentation": "receipt_saved",
      "business_purpose": "Client meeting"
    }
  ]
}
```

## Workflow

### When Document Arrives
1. Log immediately with `add_document.py`
2. Categorize by tax form type
3. Note if action required (estimated tax adjustment, etc.)
4. Store physical document in designated location

### Weekly Review
- Review logged expenses
- Ensure receipts match expenses
- Check for missing documentation
- Flag items needing professional consultation

### Monthly Summary
- Run expense summary by category
- Calculate estimated tax impact
- Adjust quarterly payments if needed
- Review for deduction opportunities

### Pre-Filing (January)
- Generate complete document inventory
- Identify missing documents
- Prepare summary for tax professional
- Organize everything by category
