# Linux 服务器 Headless Chromium 安装配置指南

> 本指南用于在 Linux 服务器上安装配置 Headless Chromium，以便 OpenClaw 的 `browser` 工具可以正常工作。

## 前提条件

- Linux 服务器（Ubuntu/Debian 推荐）
- Root 或 sudo 权限
- 已安装 OpenClaw

---

## 第一步：安装 Google Chrome

```bash
cd /tmp
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
dpkg -i google-chrome-stable_current_amd64.deb
apt --fix-broken install -y
```

### 验证安装

```bash
google-chrome --version
```

预期输出类似：
```
Google Chrome 146.0.7680.80
```

---

## 第二步：安装 Playwright 系统依赖

```bash
npx playwright install-deps chromium
```

这会安装 Chrome 运行所需的所有系统库（如 libgtk、libatk 等）。

---

## 第三步：测试 Headless 模式

```bash
google-chrome --headless --no-sandbox --disable-gpu --dump-dom https://example.com | head -20
```

**预期结果：** 输出 HTML 内容，类似：

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <title>Example Domain</title>
    ...
</head>
<body>
    <div>
        <h1>Example Domain</h1>
        ...
    </div>
</body>
</html>
```

**注意：** 可能会看到一些 WARNING 或 ERROR 信息（如 DBus/UPower 相关），这是正常的，只要 HTML 内容正确输出即可。

---

## 第四步：配置 OpenClaw

编辑配置文件 `~/.openclaw/openclaw.json`，添加 `browser` 配置项：

```json
{
  "browser": {
    "enabled": true,
    "executablePath": "/usr/bin/google-chrome-stable",
    "headless": true,
    "noSandbox": true,
    "defaultProfile": "openclaw",
    "profiles": {
      "openclaw": {
        "cdpPort": 18800,
        "color": "#FF4500"
      }
    }
  }
}
```

### 配置说明

| 参数 | 说明 |
|------|------|
| `enabled` | 启用浏览器功能 |
| `executablePath` | Chrome 可执行文件路径 |
| `headless` | 无 GUI 模式（服务器必须为 true） |
| `noSandbox` | 禁用沙箱（服务器环境通常需要） |
| `defaultProfile` | 默认使用的浏览器配置 |
| `cdpPort` | Chrome DevTools Protocol 端口 |

---

## 第五步：重启 OpenClaw Gateway

```bash
openclaw gateway restart
```

---

## 第六步：验证浏览器功能

### 方法一：命令行验证

```bash
openclaw browser status
openclaw browser start
openclaw browser open https://example.com
openclaw browser snapshot
```

### 方法二：在会话中验证

让 AI 助手执行以下操作：

```
请打开 https://example.com 并获取页面快照
```

如果成功返回页面内容，说明配置完成。

---

## 常见问题

### 问题 1：`libatk-1.0.so.0: cannot open shared object file`

**原因：** 缺少系统依赖库

**解决：**
```bash
npx playwright install-deps chromium
```

### 问题 2：`Failed to start Chrome CDP on port 18800`

**原因：** Chrome 未正确安装或配置

**解决：**
1. 确认 Chrome 版本：`google-chrome --version`
2. 检查配置文件中 `executablePath` 路径是否正确
3. 手动测试：`google-chrome --headless --no-sandbox --disable-gpu about:blank`

### 问题 3：apt/dpkg 提示权限错误

**原因：** 需要 root 权限

**解决：** 使用 `sudo` 或切换到 root 用户：
```bash
sudo -i
# 然后重新执行安装命令
```

### 问题 4：snap 版 Chromium 无法使用

**原因：** snap 的 AppArmor 限制与 OpenClaw 不兼容

**解决：** 安装官方 Google Chrome（.deb 包），不要使用 snap 版 Chromium。

---

## 使用 Playwright 自带的 Chromium（可选）

如果不想安装 Google Chrome，可以使用 Playwright 自带的 Chromium：

```bash
npx playwright install chromium
```

然后配置 `executablePath` 指向 Playwright 的 Chromium：

```json
{
  "browser": {
    "enabled": true,
    "executablePath": "/root/.cache/ms-playwright/chromium-1208/chrome-linux64/chrome",
    "headless": true,
    "noSandbox": true
  }
}
```

**注意：** Playwright Chromium 仍需要安装系统依赖：
```bash
npx playwright install-deps chromium
```

---

## 相关文档

- [OpenClaw Browser 官方文档](https://docs.openclaw.ai/tools/browser)
- [Linux 浏览器故障排除](https://docs.openclaw.ai/tools/browser-linux-troubleshooting)
- [Playwright 官方文档](https://playwright.dev)

---

## 版本信息

- 适用系统：Ubuntu 24.04 LTS / Debian 12+
- OpenClaw 版本：2026.3.x
- 更新日期：2026-03-17