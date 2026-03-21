---
name: openclaw-doctor
description: 诊断并修复 OpenClaw AI Agent 服务器的 CPU/内存/进程异常。专治：多次执行后僵尸进程堆积、exec 子进程残留、MQTT 连接泄漏、内存逐渐升高、服务器变慢。触发条件：提到 OpenClaw 卡、CPU 高、内存满、进程堆积、服务器变慢、需要诊断、需要急救。
---

# OpenClaw Doctor 🩺

> OpenClaw 服务器体检 + 进程修复 Skill。专治：僵尸进程、内存泄漏、CPU 打满。

---

## 快速体检（3 秒出结果）

```bash
echo "=== 负载 ===" && uptime
echo "=== 内存 ===" && free -m
echo "=== OpenClaw 进程 ===" && ps aux | grep -E "node|openclaw|mqtt|exec" | grep -v grep | head -10
echo "=== 僵尸进程 ===" && ps aux | awk '$8 ~ /Z/ {print}'
```

---

## 常见病因 + 处方

### 1. exec 子进程残留（最常见）

**症状**：大量 `node` / `python3` / `curl` 进程堆积，CPU 100%

**诊断**：
```bash
ps aux | grep -E "node|python3|curl" | grep -v grep | wc -l
ps aux | awk '$8 ~ /Z/ {print}'  # 找僵尸
```

**急救**：
```bash
# 按名字杀（只杀可疑的）
pkill -f "curl-smart"
pkill -f "python3.*update_hosts"

# 按 PID 杀（精确）
kill -9 $(pgrep -f "可疑关键字")
```

**根因修复**：给所有 subprocess 加 timeout，永远不用 `curl` 命令行，改用 Python urllib

### 2. MQTT 连接泄漏

**症状**：MQTT 进程堆积，Listener 反复 CONNECTING/DISCONNECTED

**处方**：
```bash
openclaw gateway restart
```

### 3. 内存逐渐升高（Node.js 堆）

**处方**：
```bash
openclaw gateway restart
```

### 4. cron 任务堆积

**处方**：
```bash
openclaw cron list
# 禁用重复的 cron
openclaw cron disable <cron-id>
```

---

## 预防规范（重要！）

### 所有 exec subprocess 必须加 timeout

```python
# ✅ 正确
subprocess.run(cmd, timeout=10)

# ❌ 错误
subprocess.run(cmd)  # 可能永远卡死
```

### 永远不用 curl，用 urllib

```python
# ✅ 正确（永远不超过5秒）
import urllib.request
with urllib.request.urlopen(url, timeout=5) as resp:
    data = resp.read()

# ❌ 错误（可能被 curl-smart 包装后重试3层）
subprocess.run(["curl", "-s", url])
```

### DNS 解析用 socket，不用命令

```python
# ✅ 正确
import socket
socket.getaddrinfo("github.com", 443)

# ❌ 错误
subprocess.run(["nslookup", "github.com"])  # 可能卡死
```

### cron 任务加进程锁

```bash
LOCK="/tmp/my-cron.lock"
if [ -f "$LOCK" ]; then exit 0; fi
trap "rm -f $LOCK" EXIT
touch "$LOCK"
# ... 业务逻辑 ...
```

---

## 实战案例

| 问题 | 原因 | 修复 |
|------|------|------|
| 2000+ curl-smart 进程 | curl 超时触发三重自动重试，无进程锁 | curl→urllib，curl-smart 加全局锁 |
| update_hosts.py 卡死 | subprocess.run curl 无 timeout | 改用 Python urllib |
| nslookup/dig 卡死 | DNS 命令超时 | 改用 socket.getaddrinfo |
| CPU 99% 内存 98% | 指数级进程堆积 | 全局锁 + urllib 替换 |

---

## 核心心法

> **每次 exec 调用，都是一个潜在的生命周期。**
> 不设 timeout，就是打开了潘多拉魔盒。
