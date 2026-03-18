# 文档处理场景：Token 节省技巧

## 核心思路

传统方式：把整篇文档塞进上下文 → 一篇 PDF 就消耗数千 token
OpenViking 方式：索引文档 → 语义搜索定位段落 → 只读相关片段

## 操作一：将文档加入知识库

```python
from openviking import OpenViking

ov = OpenViking()

# 添加单个文档（支持 PDF、Word、Markdown、txt 等）
ov.add_resource("/Users/wuguanhua/Documents/项目计划书.pdf")

# 添加整个文档目录
ov.add_resource("/Users/wuguanhua/Documents/")

# 添加网页/在线文档
ov.add_resource("https://docs.example.com/api-reference")

# 等待处理
ov.wait_processed()
print("文档已索引 ✓")
```

CLI 方式：
```bash
ovcli add-resource ~/Documents/项目计划书.pdf
ovcli add-resource ~/Documents/  # 整个目录
```

## 操作二：语义搜索文档内容

```python
from openviking import OpenViking

ov = OpenViking()

# 快速语义搜索（不需要完整阅读）
results = ov.find("项目预算和时间安排")
for r in results:
    print(r)

# 带对话上下文的搜索（更精准）
session = ov.session()
session.add(role="user", content="我在准备 Q2 项目汇报")
results = session.search("项目进度和风险评估")
print(results)
```

## 操作三：文档对比（结合 doc-diff skill）

```python
from openviking import OpenViking

ov = OpenViking()

# 分别获取两个版本的 L1 概览（不读全文）
v1_overview = ov.overview("viking://resources/项目计划书_v1.pdf")
v2_overview = ov.overview("viking://resources/项目计划书_v2.pdf")

print("V1 概览:", v1_overview)
print("V2 概览:", v2_overview)
# 再用 diff 工具对比差异，避免把两个完整文档都塞进 token
```

## 操作四：查看文档结构

```bash
# 查看知识库中的文档列表
ovcli ls viking://resources/

# 查看文档目录树
ovcli tree viking://resources/Documents/ --depth 2

# 只读摘要（判断是否相关）
ovcli abstract viking://resources/项目计划书.pdf
```

## 操作五：记录文档处理记忆

```python
from openviking import OpenViking

ov = OpenViking()
session = ov.session()

session.add(role="user", content="帮我总结《2026年战略规划》的核心要点")
session.add(role="assistant", content="核心要点：1. 扩大海外市场 2. AI 产品化 3. 降本增效")

# 提交后，下次问相关问题会自动召回
session.commit()
```

## 省 Token 最佳实践

### 文档处理流程

```
Step 1: 添加文档到 OpenViking（一次性）
         ↓
Step 2: 用 find() 语义搜索定位相关段落（消耗极少 token）
         ↓
Step 3: 读取 L0 摘要确认相关性（~100 tokens）
         ↓
Step 4: 如需深入，读 L1 概览（~2k tokens）
         ↓
Step 5: 只在必要时读完整段落（L2，按需加载）
```

### Token 消耗对比

| 方式 | 处理一篇 10 页 PDF | 处理 100 篇文档 |
|------|-------------------|-----------------|
| 传统（全文塞入）| ~8,000 tokens | ~800,000 tokens |
| OpenViking L0 搜索 | ~200 tokens | ~500 tokens |
| OpenViking L1 概览 | ~2,000 tokens | ~2,000 tokens |

### ✅ 推荐做法

```
# 先搜索定位
"搜索文档中关于预算的内容"

# 再按需深入
"给我看预算章节的详细内容"
```

### ❌ 避免的做法

```
# 不要直接上传整个文档让 AI 阅读
# 不要每次对话都重新添加相同文档
# 不要用 cat 读大文件塞进上下文
```

## 支持的文档格式

| 格式 | 支持 |
|------|------|
| PDF | ✅ |
| Word (.docx) | ✅ |
| Markdown (.md) | ✅ |
| 纯文本 (.txt) | ✅ |
| 网页 URL | ✅ |
| GitHub 仓库 | ✅ |
| 图片（含 VLM 时）| ✅ |
