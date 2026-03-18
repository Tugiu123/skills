#!/usr/bin/env python3
"""增强版股票AI分析助手 - 支持基础分析+追加专题分析"""

import sys, os, re, subprocess
sys.path.insert(0, os.path.dirname(__file__))
from data_fetcher import StockDataFetcher
from ai_client import call_ai
from stock_analyzer import analyze_company_basic, analyze_financial, analyze_valuation, analyze_shareholders, fundamental_analysis, technical_analysis

def parse_query(query):
    parts = re.split(r'[，,]', query)
    parts = [p.strip() for p in parts if p.strip()]
    if len(parts) < 2: return (query, "基本面", [])
    extras = []
    for p in parts[2:]:
        cleaned = re.sub(r'^(重点查询分析|重点分析|重点查询)', '', p).strip()
        if cleaned: extras.append(cleaned)
    return (parts[0], parts[1], extras)

def get_business_data(fetcher, ts_code):
    import pandas as pd
    mainbz_p = fetcher.get_main_business(ts_code, "P", 30)
    mainbz_d = fetcher.get_main_business(ts_code, "D", 30)
    out = []
    if mainbz_p is not None and not mainbz_p.empty:
        out.append("【主营构成-按产品】")
        for period in mainbz_p["end_date"].unique()[:2]:
            out.append(f"\n报告期:{period}")
            for _, row in mainbz_p[mainbz_p["end_date"]==period].head(10).iterrows():
                sales = row.get("bz_sales", 0)
                out.append(f"  - {row.get('bz_item','未知')}: {sales/10000:.1f}万")
    if mainbz_d is not None and not mainbz_d.empty:
        out.append("\n【主营构成-按地区】")
        for period in mainbz_d["end_date"].unique()[:2]:
            out.append(f"\n报告期:{period}")
            for _, row in mainbz_d[mainbz_d["end_date"]==period].head(10).iterrows():
                out.append(f"  - {row.get('bz_item','未知')}: {row.get('bz_sales',0)/10000:.1f}万")
    return "\n".join(out) if out else "暂无数据"

def analyze_topic(stock, ts_code, biz_data, req):
    prompt = f"""分析{stock}({ts_code})的{req}。
业务数据：{biz_data[:2000]}
请给出专业分析（200-300字）。"""
    return call_ai(prompt)

def enhanced_analysis(stock_query, extras):
    print(f"[搜索]{stock_query}...")
    fetcher = StockDataFetcher()
    info = fetcher.search_stock(stock_query)
    if not info: return f"未找到:{stock_query}"
    ts_code, name = info['ts_code'], info['name']
    print(f"[找到]{name}({ts_code})")
    
    sections = [f"📊[{name}({ts_code})增强版分析]", "="*70]
    
    print("[1/5]公司概况...")
    sections.extend(["\n🏢公司概况", "-"*50, analyze_company_basic(fetcher, ts_code, name)])
    
    print("[2/5]财务分析...")
    sections.extend(["\n📈财务质量", "-"*50, analyze_financial(fetcher, ts_code)])
    
    print("[3/5]估值分析...")
    sections.extend(["\n💰估值分析", "-"*50, analyze_valuation(fetcher, ts_code, name)])
    
    print("[4/5]股东分析...")
    sections.extend(["\n👥股东结构", "-"*50, analyze_shareholders(fetcher, ts_code)])
    
    if extras:
        print("[5/5]专题分析...")
        biz = get_business_data(fetcher, ts_code)
        sections.extend(["\n"+"="*70, "🔍深度专题", "="*70])
        for i, req in enumerate(extras, 1):
            print(f"  [{i}/{len(extras)}]{req}...")
            sections.extend([f"\n📌专题{i}:{req}", "-"*50, analyze_topic(name, ts_code, biz, req)])
        sections.extend(["\n📋参考数据", "-"*50, biz])
    
    sections.extend(["\n"+"="*70, "⚠️免责声明：以上分析基于公开历史数据，不构成投资建议。"])
    return "\n".join(sections)

def main():
    if len(sys.argv) < 2:
        print("用法:\n  enhanced_analyzer.py \"股票,基本面,重点分析xxx\"")
        return
    
    if len(sys.argv) == 2:
        stock, typ, extras = parse_query(sys.argv[1])
    else:
        stock, typ = sys.argv[1], sys.argv[2] if len(sys.argv)>2 else "基本面"
        extras = sys.argv[3:] if len(sys.argv)>3 else []
    
    if typ == "基本面":
        result = enhanced_analysis(stock, extras) if extras else fundamental_analysis(stock)
    elif typ == "技术面":
        result = technical_analysis(stock)
    else:
        result = f"未知类型:{typ}"
    
    print(result)

if __name__ == "__main__":
    import io
    if sys.platform == 'win32':
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    main()
