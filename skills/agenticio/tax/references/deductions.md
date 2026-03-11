# Deduction Tracking

## Understanding Deductions vs Credits

**Deductions** reduce taxable income. If you're in the 24% bracket, a $1,000 deduction saves $240 in taxes.

**Credits** reduce tax directly. A $1,000 credit saves $1,000 in taxes.

## Common Deduction Categories

### For Everyone
- State and local taxes (SALT) - capped at $10,000
- Mortgage interest
- Charitable contributions
- Medical expenses (above 7.5% of AGI)

### For Business Owners/Self-Employed
- Home office
- Business mileage
- Professional development
- Business meals (50% deductible)
- Equipment and supplies
- Professional subscriptions

### Often Missed
- Student loan interest
- Educator expenses
- Health savings account contributions
- Self-employment tax (deductible portion)
- Startup costs (first year)

## Documentation Requirements

| Deduction Type | Documentation Needed | Retention Period |
|----------------|---------------------|------------------|
| Business expense | Receipt + business purpose note | 7 years |
| Mileage | Log: date, miles, purpose | 7 years |
| Charitable donation | Receipt or acknowledgment | 7 years |
| Home office | Square footage calculation | 7 years |
| Medical | Bills + proof of payment | 7 years |

## Tracking System

```json
{
  "deductions": {
    "2024": {
      "business_expenses": [
        {
          "date": "2024-03-15",
          "category": "business_meal",
          "amount": 85.50,
          "deductible_amount": 42.75,
          "documentation": "receipt_plus_notes",
          "business_purpose": "Client acquisition meeting with XYZ Corp"
        }
      ],
      "summary": {
        "total_deductions": 12500,
        "largest_category": "business_expenses",
        "documentation_complete": "95%"
      }
    }
  }
}
```

## Red Flags to Avoid

- Personal expenses labeled as business
- Round numbers (guessed, not actual)
- Missing documentation
- Expenses that don't match income level
- Home office that's also personal space
