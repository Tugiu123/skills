---
name: sunsetbot-monitor-cn
description: 查询中国国内火烧云预报（sunsetbot.top）。当用户询问某城市的火烧云/晚霞预报，或需要设置定时火烧云通知时使用此 skill。
---

# Sunset Bot - 火烧云预报（国内版）

## ⚠️ 重要：调用方式

本 Skill **必须在 OpenClaw 会话环境中执行**，不能直接用 `node` 命令运行。

**依赖的全局工具**：
- `browser()` - 浏览器自动化（OpenClaw 内置）
- **消息通道** - 发送火烧云通知需要有效的消息通道。默认使用飞书（依赖 `feishu_im_user_message()` 函数），用户也可在 `scripts/check.js` 中实现其他消息通道

**❌ 错误调用**：
```bash
node scripts/check.js              # 报错：browser is not defined
exec node -e "handler({...})"      # 报错：browser is not defined
```

**✅ 正确调用**：
1. **对话查询**：spawn subagent 执行（见下文"使用方式"）
2. **定时监控**：通过 cron 配置，由 OpenClaw 自动执行

---

## 快速开始

### 1. 环境要求

本 Skill 需要浏览器支持：
- **本地环境**：通常已有浏览器，无需额外配置
- **云服务器**：需安装 Headless Chromium，详见[附录](#附录)

### 2. 配置（定时通知必须）

创建 `config/config.json`：

```json
{
  "notifyChannel": "feishu",
  "userOpenId": "你的飞书Open ID"
}
```

| 参数 | 说明 |
|------|------|
| notifyChannel | 通知渠道：`feishu` / `telegram` / `none` |
| userOpenId | 飞书 Open ID（飞书开发者后台获取）|

> 💡 对话测试时无需配置，定时通知时必须配置。

---

## 使用方式

### 对话查询

当用户询问火烧云预报时，**spawn subagent 执行**：

1. 读取 `SKILL.md` 和 `scripts/check.js`
2. Spawn 一个 subagent
3. 在 subagent 中调用：
   ```javascript
   handler({ city: '深圳', dates: ['明天日出', '明天日落'], source: 'GFS' })
   ```

### 定时监控

通过 cron 自动运行，有火烧云时发送通知：

```bash
openclaw cron add \
  --name "sunsetbot-morning" \
  --cron "0 9 * * *" \
  --tz "Asia/Shanghai" \
  --message "读取 skills/sunsetbot-monitor-cn/scripts/check.js，调用 handler({ city: '深圳', dates: ['明天日出', '明天日落'], source: 'GFS', needNotify: true })" \
  --no-deliver
```

---

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| city | 城市名称 | 深圳 |
| dates | 日期类型数组：`今天日出`、`今天日落`、`明天日出`、`明天日落` | `["明天日出", "明天日落"]` |
| source | 数据源：`GFS` 或 `EC` | GFS |
| needNotify | 是否发送通知并记录日志 | false |
| dryRun | 干运行模式，只查询不通知不记日志 | false |

---

## 技术细节

- 使用 JavaScript evaluate 直接操作 DOM
- 日期类型映射：`今天日出=rise_1`，`今天日落=set_1`，`明天日出=rise_2`，`明天日落=set_2`
- 日志格式：JSONL，存储在 `data/sunsetbot-monitor.log`
- 火烧云等级判定：`<0.2` 无烧，`0.2-0.5` 小烧，`0.5-1.0` 中烧，`1.0-2.0` 大烧，`>2.0` 世纪大烧

---

## 附录

- [Headless Chromium 安装指南](references/headless-chromium-setup-guide.md) - 云服务器 Linux 环境配置