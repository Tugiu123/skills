#!/usr/bin/env python3
"""
账本快速输出表格工具
用法: python3 print_ledger.py <账本路径> <月份> [月份2] ...
示例: python3 print_ledger.py ~/.openclaw/skills_data/ledger/兔兔 2026-01
      python3 print_ledger.py ~/.openclaw/skills_data/ledger/兔兔 2026-01 2026-02 2026-03

【重要】统计逻辑：
- 只统计用户指定的月份（不含期初结余）
- 如果用户只指定部分月份，显示的是该月当月收入/支出
- 如果指定了"全部"或所有月份，则自动包含2025-12的期初结余
"""

import json
import sys
from pathlib import Path
from datetime import datetime
from collections import defaultdict

def load_all_transactions(ledger_path):
    """加载所有交易记录（包括各月目录）"""
    base_path = Path(ledger_path)
    transactions = []
    
    # 1. 扫描所有月份目录
    for item in base_path.iterdir():
        if item.is_dir() and item.name.startswith("202"):
            trans_file = item / "transactions.jsonl"
            if trans_file.exists():
                with open(trans_file, 'r', encoding='utf-8') as f:
                    for line in f:
                        line = line.strip()
                        if line:
                            transactions.append(json.loads(line))
    
    # 2. 如果没有月份目录，尝试根目录的 transactions.jsonl
    if not transactions:
        root_file = base_path / "transactions.jsonl"
        if root_file.exists():
            with open(root_file, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line:
                        transactions.append(json.loads(line))
    
    return sorted(transactions, key=lambda x: x.get("date", ""))

def get_init_balance(ledger_path):
    """获取期初结余（2025-12-31的记录）"""
    base_path = Path(ledger_path)
    init_file = base_path / "2025-12" / "transactions.jsonl"
    
    if init_file.exists():
        with open(init_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:
                    t = json.loads(line)
                    if "结余" in t.get("description", "") or "init" in t.get("id", "").lower():
                        return t.get("amount", 0)
    
    # 尝试从根目录找
    root_file = base_path / "transactions.jsonl"
    if root_file.exists():
        with open(root_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:
                    t = json.loads(line)
                    if t.get("date", "") == "2025-12-31":
                        return t.get("amount", 0)
    
    return 0

def filter_by_months(transactions, months):
    """筛选指定月份的交易"""
    if not months:
        return transactions
    return [t for t in transactions if any(t.get("date", "").startswith(m) for m in months)]

def print_month_report(ledger_name, ledger_path, transactions, months):
    """打印指定月份的报表"""
    # 筛选指定月份
    month_trans = filter_by_months(transactions, months)
    
    if not month_trans:
        print(f"❌ 没有找到 {months} 的交易记录")
        return
    
    # 不需要期初结余，所有月份数据直接累加
    need_init = False
    
    init_balance = 0
    
    # 按月份分组显示
    for month in sorted(months):
        trans = [t for t in month_trans if t.get("date", "").startswith(month)]
        if not trans:
            continue
        
        print(f"\n## 📊 {ledger_name} - {month} 月明细")
        print("\n| 日期 | 分类 | 金额 | 账户 | 备注 |")
        print("|------|------|------|------|------|")
        
        for t in sorted(trans, key=lambda x: x.get("date", "")):
            date = t.get("date", "")[5:]  # 只显示月日
            cat = t.get("category", "其他")
            amount = t.get("amount", 0)
            account = t.get("account", "现金")
            desc = t.get("description", "")
            amt_str = f"+{amount}" if amount > 0 else str(amount)
            print(f"| {date} | {cat} | {amt_str} | {account} | {desc} |")
        
        income = sum(t.get("amount", 0) for t in trans if t.get("amount", 0) > 0 and "结余" not in t.get("description", ""))
        expense = sum(t.get("amount", 0) for t in trans if t.get("amount", 0) < 0 and "结余" not in t.get("description", ""))
        
        print(f"\n### 📈 {month} 月汇总")
        print(f"| 项目 | 金额 |")
        print(f"|------|------|")
        print(f"| 本月收入 | +{income} |")
        print(f"| 本月支出 | {expense} |")
        print(f"| **本月净收支** | **{income + expense}** |")
    
    # 总体汇总（跳过结余记录）
    total_income = sum(t.get("amount", 0) for t in month_trans if t.get("amount", 0) > 0 and "结余" not in t.get("description", ""))
    total_expense = sum(t.get("amount", 0) for t in month_trans if t.get("amount", 0) < 0 and "结余" not in t.get("description", ""))
    
    print(f"\n### 🐰 总体汇总")
    if need_init:
        print(f"| 项目 | 金额 |")
        print(f"|------|------|")
        print(f"| 期初结余 | {init_balance} |")
        print(f"| 总收入 | +{total_income} |")
        print(f"| 总支出 | {total_expense} |")
        print(f"| **期末余额** | **{init_balance + total_income + total_expense}** |")
    else:
        print(f"| 项目 | 金额 |")
        print(f"|------|------|")
        print(f"| 总收入 | +{total_income} |")
        print(f"| 总支出 | {total_expense} |")
        print(f"| **净收支** | **{total_income + total_expense}** |")

def main():
    if len(sys.argv) < 3:
        print("用法: python3 print_ledger.py <账本路径> <月份> [月份2] ...")
        print("      python3 print_ledger.py ~/.openclaw/skills_data/ledger/兔兔 2026-01")
        print("      python3 print_ledger.py ~/.openclaw/skills_data/ledger/兔兔 2026-01 2026-02 2026-03")
        print("      python3 print_ledger.py ~/.openclaw/skills_data/ledger/兔兔 全部")
        print("\n【说明】")
        print("- 统计指定月份时，只显示当月收入/支出（不含期初结余）")
        print("- 输入'全部'时，包含期初结余")
        sys.exit(1)
    
    ledger_path = sys.argv[1]
    months = sys.argv[2:]
    
    # 获取账本名称
    ledger_name = Path(ledger_path).name
    
    # 加载所有交易
    transactions = load_all_transactions(ledger_path)
    
    if not transactions:
        print(f"❌ 没有找到交易记录在 {ledger_path}")
        sys.exit(1)
    
    # 判断用户是否输入"全部"
    user_input_all = any(m.lower() in ['all', '全部', '所有'] for m in months)
    
    if user_input_all:
        # 统计全部，转换为所有月份
        all_months = sorted(set(t.get("date", "")[:7] for t in transactions if t.get("date", "")))
        months = all_months
    
    # 输出报表
    print_month_report(ledger_name, ledger_path, transactions, months)

if __name__ == "__main__":
    main()
