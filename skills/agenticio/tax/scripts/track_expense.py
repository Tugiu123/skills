#!/usr/bin/env python3
"""Track deductible expense."""
import json
import os
import uuid
import argparse
from datetime import datetime

TAX_DIR = os.path.expanduser("~/.openclaw/workspace/memory/tax")
EXPENSES_FILE = os.path.join(TAX_DIR, "expenses.json")

def ensure_dir():
    os.makedirs(TAX_DIR, exist_ok=True)

def load_expenses():
    if os.path.exists(EXPENSES_FILE):
        with open(EXPENSES_FILE, 'r') as f:
            return json.load(f)
    return {"expenses": []}

def save_expenses(data):
    ensure_dir()
    with open(EXPENSES_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def main():
    parser = argparse.ArgumentParser(description='Track deductible expense')
    parser.add_argument('--amount', type=float, required=True, help='Expense amount')
    parser.add_argument('--category', required=True, help='Expense category')
    parser.add_argument('--date', default=datetime.now().strftime('%Y-%m-%d'), help='Date')
    parser.add_argument('--merchant', default='', help='Merchant name')
    parser.add_argument('--purpose', default='', help='Business purpose')
    
    args = parser.parse_args()
    
    exp_id = f"EXP-{str(uuid.uuid4())[:6].upper()}"
    
    expense = {
        "id": exp_id,
        "amount": args.amount,
        "category": args.category,
        "date": args.date,
        "merchant": args.merchant,
        "business_purpose": args.purpose,
        "logged_at": datetime.now().isoformat()
    }
    
    data = load_expenses()
    data['expenses'].append(expense)
    save_expenses(data)
    
    print(f"✓ Expense tracked: {exp_id}")
    print(f"  Amount: ${args.amount:,.2f}")
    print(f"  Category: {args.category}")
    print(f"  Date: {args.date}")
    if args.purpose:
        print(f"  Purpose: {args.purpose}")
    print(f"\n⚠️  Remember to save receipt!")

if __name__ == '__main__':
    main()
