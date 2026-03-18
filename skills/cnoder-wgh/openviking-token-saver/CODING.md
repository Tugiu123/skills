# 写代码场景：Token 节省技巧

## 核心思路

传统方式：把整个代码库塞进上下文 → token 爆炸
OpenViking 方式：L0 摘要先定位 → L1 概览理解结构 → L2 只读需要的文件

## 操作一：将代码库加入 OpenViking

```python
from openviking import OpenViking

ov = OpenViking()

# 添加本地代码库（会自动提取 AST 结构作为 L0/L1）
ov.add_resource("/Users/wuguanhua/Documents/my-project")

# 等待处理完成
ov.wait_processed()
print("代码库已索引 ✓")
```

也可以用 CLI：
```bash
ovcli add-resource /path/to/your/project
```

添加 GitHub 仓库：
```python
ov.add_resource("https://github.com/username/repo")
```

## 操作二：智能代码搜索（不用读整个文件）

```python
from openviking import OpenViking

ov = OpenViking()

# 语义搜索 — 找相关代码片段，只返回摘要
results = ov.find("authentication middleware implementation")
print(results)

# 带上下文的搜索（更智能）
session = ov.session()
session.add(role="user", content="I'm working on adding OAuth to the API")
results = session.search("how is authentication currently handled")
print(results)
```

## 操作三：分层读取代码文件

```bash
# 只读 L0 摘要（~100 tokens，快速了解文件用途）
ovcli abstract viking://resources/my-project/src/auth/middleware.ts

# 读 L1 概览（~2k tokens，了解函数签名和结构）
ovcli overview viking://resources/my-project/src/auth/

# 只在真正需要时读完整文件（L2）
ovcli read viking://resources/my-project/src/auth/middleware.ts
```

Python SDK：
```python
# L0：极简摘要
print(ov.abstract("viking://resources/my-project/src/auth/middleware.ts"))

# L1：结构概览
print(ov.overview("viking://resources/my-project/src/"))

# L2：完整内容
print(ov.read("viking://resources/my-project/src/auth/middleware.ts"))
```

## 操作四：对话记忆（跨 session 保留编码上下文）

```python
from openviking import OpenViking

ov = OpenViking()
session = ov.session()

# 添加本次编码对话
session.add(role="user", content="在 src/api/users.ts 中添加了 JWT 验证逻辑")
session.add(role="assistant", content="已实现，使用 RS256 算法，token 有效期 24h")

# 提交 — 自动提取记忆（决策、偏好、实体等6类）
session.commit()
# 下次提问时，会自动召回"JWT 实现细节"相关记忆
```

## 省 Token 最佳实践

### ✅ 推荐做法

```
# 先用 L0 定位，确认相关再深入
"搜索项目中处理用户认证的模块"  
→ OpenViking 返回 L0 摘要（~100 tokens）

# 确认相关后读 L1
"给我看 auth 目录的结构"
→ OpenViking 返回 L1 概览（~2k tokens）

# 最后才读具体文件
"读取 middleware.ts 的完整内容"
→ 只读1个文件（按需）
```

### ❌ 避免的做法

```
# 不要一开始就问"分析整个项目"
# 不要把整个目录用 cat 塞进上下文
# 不要重复添加相同代码库
```

## 代码摘要模式配置

在 `~/.openviking/ov.conf` 中设置代码摘要策略：

```json
{
  "code": {
    "code_summary_mode": "ast"
  }
}
```

| 模式 | 说明 | 适用场景 |
|------|------|---------|
| `ast` | 提取 AST 骨架（类名、方法签名）| 推荐，速度快成本低 |
| `llm` | 用 LLM 生成摘要 | 需要语义摘要时 |
| `ast_llm` | AST + LLM 联合 | 最高质量，成本最高 |
