---
name: code-review-cycle
description: |
  自动化 Code Review 循环流程（需搭配 ACP + OpenClaw 使用）。
  通过 ACP 协议调度两个 AI Agent 协作：A（Coder）写代码 → B（Reviewer）Review → 自动循环或等待用户决策。
  支持 codex / claude-code 作为 Coder 或 Reviewer，可配置循环轮数。
user-invocable: true
aliases: ["/cr", "/review-cycle", "/code-review"]
metadata:
  openclaw:
    requires:
      bins:
        - git
        - node
      env:
        - ACP_RUNTIME
        - OPENCLAW_WORKSPACE
    emoji: "\U0001F99E"
    homepage: https://github.com/Raccoon-Office/code-review-cycle-skill
tags:
  - code-review
  - review
  - pair-programming
  - acp
  - openclaw
  - multi-agent
  - coding-workflow
  - quality-assurance
  - automated-review
  - collaboration
---

# Code Review Cycle

自动化的 A(编码) → B(Review) → 决策 协作流程。

## 前置条件

> **重要：本 Skill 依赖以下环境，使用前请确认已正确配置。**

| 依赖项 | 说明 | 安装/配置 |
|--------|------|-----------|
| **ACP（Agent Communication Protocol）** | Agent 间通信协议，用于 spawn subagent | 需要 ACP runtime 已启动并可用 |
| **OpenClaw** | Skill 运行平台，提供 `sessions_spawn` 等调度能力 | 需要 OpenClaw 已安装并配置 workspace |
| **至少一个可用的 AI Agent** | codex 或 claude-code，用于担任 Coder/Reviewer 角色 | 确保 agent 已通过 ACP 注册并可被调度 |
| **Git** | A（Coder）完成编码后会自动 commit | 项目目录需要是 git 仓库 |

### 环境检查清单

- [ ] ACP runtime 已启动（`acp status` 或等效命令可用）
- [ ] OpenClaw workspace 已配置
- [ ] 目标 Agent（codex / claude-code）已注册到 ACP
- [ ] 项目目录已初始化 git

## 角色职责

| 角色 | 职责 | 权限 |
|------|------|------|
| **A (Coder)** | 写代码、改文件、实现功能 | ✅ 可写文件 |
| **B (Reviewer)** | Review 代码、提建议、做决策 | ❌ **只读，不写文件** |
| **主会话** | 调度 A/B、传递上下文、最终决策 | - |

## 触发方式

```
/cr <功能描述>
/cr --agent-a codex --agent-b claude-code <功能描述>
/cr --rounds 2 <功能描述>  # 最多自动循环 2 轮
/cr --cwd /path/to/project <功能描述>
```

## 参数

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `--agent-a` | `codex` | 负责写代码的 agent (codex/claude-code) |
| `--agent-b` | `claude` | 负责 Review 的 agent (claude/codex) |
| `--rounds` | `1` | 自动循环轮数（A→B 算一轮，默认 1 轮后暂停等待用户决策；设为 0 则每步都等用户确认） |
| `--cwd` | 当前 workspace | 代码目录 |

## 工作原理

### 核心机制：通过 ACP 调度 subagent

本 Skill 的核心是通过 ACP 协议的 `sessions_spawn` 能力，在 OpenClaw 平台上调度 AI Agent：

```
主会话 ──(ACP sessions_spawn)──→ A (Coder Agent)
                                      │
                                      ↓ 完成后
主会话 ──(ACP sessions_spawn)──→ B (Reviewer Agent, 只读)
                                      │
                                      ↓ 完成后
主会话 ← 汇总结果，等待用户决策
```

### 流程（默认自动跑完一整轮）

#### 一轮 = A 写代码 + B Review，中间不停

1. **Spawn A（编码）** → 写代码、git commit，等待完成
2. **A 完成后立即 Spawn B（Review）** → 只读 Review，等待完成
3. **B 完成后汇总整轮结果给用户**：
   - A 做了什么（改动摘要）
   - B 的 Review 结论（严重问题/建议优化/结论）
4. **决策点**（汇总后）：
   - 如果 `--rounds > 1` 且 B 认为需要修改 → 自动进入下一轮（把 B 的 Review 反馈作为 A 的输入）
   - 达到 rounds 上限或 B 认为可以合并 → 停下来等用户指令

### 关键原则
- **一轮之内不暂停**：A 完成后直接启动 B，不要问用户"要不要看效果"或"要不要继续"
- **只在一轮结束后才跟用户交互**
- **每轮的 A 和 B 都通过 ACP subagent 调用**（确保有 announce 通知）

### Reviewer 只读保障机制

B（Reviewer）的只读约束通过以下**多层机制**共同保障：

1. **Prompt 层**：B 的任务 prompt 明确声明"只读不写文件"、"不要修改任何文件，不要 git commit"
2. **ACP Agent 权限层（推荐配置）**：在 ACP 中为 Reviewer agent 配置只读权限（如 `permissions: read-only` 或等效配置），从 runtime 层面禁止写操作
3. **OpenClaw spawn 参数层**：可在 sessions_spawn 时通过参数限制 agent 的文件系统权限

> **注意**：如果仅依赖 prompt 层约束，agent 仍有技术上的写入能力。**强烈建议在 ACP 层面配置 Reviewer agent 为只读权限**，实现技术性强制执行。

## run.js 说明

`run.js` 是一个辅助脚本，**仅用于展示 sessions_spawn 调用的 payload 示例**，不会实际调用 ACP 或执行 git 操作。真正的调度行为由 OpenClaw 主会话根据 SKILL.md 的指令完成。

## 调度实现

每次 spawn A 或 B，都用以下模式：

```
sessions_spawn(
  mode: "run",
  model: "claude4.6",
  runTimeoutSeconds: 300,
  task: "调度 subagent，内部调 sessions_spawn(runtime='acp', agentId=..., cwd=..., task=...)"
)
```

等收到 A 的 completion event 后，立即 spawn B，不等用户确认。
等收到 B 的 completion event 后，汇总整轮结果回复用户。

## 输出格式约定

### 整轮汇总（给用户看的）
```markdown
## /cr 第 N 轮完成

### A（Codex）改动摘要
- 文件 1: ...
- 文件 2: ...
- commit: xxx

### B（Claude）Review 结果
#### 严重问题
- （无 / 列表）

#### 建议优化
1. ...
2. ...

#### 结论
✅ 可以直接合并 / ⚠️ 需要修改（问题 #1, #3）

---
要让 A 根据 Review 改一轮吗？还是就这样？
```

### A 的任务 prompt 模板
```
在 {cwd} 项目中完成以下功能：{task_description}

完成后用 git add 和 git commit。
```

### B 的任务 prompt 模板
```
你是 Code Reviewer（角色 B），**只读不写文件**。
请 Review {cwd} 项目的最近改动。

按以下格式输出：

## [B-Review] 严重问题
- 列出必须修复的问题（如有）

## [B-Review] 建议优化
- 列出可以改进的地方（如有）

## [B-Review] 结论
□ 需要修改（具体问题：#1, #3）
□ 可以直接合并

---
[B 职责说明] 我只负责 Review，不修改任何文件。如需修改，请 A 执行。

**重要：不要修改任何文件，不要 git commit。**
```

### 第 2+ 轮 A 的任务 prompt 模板
```
在 {cwd} 项目中，根据以下 Code Review 反馈进行修改：

{B 的 Review 内容}

请修复上述问题，完成后 git add 和 git commit。
```

## 示例

```
/cr 实现用户登录表单验证
/cr --agent-a claude --agent-b codex 添加暗色模式切换
/cr --rounds 2 重构 utils/date.ts 增加单元测试
/cr --cwd /Users/xxx/project 修复导航栏样式
```

## 注意事项

- **前置依赖**：必须有 ACP runtime + OpenClaw 环境，否则无法调度 subagent
- **默认一整轮不停**：A→B 自动串联，只在整轮结束后暂停
- 主会话作为调度器，保留所有历史便于追溯
- A 和 B 的会话是临时的，用完即弃
- **B 只读不写** — Review 角色不修改任何文件
- 多轮模式下，B 的 Review 会自动传给下一轮的 A
- 如果 Agent 不在 ACP 中注册，spawn 会失败，请检查 ACP 配置
