---
name: openclaw-doc-finder
description: OpenClaw 文档检索专家。当用户询问 OpenClaw 配置、维护、故障排除、通道接入、技能安装、模型配置等问题时使用。支持快速定位官方文档、给出精确 URL 和关键命令。高价值触发场景包括：（1）配置 gateway、channels、plugins；（2）排查连接/认证/权限问题；（3）安装/管理技能（clawhub/skillhub）；（4）模型切换/供应商配置；（5）安全/凭证管理；（6）VPS/远程/Wi-Fi 部署；（7）openclaw CLI 命令用法；（8）any ask about "how do I configure X" / "why is Y broken" / "how to set up Z"。
---

# openclaw-doc-finder

OpenClaw 官方文档检索技能。识别用户意图，路由到正确文档，给出精确 URL + 关键命令片段。

## 检索流程（Pipeline）

```
用户问题 → 意图识别 → 文档路由 → 本地片段 / 远程拉取 → 回答
```

**严格顺序，不得跳步：**

1. **意图识别**：解析用户问题，判断属于哪个场景类别
2. **文档路由**：查 `references/doc-index.md` 定位目标文档列表
3. **本地优先**：优先使用 `references/` 下的已有片段回答
4. **缺失时拉取**：本地无相关内容 → 调用 `web_fetch` 拉取目标文档或执行 `clawhub search`
5. **版本检查**：回答结尾检查 VERSION，如文档有大版本更新则提醒用户升级技能

---

## 意图识别规则

见 `references/doc-index.md` 的「意图→文档路由表」。优先精确匹配场景关键词。

常见场景映射：

| 场景 | 目标文档 |
|------|---------|
| 首次安装 / 开始上手 | `start/getting-started.md` / `start/quickstart.md` |
| gateway 配置 / 配置文件 | `gateway/configuration.md` |
| gateway 配置项详解 | `gateway/configuration-reference.md` |
| 通道接入（Discord/Telegram/飞书等） | `channels/index.md` + 对应通道文档 |
| 技能安装 / clawhub / skillhub | `tools/clawhub` 或 `start/hubs.md` |
| 故障排除 / 报错 | `gateway/troubleshooting.md` / `channels/troubleshooting.md` |
| 凭证 / secrets / API key | `gateway/secrets.md` |
| 模型配置 / 供应商 | `providers/` 目录 + `gateway/configuration.md` |
| CLI 命令用法 | `cli/` 目录 |
| openclaw doctor | `gateway/doctor.md` |
| 安全策略 / 权限 | `gateway/security/` + `gateway/sandboxing.md` |
| 远程访问 / VPS 部署 | `gateway/remote.md` + `vps.md` |
| 心跳 / 自动化任务 | `gateway/heartbeat.md` + `cron-jobs` |
| 节点配对 / 移动端 | `nodes/` 目录 |

---

## 本地片段优先级

- `references/doc-index.md` — 始终可用，路由总表
- `references/config-guide.md` — gateway 配置高频片段
- `references/troubleshoot.md` — 常见报错速查

---

## 远程拉取规则

当用户问题涉及：
- 最新版本特性 / breaking changes
- skill 安装失败（clawhub rate limit / 网络问题）
- 文档未在本地缓存的新通道或新功能

**拉取命令：**
```bash
# 搜索 clawhub 技能
clawhub search "<关键词>"

# 拉取指定文档（docs.openclaw.ai 域名）
# 从 doc-index.md 的 URL 列获取完整路径，拼接到 https://docs.openclaw.ai
```

---

## 版本管理

- 版本文件：`VERSION`（语义化版本，格式 v1.0.0）
- **每次更新 `references/` 内容，必须同步更新 VERSION**
- 大版本更新（文档 breaking changes）：主版本号 +1，并记录 CHANGELOG 在 SKILL.md 底部

### 自动版本同步（脚本）

**脚本路径：** `scripts/sync-version.py`

**功能：**
1. 读取当前运行中的 OpenClaw 版本（`~/.npm-global/lib/node_modules/openclaw/package.json`）
2. 对比 `VERSION` 文件
3. 版本不一致时 → 自动重新扫描本地 docs 目录 → 重写 `references/doc-index.md` → 更新 VERSION

**执行方式：**
```bash
# 普通执行（直接写入）
python3 scripts/sync-version.py

# 干跑预览（不写入，只看会改什么）
python3 scripts/sync-version.py --dry-run
```

**触发时机：**
- 技能被触发时（建议每次回答前运行一次，快速检查）
- OpenClaw 大版本升级后
- 手动运行 `/openclaw_doc_finder_check` 时

---

## 输出格式规范

回答必须包含：
1. **文档标题** + **完整 URL**（`https://docs.openclaw.ai/<path>`）
2. **关键命令**（从文档中提取的 CLI 命令，用 ```bash 包裹）
3. **配置片段**（关键配置项示例）
4. **版本提示**（如已拉取最新内容，提醒技能版本）

禁止：
- 不带 URL 的泛泛回答
- 混用多个不相关的文档链接
