#!/usr/bin/env python3
"""
账本图表绘制脚本
用法: python3 plot_ledger.py <账本路径> --type line --start 2024-01-01 --end 2024-12-31 --output chart.png
"""

import json
import argparse
from datetime import datetime
from pathlib import Path
from collections import defaultdict
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# 设置英文支持
plt.rcParams['axes.unicode_minus'] = False


def load_transactions(ledger_path):
    """流式读取 JSONL 交易记录"""
    transactions_file = Path(ledger_path) / "transactions.jsonl"
    transactions = []
    try:
        with open(transactions_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:
                    transactions.append(json.loads(line))
        return transactions
    except FileNotFoundError:
        return []


def filter_by_date(transactions, start_date=None, end_date=None):
    """按日期筛选交易"""
    result = []
    for t in transactions:
        t_date = t.get('date', '')
        if start_date and t_date < start_date:
            continue
        if end_date and t_date > end_date:
            continue
        result.append(t)
    return result


def calculate_daily_balance(transactions, start_date, end_date, use_history=True):
    """计算每日余额
    
    Args:
        transactions: 所有交易记录
        start_date: 开始日期
        end_date: 结束日期
        use_history: 是否使用历史期初数据，默认True
    """
    init_balance = 0
    
    if use_history:
        # 找所有交易中最早的记录作为期初起点
        earliest_record = None
        for t in transactions:
            if earliest_record is None or t.get('date', '') < earliest_record.get('date', ''):
                earliest_record = t
        if earliest_record:
            init_balance = float(earliest_record.get('amount', 0))
            print(f"期初结余: {init_balance}")
    else:
        print(f"期初结余: 0 (不含历史数据)")
    
    # 按日期累计收支（正数=收入，负数=支出）
    daily_amounts = defaultdict(float)
    
    for t in transactions:
        date = t.get('date', '')
        if date < start_date or date > end_date:
            continue
        # 如果不使用历史期初数据，跳过2025-12-31的期初记录
        if not use_history and date < start_date:
            continue
        daily_amounts[date] += float(t.get('amount', 0))
    
    # 排序并计算累计余额
    sorted_dates = sorted(daily_amounts.keys())
    dates = []
    balance = init_balance  # 从期初结余开始
    balances = []
    
    for date in sorted_dates:
        balance += daily_amounts[date]
        dates.append(datetime.strptime(date, '%Y-%m-%d'))
        balances.append(balance)
    
    return dates, balances


def calculate_category_summary(transactions, trans_type='expense'):
    """按分类汇总"""
    category_amounts = defaultdict(float)
    
    for t in transactions:
        amount = float(t.get('amount', 0))
        if trans_type == 'expense' and amount >= 0:
            continue
        if trans_type == 'income' and amount <= 0:
            continue
        category = t.get('category', '其他')
        category_amounts[category] += abs(amount)
    
    return dict(sorted(category_amounts.items(), key=lambda x: x[1], reverse=True))


def plot_line(dates, balances, output_path):
    """绘制折线图 - 余额变化"""
    fig, ax = plt.subplots(figsize=(12, 6))
    
    ax.plot(dates, balances, marker='o', linewidth=2, markersize=4, color='#2E86AB')
    ax.fill_between(dates, balances, alpha=0.3, color='#2E86AB')
    
    ax.set_xlabel('Date', fontsize=12)
    ax.set_ylabel('Balance', fontsize=12)
    ax.set_title('Ledger Balance', fontsize=14, fontweight='bold')
    
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))
    ax.xaxis.set_major_locator(mdates.AutoDateLocator())
    plt.xticks(rotation=45)
    
    ax.grid(True, alpha=0.3)
    ax.axhline(y=0, color='r', linestyle='--', alpha=0.5)
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"图表已保存至: {output_path}")


def plot_bar(categories, amounts, output_path, title='分类统计'):
    """绘制柱状图"""
    fig, ax = plt.subplots(figsize=(10, 6))
    
    colors = plt.cm.Set3(range(len(categories)))
    bars = ax.bar(categories, amounts, color=colors)
    
    ax.set_xlabel('分类', fontsize=12)
    ax.set_ylabel('金额', fontsize=12)
    ax.set_title(title, fontsize=14, fontweight='bold')
    
    # 添加数值标签
    for bar, amount in zip(bars, amounts):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{amount:.2f}',
                ha='center', va='bottom', fontsize=9)
    
    plt.xticks(rotation=45, ha='right')
    ax.grid(True, axis='y', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"图表已保存至: {output_path}")


def plot_pie(categories, amounts, output_path, title='支出占比'):
    """绘制饼图"""
    fig, ax = plt.subplots(figsize=(10, 8))
    
    colors = plt.cm.Pastel1(range(len(categories)))
    wedges, texts, autotexts = ax.pie(
        amounts, 
        labels=categories,
        autopct='%1.1f%%',
        colors=colors,
        explode=[0.02] * len(categories),
        shadow=False
    )
    
    ax.set_title(title, fontsize=14, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"图表已保存至: {output_path}")


def main():
    parser = argparse.ArgumentParser(description='账本图表绘制工具')
    parser.add_argument('ledger_path', help='账本路径')
    parser.add_argument('--type', choices=['line', 'bar', 'pie'], default='line',
                        help='图表类型: line(折线图), bar(柱状图), pie(饼图)')
    parser.add_argument('--start', help='开始日期 (YYYY-MM-DD)')
    parser.add_argument('--end', help='结束日期 (YYYY-MM-DD)')
    parser.add_argument('--output', required=True, help='输出文件路径')
    parser.add_argument('--trans-type', choices=['income', 'expense'], default='expense',
                        help='交易类型 (用于柱状图/饼图，expense=支出，income=收入)')
    parser.add_argument('--no-history', action='store_true',
                        help='不使用历史期初数据，从0开始累计')
    
    args = parser.parse_args()
    
    # 加载数据
    transactions = load_transactions(args.ledger_path)
    if not transactions:
        print("没有找到交易记录")
        return
    
    # 筛选日期
    start_date = args.start or '2000-01-01'
    end_date = args.end or '2099-12-31'
    filtered = filter_by_date(transactions, start_date, end_date)
    
    if not filtered:
        print("指定日期范围内没有交易记录")
        return
    
    # 绘制图表
    if args.type == 'line':
        dates, balances = calculate_daily_balance(transactions, start_date, end_date, use_history=not args.no_history)
        if not dates:
            print("没有足够的数据绘制折线图")
            return
        plot_line(dates, balances, args.output)
    
    elif args.type == 'bar':
        summary = calculate_category_summary(filtered, args.trans_type)
        if not summary:
            print(f"没有{args.trans_type}类型的交易")
            return
        title = '收入分类统计' if args.trans_type == 'income' else '支出分类统计'
        plot_bar(list(summary.keys()), list(summary.values()), args.output, title=title)
    
    elif args.type == 'pie':
        summary = calculate_category_summary(filtered, args.trans_type)
        if not summary:
            print(f"没有{args.trans_type}类型的交易")
            return
        # 合并小额分类为"其他"
        total = sum(summary.values())
        main_categories = {k: v for k, v in summary.items() if v / total >= 0.03}
        other_amount = total - sum(main_categories.values())
        if other_amount > 0:
            main_categories['其他'] = other_amount
        title = '收入占比分布' if args.trans_type == 'income' else '支出占比分布'
        plot_pie(list(main_categories.keys()), list(main_categories.values()), args.output, title=title)


if __name__ == '__main__':
    main()
