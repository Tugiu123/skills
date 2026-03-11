#!/usr/bin/env python3
"""Add tax document to system."""
import json
import os
import uuid
import argparse
from datetime import datetime

TAX_DIR = os.path.expanduser("~/.openclaw/workspace/memory/tax")
DOCS_FILE = os.path.join(TAX_DIR, "documents.json")

def ensure_dir():
    os.makedirs(TAX_DIR, exist_ok=True)

def load_docs():
    if os.path.exists(DOCS_FILE):
        with open(DOCS_FILE, 'r') as f:
            return json.load(f)
    return {"documents": []}

def save_docs(data):
    ensure_dir()
    with open(DOCS_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def main():
    parser = argparse.ArgumentParser(description='Add tax document')
    parser.add_argument('--type', required=True, help='Document type (W-2, 1099, etc)')
    parser.add_argument('--issuer', required=True, help='Who issued the document')
    parser.add_argument('--amount', type=float, required=True, help='Amount')
    parser.add_argument('--tax-year', type=int, default=2024, help='Tax year')
    
    args = parser.parse_args()
    
    doc_id = f"DOC-{str(uuid.uuid4())[:6].upper()}"
    
    doc = {
        "id": doc_id,
        "type": args.type,
        "issuer": args.issuer,
        "amount": args.amount,
        "tax_year": args.tax_year,
        "date_received": datetime.now().isoformat(),
        "location": "pending_filing"
    }
    
    data = load_docs()
    data['documents'].append(doc)
    save_docs(data)
    
    print(f"✓ Document logged: {doc_id}")
    print(f"  Type: {args.type}")
    print(f"  Issuer: {args.issuer}")
    print(f"  Amount: ${args.amount:,.2f}")
    print(f"  Tax Year: {args.tax_year}")

if __name__ == '__main__':
    main()
