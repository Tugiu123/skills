---
name: skill-manager-all-in-one
description: "One-stop skill management for OpenClaw. 一站式技能管理，引导式使用，嵌套搜索、审计、创建、发布、批量更新等必要 skill。Use when reviewing installed skills, searching ClawHub, checking updates, auditing security, creating or publishing skills. Triggers: 帮我看看有没有更好的 X 技能, 审查我的 skill 体系, 检查 skill 更新, 创建一个 skill, 发布 skill, 批量更新 skill, 标准化 skill, 技能管理, 管理 skill, 安装 skill, 卸载 skill, 搜索 skill, 找 skill, 新建 skill, 制作 skill, skill 问题, skill 帮助, manage skills, install skill, create skill, update skills, search skills, skill manager."
---

# Skill Manager | 技能管理器

全面的 OpenClaw 技能管理工具。一站式解决 skill 管理问题。

**⚠️ 系统兼容性 / System Compatibility**
本技能在 **Linux 系统**上测试通过。其他系统（Windows/macOS）可能需要适配。

---

## 核心原则

1. **先本地，后网络** — 优先使用本地已有资源
2. **决定权交给用户** — 任何操作都需讲解给用户并等待确认
3. **命名规范化** — 统一格式，便于管理

---

## 快速导航 | Quick Navigation

| 场景 | 参考 |
|------|------|
| 了解术语、目录结构、命名规范 | [terminology.md](references/terminology.md) |
| 搜索、对比、审计技能 | [search-audit.md](references/search-audit.md) |
| 创建、发布、更新技能 | [create-publish-update.md](references/create-publish-update.md) |
| 查看已发布技能 | [dashboard.md](references/dashboard.md) |

---

## CLI 命令速查

```bash
# 搜索
npx clawhub@latest search <query>

# 查看详情
npx clawhub@latest inspect <slug>

# 安装
npx clawhub@latest install <slug>

# 发布
npx clawhub@latest publish <path> --slug <slug> --name "<name>" --version <version> --changelog "<changelog>"

# 浏览最新
npx clawhub@latest explore
```

---

## 嵌套引用

本 skill 通过**路径引用**其他 skills，不嵌入全文：

| 场景 | 引用路径 |
|------|----------|
| 搜索 skills | `~/.openclaw/skills/<搜索skill名>/SKILL.md` |
| 创建 skill | `~/.npm-global/lib/node_modules/openclaw/skills/skill-creator/SKILL.md` |
| 安全审计 | `~/.openclaw/skills/<审计skill名>/SKILL.md` |

**好处：** 被引用 skill 更新时，自动获得最新版本。

---

## ⚠️ 安全与隐私须知

**在技能生成、整理和上传过程中，严禁包含以下个人隐私内容：**

- ❌ 验证码 / Verification codes
- ❌ 个人账号信息 / Personal account information
- ❌ 联系人代码 / Contact codes
- ❌ 机器型号 / Machine models
- ❌ 其他敏感个人信息 / Other sensitive personal information

**违反此原则可能导致隐私泄露！**
