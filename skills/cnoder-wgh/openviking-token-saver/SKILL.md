---
name: openviking-token-saver
description: "Help OpenClaw users reduce LLM token costs by integrating OpenViking as a hierarchical context database. Use when: user wants to save tokens, reduce API costs, set up OpenViking, manage long-term memory for coding or document tasks, or optimize context loading."
metadata: { "openclaw": { "emoji": "⚡", "requires": { "bins": ["python3", "pip3"] } } }
---

# OpenViking Token Saver

通过集成 [OpenViking](https://github.com/volcengine/OpenViking) 为 OpenClaw 提供分层上下文管理，大幅降低 Token 消耗。

## 效果数据（LoCoMo10 基准测试）

| 配置 | 任务完成率 | Token 消耗 |
|------|-----------|-----------|
| 仅 OpenClaw | 35.65% | 24.6M |
| OpenClaw + OpenViking | **52.08% (+49%)** | **4.3M (-83%)** |

## 核心原理：L0/L1/L2 分层加载

OpenViking 将上下文分为三层，按需加载，避免一次性塞入大量内容：

- **L0 摘要**（~100 tokens）：极简摘要，初步判断相关性
- **L1 概览**（~2k tokens）：结构化概览，深入了解内容
- **L2 完整内容**：仅在真正需要时才加载全文

## 使用场景

### 1. 首次安装配置
当用户说"安装 OpenViking"、"配置 token 节省"、"设置 OpenViking"时：
→ 参考 `{baseDir}/SETUP.md` 引导安装

### 2. 写代码场景
当用户说"把代码库加入 OpenViking"、"代码搜索"、"分析项目结构"时：
→ 参考 `{baseDir}/CODING.md` 执行操作

### 3. 文档处理场景
当用户说"把文档加入知识库"、"语义搜索文档"、"总结文档"时：
→ 参考 `{baseDir}/DOCS.md` 执行操作

## 快速健康检查

```bash
# 检查 OpenViking 是否已安装
python3 -c "import openviking; print('OpenViking 已安装 ✓')" 2>/dev/null || echo "OpenViking 未安装，请先运行安装向导"

# 检查服务是否运行
curl -s http://localhost:1933/health 2>/dev/null | python3 -m json.tool || echo "OpenViking 服务未运行"

# 查看当前内存使用
python3 -c "
from openviking import OpenViking
ov = OpenViking()
result = ov.ls('viking://')
print(result)
" 2>/dev/null
```

## 常用命令速查

```bash
# 启动服务
openviking-server &

# 添加代码库
python3 -c "from openviking import OpenViking; OpenViking().add_resource('/path/to/repo')"

# 语义搜索
python3 -c "from openviking import OpenViking; print(OpenViking().find('your query'))"

# 查看存储的内容
ovcli ls viking://resources/
ovcli ls viking://memory/
```
