---
name: financial-ai-agent
description: "查询金融行情数据（股票、黄金、原油等）。当用户提到查询行情、价格、指数、股票时使用。例如：'查询纳斯达克'、'现在金价多少'、'标普最近一周表现'、'设置我的key'、'替换key'。"
metadata: {"openclaw": {"emoji": "📈", "requires": {"bins": ["node"]}}}
---

# Financial AI Agent

查询金融行情数据（股票、指数、黄金、原油等）。

## 功能

- 📊 查询实时行情（价格、涨跌幅）
- 📈 查询历史走势（最近n天）
- 🔑 用户可自定义 API Key

## 对话示例

| 用户说 | 执行命令 |
|--------|---------|
| 查询纳斯达克 | `faa.cjs 纳斯达克` |
| 查下黄金价格 | `faa.cjs 黄金` |
| 标普最近一周表现 | `faa.cjs 标普 --history` |
| 纳斯达克最近30天 | `faa.cjs 纳斯达克 --history --days 30` |
| 纳斯达克5分钟走势 | `faa.cjs 纳斯达克 --5min` |
| 最近20条5分钟数据 | `faa.cjs 纳斯达克 --5min --limit 20` |

## 设置 API Key

### 方式1：直接说（推荐）

用户可以直接说：
- "我的key是 `xxx`" → 自动保存为默认key
- "替换key为 `xxx`" → 替换已有key

### 方式2：命令行

```bash
# 保存 key
faa.cjs --set-key 你的key

# 查看当前 key
faa.cjs --show-key
```

### 方式3：配置文件

key 保存在用户目录：`~/.faa-key`

### 关于 Key

- **内置体验key**：`5v9Zhv8RSqPg6nk3ZlCvyK0weY9FKdTk`（有有效期限制）
- **自定义key**：可到网站 `api.financialagent.cc` 注册申请
- 替换key后，下次查询自动使用新key

## 支持的行情

| 中文 | 英文 | Symbol |
|------|------|--------|
| 纳斯达克 | Nasdaq | NDX |
| 道琼斯 | Dow Jones | DJIA |
| 标普500 | S&P 500 | SPX |
| 黄金 | Gold | XAU |
| 白银 | Silver | XAG |
| 原油 | Oil | CL |
| 上证指数 | Shanghai | SH000001 |
| 深证成指 | Shenzhen | SZ399001 |
| 创业板指 | ChiNext | SZ399006 |

## 执行命令

```
~/.npm-global/lib/node_modules/openclaw/skills/financial-ai-agent/faa.cjs <标的> [选项]
```

## 技术说明

- 脚本位置：`~/.npm-global/lib/node_modules/openclaw/skills/financial-ai-agent/faa.cjs`
- API 地址：`https://api.financialagent.cc`
- Key 保存位置：`~/.faa-key`

## 联系我们

有问题或建议请联系：pesome@gmail.com
