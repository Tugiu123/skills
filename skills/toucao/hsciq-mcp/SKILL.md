---
name: hsciq-mcp
description: HS Code Lookup for Chinese Products. Query customs codes, tariff rates, declaration elements, and regulatory requirements via HSCIQ MCP API.
license: MIT
tags:
  - HS Code Lookup for Chinese Products
  - Tariff Classification
  - Customs
  - Trade
  - China
  - MCP
env:
  HSCIQ_API_KEY:
    description: "HSCIQ API key for accessing the customs code lookup service"
    required: true
  HSCIQ_BASE_URL:
    description: "HSCIQ API base URL (default: https://www.hsciq.com)"
    required: false
    default: "https://www.hsciq.com"
credentials:
  - name: HSCIQ API Key
    description: "Free API key from https://www.hsciq.com"
    required: true
    url: https://www.hsciq.com
---

# ⚠️ 使用前必读：需要 API 密钥

**本技能需要 HSCIQ API 密钥才能正常工作。**

## 获取 API 密钥

1. 访问 [https://www.hsciq.com](https://www.hsciq.com)
2. 注册账号并登录
3. 在控制台申请 API 密钥
4. 将密钥配置到本地（见下方"配置"章节）

**没有 API 密钥将无法查询海关编码。**

---



# HSCIQ MCP - 海关编码查询服务

专业的中国商品海关编码查询与归类服务，基于 HSCIQ MCP API。

## 功能

- **search_code** - 按关键词搜索海关编码（支持中国/日本/美国）
- **get_code_detail** - 获取海关编码详情（税率、申报要素、监管条件等）
- **search_instance** - 按商品名称检索归类实例
- **search_unified** - 统一搜索（CIQ 项目/危化品/港口信息）

## 触发条件

用户提到以下关键词时自动触发：
- "海关编码"、"HS 编码"、"税号"、"商品编码"
- "查询税率"、"申报要素"、"监管条件"
- "CIQ"、"危化品"、"港口代码"
- "归类实例"、"商品归类"

## 配置

配置文件位于 `~/.openclaw/workspace/hsciq-mcp-config.json`：
```json
{
  "baseUrl": "https://www.hsciq.com",
  "apiKey": "your_api_key",
  "authHeader": "X-API-Key"
}
```

**注意**：API Key 也可以通过环境变量设置：
```bash
export HSCIQ_API_KEY=your_api_key
export HSCIQ_BASE_URL=https://www.hsciq.com
```

## 命令

```bash
# 搜索海关编码
node ~/.openclaw/skills/hsciq-mcp/hsciq-client.js search-code --keywords "塑料软管" --country CN

# 获取编码详情
node ~/.openclaw/skills/hsciq-mcp/hsciq-client.js get-detail --code "3926909090" --country CN

# 搜索归类实例
node ~/.openclaw/skills/hsciq-mcp/hsciq-client.js search-instance --keywords "电子产品" --country CN

# 统一搜索（CIQ/危化品/港口）
node ~/.openclaw/skills/hsciq-mcp/hsciq-client.js search-unified --keywords "食品" --type ciq
```

## 使用示例

### 示例 1: 查询商品的海关编码
```
用户：帮我查一下"塑料软管"的海关编码
→ 调用 search_code，返回编码列表和税率信息
```

### 示例 2: 获取编码详情
```
用户：3926909090 这个编码的税率是多少
→ 调用 get_code_detail，返回完整税率、申报要素、监管条件
```

### 示例 3: 搜索归类实例
```
用户：看看别人是怎么归类"蓝牙耳机"的
→ 调用 search_instance，返回历史归类案例
```

## API 端点说明

所有工具调用统一使用以下端点：

| 端点 | 说明 |
|------|------|
| `POST https://www.hsciq.com/mcp/tools/list` | 列出可用工具 |
| `POST https://www.hsciq.com/mcp/tools/call` | 调用任意工具（通过 `toolName` 参数区分） |

**调用格式示例**：
```json
{
  "toolName": "search_code",
  "arguments": {
    "keywords": "塑料软管",
    "country": "CN",
    "pageIndex": 1,
    "pageSize": 10
  }
}
```

## API 文档

完整 API 说明：https://www.hsciq.com/MCP/Docs

## Python 客户端

也可以使用 Python 脚本直接调用：

```bash
# 搜索海关编码
python3 ~/.openclaw/skills/hsciq-mcp/hsciq_client.py search-code --keywords "塑料软管" --country CN

# 获取编码详情
python3 ~/.openclaw/skills/hsciq-mcp/hsciq_client.py get-detail --code "3926909090"

# 搜索归类实例
python3 ~/.openclaw/skills/hsciq-mcp/hsciq_client.py search-instance --keywords "蓝牙耳机"

# 统一搜索
python3 ~/.openclaw/skills/hsciq-mcp/hsciq_client.py search-unified --keywords "食品" --type ciq

# 列出可用工具
python3 ~/.openclaw/skills/hsciq-mcp/hsciq_client.py list-tools

# JSON 输出（便于程序处理）
python3 ~/.openclaw/skills/hsciq-mcp/hsciq_client.py search-code --keywords "软管" --json
```

### Python 代码集成

```python
from hsciq_client import HSCIQClient

client = HSCIQClient()

# 搜索编码
result = client.search_code("塑料软管", country="CN")
print(result)

# 获取详情
detail = client.get_code_detail("3926909090")
print(detail)
```
