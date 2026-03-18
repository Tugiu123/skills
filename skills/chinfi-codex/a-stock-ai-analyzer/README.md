# Stock AI Analyzer 技能包

股票AI分析助手，支持基础分析和增强分析两种模式。兼容 OpenClaw 及多种 AI 模型环境。

## 功能特性

- **基础分析**：公司概况、财务指标、估值推演、股东结构
- **技术面分析**：K线形态、均线系统、MACD/RSI/KDJ指标
- **增强分析**：基础分析 + 深度专题分析
- **多环境兼容**：支持 OpenClaw、OpenAI、自定义 LLM 接口

## 必需配置

### TUSHARE_TOKEN（必需）

```bash
export TUSHARE_TOKEN=your_token_here
```

获取地址：https://tushare.pro

### AI 模型（任选其一）

**方式1：OpenClaw 环境（推荐）**
```bash
# 无需配置，OpenClaw 自动处理
```

**方式2：OpenAI 兼容接口**
```bash
export OPENAI_API_KEY=your_api_key
export OPENAI_BASE_URL=https://api.openai.com/v1  # 可选
```

**方式3：自定义 LLM**
```bash
export LLM_API_KEY=your_key
export LLM_API_BASE=https://your-api-endpoint/v1
export LLM_MODEL=your-model-name
```

**方式4：HTTP 端点**
```bash
export OPENCLAW_MODEL_ENDPOINT=http://localhost:8000/generate
```

## 使用方法

### 基础分析

```bash
python scripts/stock_analyzer.py "<股票名称>" "<基本面|技术面>"
```

### 增强分析

```bash
python scripts/enhanced_analyzer.py "股票名称，基本面，重点查询分析xxx"
```

示例：
- "东威科技，基本面，重点查询分析业务和AI pcb生产的关联性"

## 文件结构

```
scripts/
├── stock_analyzer.py       # 基础分析
├── enhanced_analyzer.py    # 增强分析
├── data_fetcher.py         # 数据获取
├── financial_ratios.py     # 财务计算
└── ai_client.py            # AI 客户端（多环境兼容）
```

## 依赖

- Python 3.8+
- tushare
- pandas
- numpy

## 免责声明

以上分析基于公开历史数据，不构成投资建议。
