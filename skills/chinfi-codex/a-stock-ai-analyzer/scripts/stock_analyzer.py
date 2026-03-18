#!/usr/bin/env python3
"""
股票AI分析主脚本
基本面数据使用 10-公司投研专家.py 中的方法
估值部分使用 financial_ratios.py 模块
"""

import sys
import os
import re
from typing import Optional, Dict, Any

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from data_fetcher import StockDataFetcher, convert_to_ts_code
from financial_ratios import FinancialAnalyzer
from ai_client import call_ai, clean_ai_output

# Prompt模板 - 对齐 10-公司投研专家.py
DEFAULT_PROMPTS = {
    "company_basic": """你是一位专业的投资分析师，请根据以下公司信息生成一段简洁的总结（80-120字）：

{text}

请涵盖：
1. 主营业务和行业地位
2. 核心竞争力或特色
3. 潜在关注点

要求：简洁专业，突出投资亮点和风险。""",

    "financial": """你是一位资深财务分析师，请对以下原始财务数据进行深度质量评估和异常巡查。

原始财务数据：
{text}

请从以下维度进行专业分析（150-200字）：

1. **盈利质量分析**
   - 扣非净利润与净利润的差异（是否存在非经常性损益粉饰）
   - 毛利率、净利率的稳定性和趋势
   - 利润含金量（经营现金流与净利润匹配度）

2. **资产负债健康度**
   - 资产负债率水平和变化趋势
   - 流动比率、速动比率反映的短期偿债能力
   - 有息负债比例和财务杠杆风险

3. **营运效率评估**
   - 应收账款周转、存货周转效率
   - 总资产周转率趋势
   - 是否存在资产周转放缓风险

4. **异常信号巡查**
   - 收入与利润增长是否匹配
   - 是否存在季节性或周期性异常波动
   - 关键财务指标的突变点和可能原因
   - 潜在的财务粉饰或风险信号

要求：
- 不要简单罗列数据，重在分析质量、趋势和异常
- 指出具体的财务风险点和需关注的指标
- 语言专业简洁，突出核心判断""",

    "shareholders": """请根据以下股东和管理层数据，生成一段简洁的股权结构分析总结（150-200字）：

{text}

请重点分析：
1. **主要股东**：前3大股东是谁？持股性质（国有/民营/机构）？
2. **大股东占比**：前5大、前10大股东合计持股比例？股权集中度如何？
3. **社保基金**：是否有社保基金持股？如有，持股比例多少？
4. **管理层持股**：管理层合计持股数量及占总股本比例？激励机制如何？

要求：
- 数据要准确，提及具体股东名称和持股比例
- 分析股权结构稳定性和治理风险
- 语言简洁专业，适合投资者快速了解股权结构""",

    "technical": """你是一位资深股票技术分析师，请根据以下K线数据进行专业技术分析。

【股票】{stock_name}

【最新价格数据】
当前价：{current_price:.2f}元
今日涨跌：{change_pct:+.2f}%
今日振幅：{amplitude:.2f}%

【均线系统】
MA5：{ma5:.2f}元 {ma5_signal}
MA10：{ma10:.2f}元 {ma10_signal}
MA20：{ma20:.2f}元 {ma20_signal}
{ma60_line}
均线排列：{ma_alignment}

【MACD指标】
DIF：{macd:.3f}
DEA：{signal:.3f}
MACD柱：{histogram:.3f}
信号：{macd_signal}

【RSI(14)】
当前值：{rsi:.2f}
状态：{rsi_status}

【KDJ(9,3,3)】
K：{k:.2f}
D：{d:.2f}
J：{j:.2f}
信号：{kdj_signal}

【近期K线数据（最近60个交易日）】
{klines}

请提供以下技术分析（简洁专业，200-300字）：

1. **趋势分析**：当前处于什么趋势？均线系统给出什么信号？

2. **技术指标研判**：
   - MACD、RSI、KDJ是否共振？
   - 是否有超买/超卖信号？
   - 是否有金叉/死叉信号？

3. **形态识别**：
   - 是否形成头肩顶/底、双顶/底、三角形等经典形态？
   - 关键支撑/阻力位在哪里？

4. **技术面综合判断**：
   - 多空力量对比
   - 短期操作策略建议（看多/看空/观望）
   - 关键价位（止损/止盈参考）

要求：
- 基于上述数据客观分析
- 给出明确的操作倾向
- 风险提示必不可少"""
}


def analyze_company_basic(fetcher: StockDataFetcher, ts_code: str, stock_name: str) -> str:
    """分析公司基本情况 - 使用 10-公司投研专家.py 方法"""
    company_info = fetcher.get_stock_basic_info(ts_code)
    if company_info is None:
        return "暂无公司信息数据"
    
    # 补充股票基本信息
    all_stocks = fetcher.get_all_stocks()
    if not all_stocks.empty:
        stock_basic = all_stocks[all_stocks["ts_code"] == ts_code]
        if not stock_basic.empty:
            company_info.update(stock_basic.iloc[0].to_dict())
    
    prompt_template = DEFAULT_PROMPTS["company_basic"]
    
    text = f"""公司名称：{company_info.get('name', '-')}
所属行业：{company_info.get('industry', '-')}
注册地：{company_info.get('area', '-')}
上市日期：{company_info.get('list_date', '-')}
公司介绍：{company_info.get('introduction', '-')[:500]}..."""
    
    prompt = prompt_template.format(text=text)
    return call_ai(prompt)


def analyze_financial(fetcher: StockDataFetcher, ts_code: str) -> str:
    """分析财务指标 - 使用 10-公司投研专家.py 方法"""
    import pandas as pd
    
    fina_df = fetcher.get_financial_indicators(ts_code, limit=12)
    if fina_df is None or fina_df.empty:
        return "暂无财务数据可供分析"
    
    prompt_template = DEFAULT_PROMPTS["financial"]
    
    # 构建财务数据文本 - 对齐 10-公司投研专家.py 格式
    fina_df = fina_df.sort_values("end_date", ascending=False).head(8)
    text_lines = []
    
    for _, row in fina_df.iterrows():
        period = row.get("end_date", "-")
        text_lines.append(f"\n【报告期：{period}】")
        
        # 收入利润指标
        revenue = row.get("total_revenue_ps", None)
        profit = row.get("profit_dedt", None)
        net_profit = row.get("netprofit_margin", None)
        text_lines.append(f"  营收：{revenue:.2f}元/股" if pd.notna(revenue) else "  营收：无")
        text_lines.append(f"  扣非净利润：{profit:.2f}元" if pd.notna(profit) else "  扣非净利润：无")
        text_lines.append(f"  销售净利率：{net_profit:.2f}%" if pd.notna(net_profit) else "  销售净利率：无")
        
        # 盈利能力
        roe = row.get("roe", None)
        gross_margin = row.get("grossprofit_margin", None)
        text_lines.append(f"  ROE：{roe:.2f}%" if pd.notna(roe) else "  ROE：无")
        text_lines.append(f"  毛利率：{gross_margin:.2f}%" if pd.notna(gross_margin) else "  毛利率：无")
        
        # 资产负债
        debt_ratio = row.get("debt_to_assets", None)
        current_ratio = row.get("current_ratio", None)
        quick_ratio = row.get("quick_ratio", None)
        text_lines.append(f"  资产负债率：{debt_ratio:.2f}%" if pd.notna(debt_ratio) else "  资产负债率：无")
        text_lines.append(f"  流动比率：{current_ratio:.2f}" if pd.notna(current_ratio) else "  流动比率：无")
        text_lines.append(f"  速动比率：{quick_ratio:.2f}" if pd.notna(quick_ratio) else "  速动比率：无")
        
        # 现金流
        cfps = row.get("cfps", None)
        text_lines.append(f"  每股现金流：{cfps:.2f}" if pd.notna(cfps) else "  每股现金流：无")
    
    text = "\n".join(text_lines)
    prompt = prompt_template.format(text=text)
    return call_ai(prompt)


def analyze_valuation(fetcher: StockDataFetcher, ts_code: str, stock_name: str) -> str:
    """估值分析 - 使用 financial_ratios.py 进行估值计算"""
    import pandas as pd
    
    # 获取市场数据
    market_data = fetcher.get_market_data(ts_code)
    current_price = market_data.get("price")
    total_shares = market_data.get("total_shares")
    
    if not current_price or not total_shares:
        return "暂无足够数据进行估值分析"
    
    # 获取财务指标数据计算估值
    fina_df = fetcher.get_financial_indicators(ts_code, limit=8)
    if fina_df is None or fina_df.empty:
        return "暂无财务数据进行估值"
    
    # 获取最新期数据
    latest = fina_df.iloc[0]
    
    # 计算EPS和估值指标
    eps = None
    if "eps" in latest and pd.notna(latest["eps"]):
        eps = float(latest["eps"])
    elif "basic_eps" in latest and pd.notna(latest["basic_eps"]):
        eps = float(latest["basic_eps"])
    
    if not eps or eps <= 0:
        return "因缺少有效EPS数据，无法进行估值分析"
    
    # 计算估值指标
    pe = current_price / eps if eps > 0 else None
    
    # 构建简单的估值分析文本
    bvps = latest.get("bps", None)  # 每股净资产
    pb = current_price / float(bvps) if bvps and pd.notna(bvps) and float(bvps) > 0 else None
    
    # 三情景估值
    base_pe = pe if pe else 20.0
    base_eps_growth = 0.15
    
    scenarios = []
    
    # Base情景
    base_target = eps * (1 + base_eps_growth) * base_pe
    scenarios.append({
        "name": "Base（基准）",
        "target": base_target,
        "upside": (base_target - current_price) / current_price * 100,
        "pe": base_pe,
        "growth": base_eps_growth * 100,
    })
    
    # Optimistic情景
    opt_pe = base_pe * 1.2
    opt_growth = base_eps_growth + 0.10
    opt_target = eps * (1 + opt_growth) * opt_pe
    scenarios.append({
        "name": "Optimistic（乐观）",
        "target": opt_target,
        "upside": (opt_target - current_price) / current_price * 100,
        "pe": opt_pe,
        "growth": opt_growth * 100,
    })
    
    # Stress情景
    stress_pe = base_pe * 0.7
    stress_growth = max(base_eps_growth - 0.10, -0.20)
    stress_target = eps * (1 + stress_growth) * stress_pe
    scenarios.append({
        "name": "Stress（压力）",
        "target": stress_target,
        "upside": (stress_target - current_price) / current_price * 100,
        "pe": stress_pe,
        "growth": stress_growth * 100,
    })
    
    # 生成分析文本
    output = []
    output.append(f"当前股价: {current_price:.2f}元")
    output.append(f"当前EPS(TTM): {eps:.2f}元")
    output.append(f"当前PE: {pe:.1f}倍" if pe else "当前PE: N/A")
    output.append(f"当前PB: {pb:.1f}倍" if pb else "当前PB: N/A")
    output.append("")
    output.append("估值情景推演:")
    output.append(f"{'情景':<20} {'目标价':>10} {'空间':>10} {'PE假设':>8} {'增速假设':>8}")
    output.append("-" * 65)
    
    for s in scenarios:
        ud_str = f"{s['upside']:+.1f}%"
        output.append(f"{s['name']:<20} {s['target']:>10.2f} {ud_str:>10} {s['pe']:>8.1f} {s['growth']:>7.1f}%")
    
    return "\n".join(output)


def analyze_shareholders(fetcher: StockDataFetcher, ts_code: str) -> str:
    """分析股东和管理层 - 使用 10-公司投研专家.py 方法"""
    import pandas as pd
    
    holders_df = fetcher.get_top10_holders(ts_code, limit=4)
    managers_df = fetcher.get_managers(ts_code)
    rewards_df = fetcher.get_manager_rewards(ts_code)
    
    prompt_template = DEFAULT_PROMPTS["shareholders"]
    
    # 构建分析文本 - 对齐 10-公司投研专家.py 格式
    text_lines = []
    
    # 股东数据
    if holders_df is not None and not holders_df.empty:
        latest_period = holders_df["end_date"].iloc[0]
        period_df = holders_df[holders_df["end_date"] == latest_period].copy()
        period_df = period_df.sort_values("hold_ratio", ascending=False)
        
        text_lines.append(f"【十大股东数据 - 报告期：{latest_period}】")
        text_lines.append(f"股东总数：{len(period_df)}家")
        
        top5_ratio = period_df.head(5)["hold_ratio"].sum() if len(period_df) >= 5 else period_df["hold_ratio"].sum()
        top10_ratio = period_df["hold_ratio"].sum()
        text_lines.append(f"前5大股东合计持股：{top5_ratio:.2f}%")
        text_lines.append(f"前10大股东合计持股：{top10_ratio:.2f}%")
        
        text_lines.append("\n主要股东详情：")
        for idx, row in period_df.head(5).iterrows():
            holder_name = row.get("holder_name", "-")
            hold_ratio = row.get("hold_ratio", 0)
            text_lines.append(f"- {holder_name}: {hold_ratio:.2f}%")
        
        # 检查社保基金
        social_security = period_df[period_df["holder_name"].str.contains("社保|全国社会保障", na=False, case=False)]
        if not social_security.empty:
            text_lines.append(f"\n社保基金持股：")
            for idx, row in social_security.iterrows():
                text_lines.append(f"- {row['holder_name']}: {row['hold_ratio']:.2f}%")
        else:
            text_lines.append("\n社保基金持股：无")
    
    # 管理层数据
    if rewards_df is not None and not rewards_df.empty:
        text_lines.append(f"\n【管理层持股数据】")
        total_hold = rewards_df["hold_vol"].sum()
        
        # 估算总股本
        total_shares = 0
        if holders_df is not None and not holders_df.empty:
            latest_period = holders_df["end_date"].iloc[0]
            period_df = holders_df[holders_df["end_date"] == latest_period]
            if not period_df.empty and "hold_ratio" in period_df.columns and "hold_amount" in period_df.columns:
                first_row = period_df.iloc[0]
                if first_row["hold_ratio"] > 0:
                    total_shares = first_row["hold_amount"] / (first_row["hold_ratio"] / 100)
        
        mgmt_ratio = (total_hold / total_shares * 100) if total_shares > 0 else 0
        text_lines.append(f"管理层合计持股：{total_hold:,.0f}股")
        text_lines.append(f"管理层持股比例：{mgmt_ratio:.4f}%")
        text_lines.append(f"管理层人数：{len(rewards_df)}人")
    
    # 管理层名单
    if managers_df is not None and not managers_df.empty:
        text_lines.append(f"\n【管理层名单】")
        for idx, row in managers_df.head(5).iterrows():
            name = row.get("name", "-")
            title = row.get("title", "-")
            text_lines.append(f"- {name}: {title}")
    
    text = "\n".join(text_lines) if text_lines else "暂无股东及管理层数据"
    prompt = prompt_template.format(text=text)
    return call_ai(prompt)


def analyze_technical(fetcher: StockDataFetcher, ts_code: str, stock_name: str) -> str:
    """技术分析"""
    import pandas as pd
    import numpy as np
    
    df_daily = fetcher.get_daily_prices(ts_code, count=60)
    if df_daily is None or df_daily.empty:
        return "暂无数据可供技术分析"
    
    df = df_daily.tail(60).copy()
    
    # 构建K线数据文本
    klines = []
    for idx, row in df.iterrows():
        date_str = idx.strftime('%m-%d') if hasattr(idx, 'strftime') else str(idx)[:5]
        klines.append(f"{date_str}: 开{row['open']:.2f} 高{row['high']:.2f} 低{row['low']:.2f} 收{row['close']:.2f} 量{row['vol']/10000:.1f}万")
    
    # 计算均线
    ma5 = df['close'].rolling(5).mean().iloc[-1]
    ma10 = df['close'].rolling(10).mean().iloc[-1]
    ma20 = df['close'].rolling(20).mean().iloc[-1]
    ma60 = df['close'].rolling(60).mean().iloc[-1] if len(df) >= 60 else None
    
    # MACD
    exp1 = df['close'].ewm(span=12, adjust=False).mean()
    exp2 = df['close'].ewm(span=26, adjust=False).mean()
    macd_line = exp1 - exp2
    signal_line = macd_line.ewm(span=9, adjust=False).mean()
    
    # RSI
    delta = df['close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    
    # KDJ
    low_list = df['low'].rolling(window=9, min_periods=9).min()
    high_list = df['high'].rolling(window=9, min_periods=9).max()
    rsv = (df['close'] - low_list) / (high_list - low_list) * 100
    k_line = rsv.ewm(com=2, adjust=False).mean()
    d_line = k_line.ewm(com=2, adjust=False).mean()
    j_line = 3 * k_line - 2 * d_line
    
    latest = df.iloc[-1]
    prev = df.iloc[-2] if len(df) > 1 else latest
    
    technical_data = {
        'stock_name': stock_name,
        'current_price': latest['close'],
        'change_pct': (latest['close']/prev['close']-1)*100 if prev['close'] != 0 else 0,
        'amplitude': (latest['high']/latest['low']-1)*100 if latest['low'] != 0 else 0,
        'ma5': ma5,
        'ma10': ma10,
        'ma20': ma20,
        'ma60': ma60 if ma60 is not None else 0,
        'ma5_signal': '↑' if latest['close'] > ma5 else '↓',
        'ma10_signal': '↑' if latest['close'] > ma10 else '↓',
        'ma20_signal': '↑' if latest['close'] > ma20 else '↓',
        'ma60_line': f"MA60：{ma60:.2f}元 {'↑' if latest['close'] > ma60 else '↓'}" if ma60 else '',
        'ma_alignment': '多头排列' if ma5 > ma10 > ma20 else '空头排列' if ma5 < ma10 < ma20 else '缠绕',
        'macd': macd_line.iloc[-1],
        'signal': signal_line.iloc[-1],
        'histogram': (macd_line.iloc[-1] - signal_line.iloc[-1])*2,
        'macd_signal': '金叉' if macd_line.iloc[-1] > signal_line.iloc[-1] and macd_line.iloc[-2] <= signal_line.iloc[-2] else '死叉' if macd_line.iloc[-1] < signal_line.iloc[-1] and macd_line.iloc[-2] >= signal_line.iloc[-2] else 'DIF在DEA上方' if macd_line.iloc[-1] > signal_line.iloc[-1] else 'DIF在DEA下方',
        'rsi': rsi.iloc[-1],
        'rsi_status': '超买(>70)' if rsi.iloc[-1] > 70 else '超卖(<30)' if rsi.iloc[-1] < 30 else '中性',
        'k': k_line.iloc[-1],
        'd': d_line.iloc[-1],
        'j': j_line.iloc[-1],
        'kdj_signal': '金叉' if k_line.iloc[-1] > d_line.iloc[-1] and k_line.iloc[-2] <= d_line.iloc[-2] else '死叉' if k_line.iloc[-1] < d_line.iloc[-1] and k_line.iloc[-2] >= d_line.iloc[-2] else 'K在D上方' if k_line.iloc[-1] > d_line.iloc[-1] else 'K在D下方',
        'klines': '\n'.join(klines)
    }
    
    prompt_template = DEFAULT_PROMPTS["technical"]
    prompt = prompt_template.format(**technical_data)
    return call_ai(prompt)


def fundamental_analysis(stock_query: str) -> str:
    """基本面分析主函数"""
    print(f"[搜索] 正在搜索股票: {stock_query}...")
    
    fetcher = StockDataFetcher()
    stock_info = fetcher.search_stock(stock_query)
    
    if stock_info is None:
        return f"❌ 未找到股票: {stock_query}\n请检查股票名称或代码是否正确。"
    
    ts_code = stock_info['ts_code']
    stock_name = stock_info['name']
    
    print(f"[成功] 找到股票: {stock_name} ({ts_code})")
    print("[分析] 正在获取数据并分析...\n")
    
    output = []
    output.append(f"📊 [{stock_name} ({ts_code}) 基本面分析]")
    output.append("=" * 60)
    
    # 公司概况
    print("[1/4] 分析公司概况...")
    output.append("\n🏢 公司概况")
    output.append("-" * 40)
    basic_summary = analyze_company_basic(fetcher, ts_code, stock_name)
    output.append(basic_summary)
    
    # 财务分析
    print("[2/4] 分析财务指标...")
    output.append("\n📈 财务质量分析")
    output.append("-" * 40)
    financial_summary = analyze_financial(fetcher, ts_code)
    output.append(financial_summary)
    
    # 估值分析
    print("[3/4] 估值情景推演...")
    output.append("\n💰 估值分析")
    output.append("-" * 40)
    valuation_summary = analyze_valuation(fetcher, ts_code, stock_name)
    output.append(valuation_summary)
    
    # 股东分析
    print("[4/4] 分析股东结构...")
    output.append("\n👥 股东与管理层")
    output.append("-" * 40)
    shareholder_summary = analyze_shareholders(fetcher, ts_code)
    output.append(shareholder_summary)
    
    output.append("\n" + "=" * 60)
    output.append("⚠️ 免责声明：以上分析基于公开历史数据，不构成投资建议。")
    
    return "\n".join(output)


def technical_analysis(stock_query: str) -> str:
    """技术面分析主函数"""
    print(f"[搜索] 正在搜索股票: {stock_query}...")
    
    fetcher = StockDataFetcher()
    stock_info = fetcher.search_stock(stock_query)
    
    if stock_info is None:
        return f"❌ 未找到股票: {stock_query}\n请检查股票名称或代码是否正确。"
    
    ts_code = stock_info['ts_code']
    stock_name = stock_info['name']
    
    print(f"✅ 找到股票: {stock_name} ({ts_code})")
    print("[分析] 正在获取K线数据并分析...\n")
    
    output = []
    output.append(f"📈 [{stock_name} ({ts_code}) 技术面分析]")
    output.append("=" * 60)
    
    # 获取当前价格
    current_price = fetcher.get_current_price(ts_code)
    if current_price:
        output.append(f"\n当前股价: {current_price:.2f}元")
        output.append("-" * 40)
    
    # 技术分析
    print("[分析] 进行技术分析...")
    technical_summary = analyze_technical(fetcher, ts_code, stock_name)
    output.append(technical_summary)
    
    output.append("\n" + "=" * 60)
    output.append("⚠️ 免责声明：以上分析基于历史技术数据，不构成投资建议。")
    output.append("📌 股市有风险，投资需谨慎。")
    
    return "\n".join(output)


def main():
    """主函数"""
    if len(sys.argv) < 3:
        print("""
╔══════════════════════════════════════════════════════════════╗
║              股票AI分析助手                                  ║
╚══════════════════════════════════════════════════════════════╝

使用方法:
    python stock_analyzer.py <股票名称/代码> <分析类型>
    
分析类型:
    基本面  - 深度基本面分析（财务+估值+股东）
    技术面  - 分析技术形态（K线、均线、指标）
    
示例:
    python stock_analyzer.py 贵州茅台 基本面
    python stock_analyzer.py 000001 技术面
""")
        sys.exit(1)
    
    stock_query = sys.argv[1]
    analysis_type = sys.argv[2]
    
    if analysis_type == "基本面":
        result = fundamental_analysis(stock_query)
    elif analysis_type == "技术面":
        result = technical_analysis(stock_query)
    else:
        print(f"❌ 未知的分析类型: {analysis_type}")
        print("支持的分析类型: 基本面、技术面")
        sys.exit(1)
    
    print(result)


if __name__ == "__main__":
    import io
    import sys
    # Redirect stdout to handle encoding properly
    if sys.platform == 'win32':
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    main()
