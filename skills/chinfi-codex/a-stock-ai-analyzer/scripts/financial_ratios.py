#!/usr/bin/env python3
"""
财务比率计算模块
基于 calc_fundamental_ratios.py 整合优化
支持：核心财务比率计算、估值指标、异常检测、估值情景推演
"""

import json
from typing import Any, Optional
from dataclasses import dataclass
from datetime import datetime


# 字段别名映射（支持中英文输入）
FIELD_ALIASES: dict[str, tuple[str, ...]] = {
    "period": ("period", "报告期", "end_date"),
    "revenue": ("revenue", "营业收入", "total_revenue"),
    "gross_profit": ("gross_profit", "毛利润", "毛利", "grossprofit"),
    "operating_income": ("operating_income", "营业利润", "operate_profit"),
    "net_income": ("net_income", "净利润", "归母净利润", "n_income_attr_p"),
    "ebit": ("ebit", "息税前利润"),
    "ebitda": ("ebitda", "税息折旧摊销前利润"),
    "operating_cash_flow": ("operating_cash_flow", "经营活动现金流净额", "n_cashflow_act", "ocf"),
    "capital_expenditure": ("capital_expenditure", "资本开支", "c_acq_assets"),
    "total_assets": ("total_assets", "总资产", "total_assets"),
    "total_equity": ("total_equity", "股东权益", "净资产", "total_hldr_eqy_exc_min_int"),
    "total_debt": ("total_debt", "有息负债", "total_liab"),
    "current_assets": ("current_assets", "流动资产", "total_cur_assets"),
    "current_liabilities": ("current_liabilities", "流动负债", "total_cur_liab"),
    "inventory": ("inventory", "存货", "inventories"),
    "shares_outstanding": ("shares_outstanding", "总股本", "total_share"),
}

MARKET_ALIASES: dict[str, tuple[str, ...]] = {
    "price": ("price", "股价", "close"),
    "market_cap": ("market_cap", "总市值"),
    "enterprise_value": ("enterprise_value", "企业价值", "ev"),
}


# ============ 工具函数 ============

def to_float(value: Any) -> float | None:
    """转换为浮点数，失败返回None"""
    if value is None:
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def safe_div(numerator: float | None, denominator: float | None) -> float | None:
    """安全除法"""
    if numerator is None or denominator in (None, 0):
        return None
    return numerator / denominator


def yoy_growth(current: float | None, previous: float | None) -> float | None:
    """同比增长率"""
    if current is None or previous in (None, 0):
        return None
    return (current - previous) / abs(previous)


def average_two(current: float | None, previous: float | None) -> float | None:
    """计算平均值"""
    if current is None:
        return None
    if previous is None:
        return current
    return (current + previous) / 2.0


def pick_value(row: dict[str, Any], canonical_key: str) -> Any:
    """从行数据中按别名获取值"""
    for key in FIELD_ALIASES.get(canonical_key, (canonical_key,)):
        if key in row and row[key] is not None:
            return row.get(key)
    return None


def pick_market_value(row: dict[str, Any], canonical_key: str) -> Any:
    """从市场数据中按别名获取值"""
    for key in MARKET_ALIASES.get(canonical_key, (canonical_key,)):
        if key in row and row[key] is not None:
            return row.get(key)
    return None


def format_ratio(value: float | None, precision: int = 2, percentage: bool = False) -> str:
    """格式化比率输出"""
    if value is None:
        return "N/A"
    if percentage:
        return f"{value * 100:.{precision}f}%"
    return f"{value:.{precision}f}"


# ============ 核心计算类 ============

@dataclass
class PeriodMetrics:
    """单期财务指标"""
    period: str
    revenue: float | None = None
    revenue_growth_yoy: float | None = None
    net_income: float | None = None
    net_income_growth_yoy: float | None = None
    eps: float | None = None
    eps_growth_yoy: float | None = None
    gross_margin: float | None = None
    operating_margin: float | None = None
    net_margin: float | None = None
    roe: float | None = None
    roa: float | None = None
    asset_liability_ratio: float | None = None
    debt_to_equity: float | None = None
    current_ratio: float | None = None
    quick_ratio: float | None = None
    ocf_to_net_income: float | None = None
    free_cash_flow: float | None = None
    ebit_margin: float | None = None
    ebitda_margin: float | None = None
    
    def to_dict(self) -> dict:
        return {
            "period": self.period,
            "revenue": self.revenue,
            "revenue_growth_yoy": self.revenue_growth_yoy,
            "net_income": self.net_income,
            "net_income_growth_yoy": self.net_income_growth_yoy,
            "eps": self.eps,
            "eps_growth_yoy": self.eps_growth_yoy,
            "gross_margin": self.gross_margin,
            "operating_margin": self.operating_margin,
            "net_margin": self.net_margin,
            "roe": self.roe,
            "roa": self.roa,
            "asset_liability_ratio": self.asset_liability_ratio,
            "debt_to_equity": self.debt_to_equity,
            "current_ratio": self.current_ratio,
            "quick_ratio": self.quick_ratio,
            "ocf_to_net_income": self.ocf_to_net_income,
            "free_cash_flow": self.free_cash_flow,
            "ebit_margin": self.ebit_margin,
            "ebitda_margin": self.ebitda_margin,
        }


@dataclass
class ValuationMetrics:
    """估值指标"""
    pe: float | None = None
    ps: float | None = None
    pb: float | None = None
    ev_ebit: float | None = None
    ev_ebitda: float | None = None
    dividend_yield: float | None = None
    
    def to_dict(self) -> dict:
        return {
            "pe": self.pe,
            "ps": self.ps,
            "pb": self.pb,
            "ev_ebit": self.ev_ebit,
            "ev_ebitda": self.ev_ebitda,
            "dividend_yield": self.dividend_yield,
        }


@dataclass
class ValuationScenario:
    """估值情景"""
    name: str
    description: str
    target_price: float
    upside_downside: float
    pe_assumption: float
    eps_growth_assumption: float
    probability: str
    key_triggers: list[str]
    confidence: str
    
    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "description": self.description,
            "target_price": self.target_price,
            "upside_downside": self.upside_downside,
            "pe_assumption": self.pe_assumption,
            "eps_growth_assumption": self.eps_growth_assumption,
            "probability": self.probability,
            "key_triggers": self.key_triggers,
            "confidence": self.confidence,
        }


class FinancialAnalyzer:
    """财务分析器"""
    
    def __init__(self, periods_data: list[dict], market_data: dict | None = None):
        """
        初始化
        
        Args:
            periods_data: 多期财务数据列表，每项为一个报告期的原始数据
            market_data: 市场数据（股价、市值等），可选
        """
        self.periods_raw = periods_data
        self.market_data = market_data or {}
        self.period_metrics: list[PeriodMetrics] = []
        self.valuation_metrics: ValuationMetrics | None = None
        self.anomalies: list[dict] = []
        
        # 执行分析
        self._normalize_data()
        self._compute_metrics()
        if market_data:
            self._compute_valuation()
        self._detect_anomalies()
    
    def _normalize_data(self) -> None:
        """标准化原始数据"""
        self.normalized_periods = []
        for row in self.periods_raw:
            item = {}
            for key in FIELD_ALIASES:
                item[key] = pick_value(row, key)
            self.normalized_periods.append(item)
    
    def _compute_metrics(self) -> None:
        """计算各期财务指标"""
        previous = None
        
        for row in self.normalized_periods:
            p = row.get("period", "unknown")
            
            # 提取原始值
            revenue = to_float(row.get("revenue"))
            gross_profit = to_float(row.get("gross_profit"))
            operating_income = to_float(row.get("operating_income"))
            net_income = to_float(row.get("net_income"))
            ebit = to_float(row.get("ebit"))
            ebitda = to_float(row.get("ebitda"))
            ocf = to_float(row.get("operating_cash_flow"))
            capex = to_float(row.get("capital_expenditure"))
            total_assets = to_float(row.get("total_assets"))
            total_equity = to_float(row.get("total_equity"))
            total_debt = to_float(row.get("total_debt"))
            current_assets = to_float(row.get("current_assets"))
            current_liabilities = to_float(row.get("current_liabilities"))
            inventory = to_float(row.get("inventory"))
            shares = to_float(row.get("shares_outstanding"))
            
            # 上期值（用于计算增长率）
            prev_revenue = to_float(previous.get("revenue")) if previous else None
            prev_net_income = to_float(previous.get("net_income")) if previous else None
            prev_shares = to_float(previous.get("shares_outstanding")) if previous else None
            prev_equity = to_float(previous.get("total_equity")) if previous else None
            prev_assets = to_float(previous.get("total_assets")) if previous else None
            
            # 计算指标
            eps = safe_div(net_income, shares)
            prev_eps = safe_div(prev_net_income, prev_shares) if previous else None
            
            capex_outflow = abs(capex) if capex is not None else None
            fcf = ocf - capex_outflow if ocf is not None and capex_outflow is not None else None
            
            avg_equity = average_two(total_equity, prev_equity)
            avg_assets = average_two(total_assets, prev_assets)
            
            metrics = PeriodMetrics(
                period=p,
                revenue=revenue,
                revenue_growth_yoy=yoy_growth(revenue, prev_revenue),
                net_income=net_income,
                net_income_growth_yoy=yoy_growth(net_income, prev_net_income),
                eps=eps,
                eps_growth_yoy=yoy_growth(eps, prev_eps),
                gross_margin=safe_div(gross_profit, revenue),
                operating_margin=safe_div(operating_income, revenue),
                net_margin=safe_div(net_income, revenue),
                roe=safe_div(net_income, avg_equity),
                roa=safe_div(net_income, avg_assets),
                asset_liability_ratio=(
                    (total_assets - total_equity) / total_assets
                    if total_assets and total_equity is not None
                    else None
                ),
                debt_to_equity=safe_div(total_debt, total_equity),
                current_ratio=safe_div(current_assets, current_liabilities),
                quick_ratio=safe_div(
                    current_assets - inventory if current_assets is not None and inventory is not None else None,
                    current_liabilities
                ),
                ocf_to_net_income=safe_div(ocf, net_income),
                free_cash_flow=fcf,
                ebit_margin=safe_div(ebit, revenue),
                ebitda_margin=safe_div(ebitda, revenue),
            )
            
            self.period_metrics.append(metrics)
            previous = row
    
    def _compute_valuation(self) -> None:
        """计算估值指标"""
        if not self.normalized_periods:
            return
        
        latest = self.normalized_periods[-1]
        revenue = to_float(latest.get("revenue"))
        net_income = to_float(latest.get("net_income"))
        total_equity = to_float(latest.get("total_equity"))
        ebit = to_float(latest.get("ebit"))
        ebitda = to_float(latest.get("ebitda"))
        shares = to_float(latest.get("shares_outstanding"))
        
        price = pick_market_value(self.market_data, "price")
        market_cap = pick_market_value(self.market_data, "market_cap")
        ev = pick_market_value(self.market_data, "enterprise_value")
        
        # 计算EPS
        eps = safe_div(net_income, shares)
        
        self.valuation_metrics = ValuationMetrics(
            pe=safe_div(price, eps) if price else safe_div(market_cap, net_income),
            ps=safe_div(market_cap, revenue),
            pb=safe_div(market_cap, total_equity),
            ev_ebit=safe_div(ev, ebit),
            ev_ebitda=safe_div(ev, ebitda),
        )
    
    def _detect_anomalies(self) -> None:
        """检测财务异常"""
        if len(self.period_metrics) < 2:
            return
        
        for i, metrics in enumerate(self.period_metrics):
            # 收入突变 (>30%)
            if metrics.revenue_growth_yoy is not None and abs(metrics.revenue_growth_yoy) > 0.3:
                self.anomalies.append({
                    "period": metrics.period,
                    "type": "收入增速异常",
                    "metric": "revenue_growth_yoy",
                    "value": f"{metrics.revenue_growth_yoy*100:.1f}%",
                    "severity": "high" if abs(metrics.revenue_growth_yoy) > 0.5 else "medium",
                })
            
            # 利润突变 (>50%)
            if metrics.net_income_growth_yoy is not None and abs(metrics.net_income_growth_yoy) > 0.5:
                self.anomalies.append({
                    "period": metrics.period,
                    "type": "利润增速异常",
                    "metric": "net_income_growth_yoy",
                    "value": f"{metrics.net_income_growth_yoy*100:.1f}%",
                    "severity": "high" if abs(metrics.net_income_growth_yoy) > 1.0 else "medium",
                })
            
            # 毛利率与净利率背离
            if i > 0:
                prev = self.period_metrics[i-1]
                if (metrics.gross_margin is not None and prev.gross_margin is not None and
                    metrics.net_margin is not None and prev.net_margin is not None):
                    gm_change = metrics.gross_margin - prev.gross_margin
                    nm_change = metrics.net_margin - prev.net_margin
                    if abs(gm_change) > 0.02 and gm_change * nm_change < 0:  # 方向相反且变化显著
                        self.anomalies.append({
                            "period": metrics.period,
                            "type": "毛利率与净利率背离",
                            "metric": "gross_margin vs net_margin",
                            "value": f"毛利率变化{gm_change*100:.1f}%, 净利率变化{nm_change*100:.1f}%",
                            "severity": "medium",
                        })
            
            # 利润与现金流背离
            if metrics.ocf_to_net_income is not None and metrics.ocf_to_net_income < 0.5:
                self.anomalies.append({
                    "period": metrics.period,
                    "type": "利润含金量低",
                    "metric": "ocf_to_net_income",
                    "value": f"{metrics.ocf_to_net_income:.2f}",
                    "severity": "high" if metrics.ocf_to_net_income < 0 else "medium",
                })
            
            # ROE异常低
            if metrics.roe is not None and metrics.roe < 0.05:
                self.anomalies.append({
                    "period": metrics.period,
                    "type": "ROE偏低",
                    "metric": "roe",
                    "value": f"{metrics.roe*100:.1f}%",
                    "severity": "medium",
                })
    
    def generate_valuation_scenarios(
        self,
        current_price: float,
        assumptions: dict | None = None
    ) -> list[ValuationScenario]:
        """
        生成估值情景推演
        
        Args:
            current_price: 当前股价
            assumptions: 用户自定义假设，可选
            
        Returns:
            Base/Optimistic/Stress 三情景估值
        """
        if not self.period_metrics or not self.valuation_metrics:
            return []
        
        latest = self.period_metrics[-1]
        
        # 获取EPS（TTM或最近年报）
        eps = latest.eps
        if eps is None or eps <= 0:
            return []
        
        # 当前PE
        current_pe = self.valuation_metrics.pe or 20.0
        
        # 使用用户假设或默认值
        base_pe = assumptions.get("base_pe", current_pe) if assumptions else current_pe
        opt_pe = assumptions.get("optimistic_pe", base_pe * 1.2) if assumptions else base_pe * 1.2
        stress_pe = assumptions.get("stress_pe", base_pe * 0.7) if assumptions else base_pe * 0.7
        
        base_growth = assumptions.get("base_growth", 0.15) if assumptions else 0.15
        opt_growth = assumptions.get("optimistic_growth", base_growth + 0.10) if assumptions else base_growth + 0.10
        stress_growth = assumptions.get("stress_growth", base_growth - 0.10) if assumptions else max(base_growth - 0.10, -0.20)
        
        scenarios = []
        
        # Base情景（基准）
        base_eps = eps * (1 + base_growth)
        base_target = base_eps * base_pe
        scenarios.append(ValuationScenario(
            name="Base（基准情景）",
            description="基于历史平均增速和行业合理PE的中性假设",
            target_price=round(base_target, 2),
            upside_downside=round((base_target - current_price) / current_price * 100, 1),
            pe_assumption=round(base_pe, 1),
            eps_growth_assumption=round(base_growth * 100, 1),
            probability="50%",
            key_triggers=[
                "业绩保持历史平均增速",
                "估值维持在当前中枢水平",
                "行业竞争格局稳定"
            ],
            confidence="中"
        ))
        
        # Optimistic情景（乐观）
        opt_eps = eps * (1 + opt_growth)
        opt_target = opt_eps * opt_pe
        scenarios.append(ValuationScenario(
            name="Optimistic（乐观情景）",
            description="受益于行业景气上行和公司竞争优势扩大",
            target_price=round(opt_target, 2),
            upside_downside=round((opt_target - current_price) / current_price * 100, 1),
            pe_assumption=round(opt_pe, 1),
            eps_growth_assumption=round(opt_growth * 100, 1),
            probability="25%",
            key_triggers=[
                "新产品/新业务超预期放量",
                "行业政策利好落地",
                "市占率显著提升"
            ],
            confidence="低"
        ))
        
        # Stress情景（压力）
        stress_eps = eps * (1 + stress_growth)
        stress_target = stress_eps * stress_pe
        scenarios.append(ValuationScenario(
            name="Stress（压力情景）",
            description="面临行业下行周期或公司经营挑战",
            target_price=round(stress_target, 2),
            upside_downside=round((stress_target - current_price) / current_price * 100, 1),
            pe_assumption=round(stress_pe, 1),
            eps_growth_assumption=round(stress_growth * 100, 1),
            probability="25%",
            key_triggers=[
                "行业竞争加剧导致毛利率下滑",
                "宏观经济下行影响需求",
                "原材料成本大幅上升"
            ],
            confidence="中"
        ))
        
        return scenarios
    
    def get_summary(self) -> dict:
        """获取分析摘要"""
        return {
            "period_count": len(self.period_metrics),
            "latest_period": self.period_metrics[-1].period if self.period_metrics else None,
            "valuation": self.valuation_metrics.to_dict() if self.valuation_metrics else None,
            "anomaly_count": len(self.anomalies),
            "anomalies": self.anomalies,
        }
    
    def to_dict(self) -> dict:
        """导出完整分析结果"""
        return {
            "period_metrics": [m.to_dict() for m in self.period_metrics],
            "valuation_metrics": self.valuation_metrics.to_dict() if self.valuation_metrics else None,
            "anomalies": self.anomalies,
        }


def analyze_financial_data(
    periods_data: list[dict],
    market_data: dict | None = None,
    current_price: float | None = None
) -> dict:
    """
    便捷的财务分析入口函数
    
    Args:
        periods_data: 多期财务数据
        market_data: 市场数据（用于估值）
        current_price: 当前股价（用于情景推演）
        
    Returns:
        完整分析结果字典
    """
    analyzer = FinancialAnalyzer(periods_data, market_data)
    result = analyzer.to_dict()
    
    if current_price:
        result["valuation_scenarios"] = [
            s.to_dict() for s in analyzer.generate_valuation_scenarios(current_price)
        ]
    
    return result


if __name__ == "__main__":
    pass
