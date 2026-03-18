---
name: stock-ai-analyzer
description: 股票AI分析助手，支持基础分析和增强分析。基础模式：输入"股票名称 基本面/技术面"进行标准分析。增强模式：输入"股票名称，基本面，重点查询分析xxx"可在基础分析上追加深度专题分析。⚠️ 重要提示：1) 需要配置 TUSHARE_TOKEN 才能获取股票数据；2) 需要配置 AI 模型才能进行分析（支持 OpenAI 兼容接口、自定义 LLM 端点或 OpenClaw 环境自动处理）。
trigger_patterns:
  - "{stock_name} 基本面"
  - "{stock_name} 技术面"
  - "分析 {stock_name} 基本面"
  - "分析 {stock_name} 技术面"
  - "{stock_name}，基本面，重点查询分析{extra}"
---

# 股票AI分析助手

支持基础分析和增强分析两种模式。兼容 OpenClaw 及多种 AI 模型环境。

## ⚠️ 重要依赖声明

### 必需配置

**TUSHARE_TOKEN**（必需）
- 用途：获取股票数据
- 获取：https://tushare.pro
- 配置：`export TUSHARE_TOKEN=your_token`

**AI 模型**（必需，以下方式任选其一）

1. **OpenClaw 环境**（推荐）
   - 无需额外配置，OpenClaw 会自动处理 AI 调用
   
2. **OpenAI 兼容接口**
   ```bash
   export OPENAI_API_KEY=your_key
   export OPENAI_BASE_URL=https://api.openai.com/v1  # 可选，默认 OpenAI
   ```
   
3. **自定义 LLM 接口**
   ```bash
   export LLM_API_KEY=your_key
   export LLM_API_BASE=https://your-endpoint/v1
   export LLM_MODEL=your-model-name
   ```
   
4. **HTTP 端点**
   ```bash
   export OPENCLAW_MODEL_ENDPOINT=http://localhost:8000/generate
   ```

## ⚠️ 数据安全说明

- 股票数据和财务信息会发送到配置的 AI 模型进行处理
- 请确保您的 AI 服务端点可信
- 敏感股票数据请谨慎使用

## 使用模式

### 基础分析
```
股票名称 基本面
股票名称 技术面
```

### 增强分析（基础+深度专题）
```
股票名称，基本面，重点查询分析[专题]
```

示例：
- "东威科技，基本面，重点查询分析业务和AI pcb生产的关联性"

## 分析内容

### 基础模块
- 公司概况
- 财务质量分析
- 估值分析（三情景估值）
- 股东与管理层

### 增强专题
- 业务关联性分析
- 客户结构分析
- 竞争优势分析

## 文件结构

```
scripts/
├── stock_analyzer.py       # 基础分析
├── enhanced_analyzer.py    # 增强分析
├── data_fetcher.py         # 数据获取
├── financial_ratios.py     # 财务计算
└── ai_client.py            # AI 模型客户端（多环境兼容）
```

## 依赖

- Python 3.8+
- tushare
- pandas
- numpy

## 免责声明

以上分析基于公开历史数据，不构成投资建议。
