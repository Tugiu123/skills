"""
股票数据获取模块
使用 Tushare Pro API 获取股票数据
"""

import os
import sys
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, List

import pandas as pd
import numpy as np

# 尝试导入tushare
try:
    import tushare as ts
except ImportError:
    print("错误：请先安装tushare: pip install tushare")
    sys.exit(1)


def get_tushare_token() -> str:
    """获取Tushare Token，优先级：环境变量 > 当前目录.env文件"""
    # 1. 尝试从环境变量获取
    token = os.environ.get("TUSHARE_TOKEN", "").strip()
    if token:
        return token
    
    # 2. 仅从当前工作目录的 .env 文件获取（安全限制：不搜索上级目录或用户目录）
    try:
        env_path = os.path.join(os.getcwd(), ".env")
        if os.path.exists(env_path):
            with open(env_path, "r", encoding="utf-8") as f:
                for line in f:
                    s = line.strip()
                    if not s or s.startswith("#") or "=" not in s:
                        continue
                    k, v = s.split("=", 1)
                    if k.strip() == "TUSHARE_TOKEN":
                        token = v.strip().strip('"').strip("'")
                        if token:
                            return token
    except Exception:
        pass
    
    return ""


def get_tushare_pro():
    """获取Tushare Pro API客户端"""
    token = get_tushare_token()
    if not token:
        raise RuntimeError("缺少TUSHARE_TOKEN: 请设置环境变量或在.env文件中配置")
    return ts.pro_api(token)


class StockDataFetcher:
    """股票数据获取器 - 对齐 10-公司投研专家.py 的实现"""
    
    def __init__(self):
        self.pro = get_tushare_pro()
        self._stock_list_cache: Optional[pd.DataFrame] = None
        self._cache_time: Optional[datetime] = None
    
    def get_all_stocks(self) -> pd.DataFrame:
        """获取所有上市股票列表（带缓存）"""
        if (self._stock_list_cache is not None and 
            self._cache_time is not None and
            (datetime.now() - self._cache_time).days < 1):
            return self._stock_list_cache
        
        try:
            df = self.pro.stock_basic(
                list_status="L",
                fields="ts_code,name,area,industry,market,list_date"
            )
            if df is None or df.empty:
                return pd.DataFrame()
            
            df["code6"] = df["ts_code"].str.split(".").str[0]
            df["board"] = df["code6"].apply(self._classify_board)
            
            self._stock_list_cache = df
            self._cache_time = datetime.now()
            return df
        except Exception as e:
            print(f"获取股票列表失败: {e}")
            return pd.DataFrame()
    
    def _classify_board(self, code6: str) -> str:
        """根据6位代码判断板块"""
        if code6.startswith(("688", "689")):
            return "科创板"
        if code6.startswith(("300", "301")):
            return "创业板"
        if code6.startswith(("8", "4")):
            return "北交所"
        if code6.startswith(("0", "3", "6")):
            return "主板"
        return "其他"
    
    def search_stock(self, query: str) -> Optional[Dict[str, Any]]:
        """搜索股票，返回第一个匹配结果"""
        query = query.strip()
        all_stocks = self.get_all_stocks()
        
        if all_stocks.empty:
            return None
        
        # 精确匹配6位代码
        if query.isdigit() and len(query) == 6:
            result = all_stocks[all_stocks["code6"] == query]
            if not result.empty:
                return result.iloc[0].to_dict()
        
        # 匹配ts_code格式
        if "." in query.upper():
            result = all_stocks[all_stocks["ts_code"] == query.upper()]
            if not result.empty:
                return result.iloc[0].to_dict()
        
        # 模糊匹配名称
        result = all_stocks[all_stocks["name"].str.contains(query, case=False, na=False)]
        if not result.empty:
            return result.iloc[0].to_dict()
        
        # 模糊匹配代码
        result = all_stocks[all_stocks["code6"].str.contains(query, na=False)]
        if not result.empty:
            return result.iloc[0].to_dict()
        
        return None
    
    # =========================================================================
    # 以下方法完全对齐 10-公司投研专家.py 的实现
    # =========================================================================
    
    def get_stock_basic_info(self, ts_code: str) -> Optional[Dict[str, Any]]:
        """获取上市公司基本信息 - 对齐 10-公司投研专家.py"""
        try:
            df = self.pro.stock_company(ts_code=ts_code)
            if df is not None and not df.empty:
                return df.iloc[0].to_dict()
            return None
        except Exception as e:
            print(f"获取公司基本信息失败: {e}")
            return None
    
    def get_financial_indicators(self, ts_code: str, limit: int = 12) -> Optional[pd.DataFrame]:
        """获取财务指标数据 - 对齐 10-公司投研专家.py"""
        try:
            df = self.pro.fina_indicator(ts_code=ts_code, limit=limit)
            if df is not None and not df.empty:
                df = df.sort_values("end_date", ascending=False)
                return df
            return None
        except Exception as e:
            print(f"获取财务指标失败: {e}")
            return None
    
    def get_main_business(self, ts_code: str, bz_type: str = "P", limit: int = 20) -> Optional[pd.DataFrame]:
        """获取主营业务构成 - 对齐 10-公司投研专家.py"""
        try:
            df = self.pro.fina_mainbz(ts_code=ts_code, type=bz_type)
            if df is not None and not df.empty:
                df = df.sort_values("end_date", ascending=False)
                if len(df) > limit * 5:
                    df = df.head(limit * 5)
                return df
            return None
        except Exception as e:
            print(f"获取主营构成失败: {e}")
            return None
    
    def get_top10_holders(self, ts_code: str, limit: int = 4) -> Optional[pd.DataFrame]:
        """获取前十大股东 - 对齐 10-公司投研专家.py"""
        try:
            df = self.pro.top10_holders(ts_code=ts_code)
            if df is not None and not df.empty:
                df = df.sort_values(["end_date", "hold_ratio"], ascending=[False, False])
                latest_dates = df["end_date"].unique()[:limit]
                df = df[df["end_date"].isin(latest_dates)]
                return df
            return None
        except Exception as e:
            print(f"获取十大股东失败: {e}")
            return None
    
    def get_managers(self, ts_code: str) -> Optional[pd.DataFrame]:
        """获取管理层信息 - 对齐 10-公司投研专家.py"""
        try:
            df = self.pro.stk_managers(ts_code=ts_code)
            if df is not None and not df.empty:
                latest_ann_date = df["ann_date"].max()
                df = df[df["ann_date"] == latest_ann_date]
                return df
            return None
        except Exception as e:
            print(f"获取管理层信息失败: {e}")
            return None
    
    def get_manager_rewards(self, ts_code: str) -> Optional[pd.DataFrame]:
        """获取管理层薪酬和持股 - 对齐 10-公司投研专家.py"""
        try:
            df = self.pro.stk_rewards(ts_code=ts_code)
            if df is not None and not df.empty:
                latest_end_date = df["end_date"].max()
                df = df[df["end_date"] == latest_end_date]
                return df
            return None
        except Exception as e:
            print(f"获取管理层薪酬失败: {e}")
            return None
    
    def get_share_float(self, ts_code: str, limit: int = 50) -> Optional[pd.DataFrame]:
        """获取限售股解禁数据 - 对齐 10-公司投研专家.py"""
        try:
            start_date = datetime.now().strftime("%Y%m%d")
            end_date = (datetime.now() + timedelta(days=365*3)).strftime("%Y%m%d")
            df = self.pro.share_float(ts_code=ts_code, start_date=start_date, end_date=end_date)
            if df is not None and not df.empty:
                df = df.sort_values("float_date")
                if len(df) > limit:
                    df = df.head(limit)
                return df
            return None
        except Exception as e:
            print(f"获取限售解禁失败: {e}")
            return None
    
    def get_block_trade(self, ts_code: str, limit: int = 100) -> Optional[pd.DataFrame]:
        """获取大宗交易数据 - 对齐 10-公司投研专家.py"""
        try:
            end_date = datetime.now().strftime("%Y%m%d")
            start_date = (datetime.now() - timedelta(days=90)).strftime("%Y%m%d")
            df = self.pro.block_trade(ts_code=ts_code, start_date=start_date, end_date=end_date)
            if df is not None and not df.empty:
                df = df.sort_values("trade_date", ascending=False)
                if len(df) > limit:
                    df = df.head(limit)
                return df
            return None
        except Exception as e:
            print(f"获取大宗交易失败: {e}")
            return None
    
    def get_stk_holdertrade(self, ts_code: str, limit: int = 100) -> Optional[pd.DataFrame]:
        """获取股东增减持数据 - 对齐 10-公司投研专家.py"""
        try:
            end_date = datetime.now().strftime("%Y%m%d")
            start_date = (datetime.now() - timedelta(days=365)).strftime("%Y%m%d")
            df = self.pro.stk_holdertrade(ts_code=ts_code, start_date=start_date, end_date=end_date)
            if df is not None and not df.empty:
                df = df.sort_values("ann_date", ascending=False)
                if len(df) > limit:
                    df = df.head(limit)
                return df
            return None
        except Exception as e:
            print(f"获取增减持失败: {e}")
            return None
    
    def get_stk_holdernumber(self, ts_code: str, limit: int = 50) -> Optional[pd.DataFrame]:
        """获取股东人数数据 - 对齐 10-公司投研专家.py"""
        try:
            df = self.pro.stk_holdernumber(ts_code=ts_code)
            if df is not None and not df.empty:
                df = df.sort_values("end_date", ascending=False)
                if len(df) > limit:
                    df = df.head(limit)
                return df
            return None
        except Exception as e:
            print(f"获取股东人数失败: {e}")
            return None
    
    # =========================================================================
    # 价格数据（用于技术面和估值）
    # =========================================================================
    
    def get_daily_prices(self, ts_code: str, count: int = 60) -> Optional[pd.DataFrame]:
        """获取日线数据"""
        try:
            end_date = datetime.now().strftime("%Y%m%d")
            start_date = (datetime.now() - timedelta(days=count * 2)).strftime("%Y%m%d")
            
            df = self.pro.daily(ts_code=ts_code, start_date=start_date, end_date=end_date)
            if df is not None and not df.empty:
                df = df.sort_values("trade_date")
                df["trade_date"] = pd.to_datetime(df["trade_date"])
                df.set_index("trade_date", inplace=True)
                df = df.tail(count)
                return df
            return None
        except Exception as e:
            print(f"获取日线数据失败: {e}")
            return None
    
    def get_current_price(self, ts_code: str) -> Optional[float]:
        """获取最新股价"""
        try:
            df = self.get_daily_prices(ts_code, count=1)
            if df is not None and not df.empty:
                return float(df.iloc[-1]["close"])
            
            df = self.pro.daily(ts_code=ts_code, limit=1)
            if df is not None and not df.empty:
                return float(df.iloc[0]["close"])
            return None
        except Exception as e:
            print(f"获取当前股价失败: {e}")
            return None
    
    def get_market_data(self, ts_code: str) -> Dict[str, Any]:
        """获取市场数据（用于估值计算）"""
        try:
            price = self.get_current_price(ts_code)
            
            # 获取总股本计算市值
            stock_info = self.pro.stock_basic(ts_code=ts_code, fields="ts_code,total_share")
            market_cap = None
            total_shares = None
            if stock_info is not None and not stock_info.empty:
                total_shares = stock_info.iloc[0].get("total_share", 0)
                if price and total_shares:
                    market_cap = price * total_shares
            
            return {
                "price": price,
                "market_cap": market_cap,
                "total_shares": total_shares,
            }
        except Exception as e:
            print(f"获取市场数据失败: {e}")
            return {}


def convert_to_ts_code(code: str) -> str:
    """将多种格式转换为ts_code格式"""
    if code is None or not code.strip():
        raise ValueError("股票代码不能为空")
    
    code = str(code).strip()
    upper_code = code.upper()
    
    # 已经是ts_code格式
    if "." in upper_code:
        prefix, suffix = upper_code.split(".", 1)
        suffix = suffix.replace("SS", "SH")
        if suffix in ("SH", "SZ", "BJ"):
            return f"{prefix}.{suffix}"
    
    # 带前缀格式
    if upper_code.startswith(("SZ", "SH", "BJ")) and len(upper_code) >= 8:
        body = upper_code[2:]
        suffix = upper_code[:2]
        return f"{body}.{suffix}"
    
    # 纯数字格式
    if len(code) == 6 and code.isdigit():
        if code.startswith(("0", "3")):
            return f"{code}.SZ"
        elif code.startswith(("6", "9")):
            return f"{code}.SH"
        elif code.startswith("8"):
            return f"{code}.BJ"
    
    return upper_code


if __name__ == "__main__":
    pass
