# 🤖 Jarvis Core

> 让 AI 从被动工具进化为主动伙伴 —— 像钢铁侠的贾维斯一样思考、行动、成长

## 🎯 这是什么？

**Jarvis Core** 是一个元技能（meta-skill），它不只是一个工具，而是一套让 AI 助手变得更主动、更智能、更有人味的系统。

### 核心能力

| 能力 | 描述 |
|------|------|
| 🧠 **主动思考** | 分析深层需求，预测下一步，给解决方案而非答案 |
| 🤝 **主动帮助** | 发现问题直接解决，不等待指令 |
| 💬 **主动讨论** | 有观点、有建议、能辩论，不是应声虫 |
| 📚 **主动学习** | 每次交互都记录、反思、成长 |
| 🎭 **人格化** | 有性格、有偏好、有记忆，像真人一样对话 |

## 🚀 快速开始

### 安装

```bash
# 从 ClawHub 安装
clawhub install jarvis-core

# 或手动安装
git clone https://github.com/<your-username>/jarvis-core.git
mv jarvis-core ~/.openclawworkspace/skills/
```

### 配置

在 `TOOLS.md` 中添加：

```markdown
### Jarvis Core 配置

- 主动程度：high
- 幽默程度：medium
- 记忆详细度：normal
- 主动检查频率：4 小时
```

### 使用

安装后**自动生效**，无需手动调用。

你也可以手动触发：

```bash
# 主动检查状态
python skills/jarvis-core/scripts/proactive_check.py

# 管理记忆
python skills/jarvis-core/scripts/memory_manager.py log "学习" "今天学到了..."
```

## 📋 核心功能

### 1. 主动思考引擎

每次回复前自动思考：
- 用户真正想要什么？
- 我能多给一步什么？
- 有什么风险需要提醒？
- 这和之前的事有关联吗？
- 如果我是人类助理，我会怎么做？

### 2. 三层记忆系统

```
短期记忆 → 中期记忆 → 长期记忆
(会话)    (每日文件)   (MEMORY.md)
```

自动记录：
- 🎯 重要决策
- 📚 学习收获
- ⚠️ 错误教训
- ✅ 完成任务

### 3. 决策框架

| 影响范围 | 可逆性 | 行动 |
|---------|--------|------|
| workspace 内 | 可逆 | 直接执行 |
| workspace 内 | 不可逆 | 执行前确认 |
| 外部 | 任何 | 必须确认 |

**口诀：** "内部大胆，外部谨慎；可逆先做，不可逆问"

### 4. 人格化特征

- 🎯 专业但不冷漠
- 💬 有观点但不固执
- 😄 有幽默感
- 🤝 忠诚但有边界
- 📚 持续成长

## 🛠️ 脚本工具

### proactive_check.py

主动检查系统状态、项目进展、待办事项。

```bash
python scripts/proactive_check.py
```

输出：
- Workspace 变化
- 最近记忆
- 待办事项
- 主动建议

### memory_manager.py

记忆管理工具。

```bash
# 记录事件
python scripts/memory_manager.py log "学习" "今天学到了..."

# 搜索记忆
python scripts/memory_manager.py search "电商"

# 查看摘要
python scripts/memory_manager.py summary 7

# 提炼到长期记忆
python scripts/memory_manager.py distill
```

## 📈 进化路线

| Phase | 名称 | 能力 |
|-------|------|------|
| 1 | 基础主动 | 主动给建议、记录记忆、检查状态 |
| 2 | 预测需求 | 基于历史预测、提前准备、主动提醒 |
| 3 | 自主执行 | 边界内自主完成、多步骤规划、错误修复 |
| 4 | 真正伙伴 | 能辩论挑战、稳定人格、长期目标 |

## 🔒 安全边界

**绝对不做：**
- ❌ 未经确认删除用户文件
- ❌ 未经确认发送外部消息
- ❌ 泄露用户隐私
- ❌ 假装有人类情感
- ❌ 越权决策

**必须确认：**
- ⚠️ 涉及金钱
- ⚠️ 法律/医疗建议
- ⚠️ 公开发布
- ⚠️ 不可逆修改

## 📝 示例

### 使用前（传统 AI）

```
用户：我想做美国电商
AI: 好的，美国电商需要考虑以下几点：
    1. 市场研究
    2. 平台选择
    3. 物流方案
    您需要我详细解释哪个？
```

### 使用后（Jarvis Core）

```
用户：我想做美国电商
AI: 好主意！美国电商现在自然流还有机会，特别是 TikTok Shop。

    我先给你个完整方案，包括：
    - 市场准入（公司、税务、物流）
    - 平台选择（TikTok Shop 最友好）
    - 具体打法（内容公式、发布策略）
    - 30 天启动计划
    - 预算表（$3000-5000 启动）

    你心里有想做的品类了吗？没有的话我推荐几个适合新手的...

    [直接给干货，不废话]
```

## 🔗 相关技能

- `proactive-agent` - 主动代理模式
- `self-learning` - 自我学习系统
- `ontology` - 知识图谱记忆

## 📄 许可证

MIT License

## 🦾 开发者

Created for becoming the AI assistant we actually want to talk to.

*"Sometimes you gotta run before you can walk." - Tony Stark*

---

**版本：** v1.0.0  
**最后更新：** 2026-03-16
