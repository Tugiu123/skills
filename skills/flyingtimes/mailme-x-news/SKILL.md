---
name: mailme-x-news
description: 抓取 X/Twitter 帖子，通过 AI 翻译成中文，并发送邮件。完全通过技能控制，无需额外脚本。
---

# MailMe X News

抓取 X/Twitter 帖子，通过 AI（translate 技能）翻译成中文，并发送邮件。完全通过技能控制，无需额外脚本。

## 环境变量说明

- **`$CLAWD`**：OpenClaw 工作目录的绝对路径（如 `/Users/clark/clawd`）
- 所有命令中使用 `$CLAWD` 而非硬编码绝对路径，确保跨环境兼容
- 技能会在任何 OpenClaw 环境下正常工作，无需修改路径

## 配置

创建配置文件 `config.json`（与 SKILL.md 同目录）：

```json
{
  "to": "chenguangming@gd.chinamobile.com",
  "cc": "fanliang@gd.chinamobile.com"
}
```

- **to**: 主收件人
- **cc**: 抄送人（可留空）

## 前置要求

使用此技能前，确保以下技能已配置完成：

1. **crawl-from-x** - X/Twitter 抓取工具
   - 安装并配置 OpenClaw Browser Relay
   - 浏览器已登录 X 账号
   - 已添加关注的用户到用户列表

2. **send-email** - 邮件发送工具
   - 已配置 SMTP 服务器
   - 已保存发件人邮箱和密码到 keyring

3. **translate** - 翻译技能
   - 已安装并可用（AI 会自动使用）

## 使用方法

### 完整工作流程

```
使用 crawl-from-x 技能抓取 X 推文
```

AI 会自动执行以下操作：

1. **抓取** - 调用 crawl-from-x 技能，保存到 `results/` 目录
2. **翻译** - 调用 translate 技能，翻译最新的 md 文件
3. **发送** - 调用 send-email 技能，发送邮件
   - 自动读取 `config.json` 中的收件人和抄送人配置
   - 自动查找最新的翻译文件

就这么简单！一条指令完成所有步骤 ✨

---

## 技能调用流程

### 步骤 1: 抓取 X 推文

AI 会调用 `crawl-from-x` 技能，抓取所有关注用户的最新推文。

**结果保存到：**
```
$CLAWD/skills/crawl-from-x/results/posts_YYYYMMDD_HHMMSS.md
```

---

### 步骤 2: 翻译为中文

AI 会调用 `translate` 技能，自动：

1. **查找最新文件**：在 `results/` 目录下按时间排序，找到最新的 `*.md` 文件
2. **翻译内容**：应用翻译规则：
   - 保持 Markdown 格式（标题、链接、粗体等）
   - 不翻译代码块、HTML 标签
   - 不翻译 URL、用户名、技术术语
   - 保留数字、日期、ID 的原始格式
   - 适应中文语境和表达习惯
3. **保存翻译**：保存为 `posts_YYYYMMDD_HHMMSS_zh.md`（添加 `_zh` 后缀）

---

### 步骤 3: 发送邮件

AI 会调用 `send-email` 技能，自动：

1. **读取配置**：从 `config.json` 中读取收件人和抄送人
2. **查找文件**：在 `results/` 目录下查找最新的 `*_zh.md` 文件
3. **切换工作目录**：**必须先切换到 `results/` 目录**（关键步骤！）
   - 原因：Markdown 文件中的图片使用相对路径 `images/xxx.png`
   - 只有在 `results/` 目录下执行，相对路径才能正确解析
4. **发送邮件**：
   - 收件人：`config.json` 中设置的 `to`
   - 抄送人：`config.json` 中设置的 `cc`（如果有）
   - 主题：自动生成（包含时间戳）
   - 内容：自动检测 Markdown 格式并内嵌图片
   - **模板**：使用 `default` 模板（仿照 x.com 样式）
   - **标题**：设置为"X 帖子摘要"

**⚠️ 重要：工作目录问题**

使用 `$CLAWD` 环境变量确保跨环境兼容：

```bash
# ❌ 错误做法（绝对路径，不同环境会失效）
cd /Users/clark/clawd/skills/send-email/scripts
python3 send_email.py send --body "$(cat ../crawl-from-x/results/*_zh.md)" ...

# ✅ 正确做法（使用 $CLAWD 环境变量）
cd $CLAWD/skills/crawl-from-x/results
python3 $CLAWD/skills/send-email/scripts/send_email.py send \
  --to "recipient@example.com" \
  --subject "X 推文摘要" \
  --body "$(cat posts_20260302_123015_zh.md)" \
  --template default \
  --title "X 帖子摘要"
```

**模板说明：**
- `--template default`：使用默认模板（仿照 x.com 样式）
- `--title "X 帖子摘要"`：设置邮件标题（显示在模板中）

---

## 配置文件说明

**文件位置：** `config.json`（与 SKILL.md 同目录）

**配置内容：**
```json
{
  "to": "chenguangming@gd.chinamobile.com",
  "cc": "fanliang@gd.chinamobile.com"
}
```

**字段说明：**
- `to`：主收件人邮箱地址（必填）
- `cc`：抄送人邮箱地址（可选，数组或字符串）

**修改收件人或抄送人：**
编辑 `config.json` 文件即可，无需修改 SKILL.md。

---

## 快速示例

### 示例 1: 发送 X 推文摘要

```
使用 crawl-from-x 技能抓取 X 推文
```

AI 会自动完成所有步骤（抓取 → 翻译 → 发送）。

---

### 示例 2: 查看配置

```
查看 mailme-x-news 的配置
```

AI 会显示当前的收件人和抄送人配置。

---

### 示例 3: 修改配置

```
修改 config.json，收件人改为 your-email@example.com
```

AI 会更新配置文件中的 `to` 字段。

---

## 文件命名规则

- **原始文件**：`posts_20260301_213000.md`（抓取时间戳）
- **翻译文件**：`posts_20260301_213000_zh.md`（添加 `_zh` 后缀）
- **排序依据**：修改时间（`mtime`）

---

## 注意事项

1. **Browser Relay** - 抓取前必须启动并确保浏览器扩展已连接
2. **登录状态** - 浏览器必须登录 X 账号
3. **翻译质量** - 使用 AI 翻译，质量优于自动翻译工具
4. **邮件配置** - 确保 `send-email` 技能已正确配置 SMTP 和密钥
5. **配置文件** - 收件人和抄送人通过 `config.json` 配置，无需修改代码
6. **文件清理** - 定期清理旧的抓取结果文件，避免占用磁盘空间
7. **时间排序**：AI 会根据文件的修改时间判断"最新"，确保每次都处理正确的文件

---

## 故障排查

### 抓取失败

- 检查 Browser Relay 是否启动：`openclaw browser status`
- 检查浏览器扩展是否已连接（显示绿色图标）
- 检查是否登录了 X 账号
- 查看用户列表：`cd $CLAWD/skills/crawl-from-x/scripts && python3 craw_hot.py list`

### 翻译失败

- 确认抓取已完成：`ls -lht $CLAWD/skills/crawl-from-x/results/`
- 确保 translate 技能已安装并可用
- 检查文件是否存在且可读

### 发送失败

- 检查配置文件：`cat $CLAWD/skills/mailme-x-news/config.json`
- 检查 SMTP 配置：`cd $CLAWD/skills/send-email/scripts && python3 send_email.py config`
- 检查密钥是否已保存：`python3 send_email.py username` 和 `python3 send_email.py password`
- 确认翻译已完成：`ls -lht $CLAWD/skills/crawl-from-x/results/*_zh.md`
- 检查模板是否存在：`ls -la $CLAWD/skills/send-email/templates/`

### 邮件中没有图片

**症状：** 邮件发送成功，但所有图片都显示为跳过警告。

**原因：** 工作目录错误，导致相对路径 `images/xxx.png` 无法解析。

**解决方法：**
```bash
# 切换到正确的目录（使用 $CLAWD 环境变量）
cd $CLAWD/skills/crawl-from-x/results

# 重新发送邮件
python3 $CLAWD/skills/send-email/scripts/send_email.py send \
  --to "recipient@example.com" \
  --subject "X 推文摘要" \
  --body "$(cat posts_20260302_123015_zh.md)"
```

**检查方法：**
```bash
# 确认图片文件存在
ls -lh $CLAWD/skills/crawl-from-x/results/images/

# 确认当前工作目录
pwd
# 应该输出：$CLAWD/skills/crawl-from-x/results
# 例如：/Users/clark/clawd/skills/crawl-from-x/results
```

---

## 定时任务

可以通过 OpenClaw cron 设置定时任务，每天自动发送 X 推文摘要。

示例：每天中午 12:08 执行
```
mailme-x-news
```

Cron 配置示例：
```bash
0 8 12 * * @ Asia/Shanghai
```

---

## 技术说明

**技能控制流程：**

1. **用户指令** → `使用 crawl-from-x 技能抓取 X 推文`
2. **AI 解析** → 识别意图，确定要执行的步骤
3. **技能调用链**：
   - `crawl-from-x` 抓取 → 保存 md 文件到 `results/`
   - `translate` 翻译 → 保存 *_zh.md 文件到 `results/`
   - `send-email` 发送 → **切换到 `results/` 目录**，然后调用 send_email.py

**无额外脚本：**
- 不需要任何 Python 脚本
- 所有逻辑通过 AI 和技能控制完成
- 配置文件简化为 JSON 格式

**⚠️ 关键：工作目录与相对路径**
- Markdown 文件中图片使用相对路径：`images/xxx.png`
- 图片实际位置：`results/images/`
- **必须**在发送邮件前切换到 `results/` 目录，否则图片路径解析失败
- 正确的命令示例（使用 `$CLAWD` 确保跨环境兼容）：
  ```bash
  cd $CLAWD/skills/crawl-from-x/results
  python3 $CLAWD/skills/send-email/scripts/send_email.py send \
    --to "recipient@example.com" \
    --subject "X 推文摘要" \
    --body "$(cat posts_20260302_123015_zh.md)" \
    --template default \
    --title "X 帖子摘要"
  ```

**模板功能：**
- 使用 `--template default` 启用模板渲染
- 模板会自动应用现代简约的商务风格
- 卡片式布局，仿照 x.com 网页样式
- 完全兼容 Markdown 自动检测和图片内嵌

**配置优先级：**
1. `config.json` 中的 `to` 和 `cc`
2. 如果没有 `config.json`，使用默认值

---

## 更新日志

- **2026-03-02 v4** - 添加模板支持
  - 使用 `--template default` 参数启用模板渲染
  - 默认模板仿照 x.com 样式，现代简约商务风格
  - 完全兼容 Markdown 自动检测和图片内嵌
  - 更新所有命令示例，包含模板参数

- **2026-03-02 v3** - 使用环境变量确保跨环境兼容
  - 所有绝对路径改为 `$CLAWD` 环境变量
  - 避免不同用户环境下路径不一致的问题
  - 提高技能的可移植性

- **2026-03-02 v2** - 修正工作目录问题
  - 添加关键步骤：发送邮件前必须切换到 `results/` 目录
  - 新增"邮件中没有图片"故障排查条目
  - 强调相对路径的处理逻辑

- **2026-03-02 v1** - 初始版本
  - 完全基于技能控制
  - 添加 config.json 配置支持
  - 自动化抓取、翻译、发送流程
