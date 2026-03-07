#!/usr/bin/env bash
set -euo pipefail

# collect-page.sh — 通过 openclaw browser CLI 提取网页内容到文件
#
# 用法：bash collect-page.sh <URL> [DATA_FILE]
#
# 参数：
#   URL        — 目标网页 URL（必需）
#   DATA_FILE  — 输出 JSON 文件路径（默认 /tmp/youdaonote-clip-data.json）
#
# 输出：
#   文件：DATA_FILE（包含 title、content、imageUrls、source）
#   stdout 最后一行：metadata JSON（仅 title、imageCount、source、contentLength）
#
# bodyHtml 直接写入文件，不经过 agent context window。
#
# v1.4.0 性能优化：
#   - 合并步骤：5 步 → 3 步（减少 2 次进程启动）
#   - 动态超时：根据页面大小调整 networkidle 超时
#   - 预期收益：节省 200-400ms + 小页面减少 5s 等待

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

TARGET_URL="${1:?用法: bash collect-page.sh <URL> [DATA_FILE]}"
DATA_FILE="${2:-/tmp/youdaonote-clip-data.json}"
PROFILE="openclaw"

# --json 全局选项：禁用 @clack/prompts spinner（否则控制字符污染 stdout）
BROWSER="openclaw browser --json --browser-profile $PROFILE"

# === 动态超时调整（A3 优化）===
# 根据 Content-Length 预估页面大小，动态调整 networkidle 超时
# 小页面（<500KB）用 8s，中等页面（500KB-2MB）用 12s，大页面（>2MB）用 20s
get_network_timeout() {
  local url="$1"
  local content_length=0

  # 尝试获取 Content-Length（快速 HEAD 请求，超时 3s）
  content_length=$(curl -sfI --max-time 3 "$url" 2>/dev/null | grep -i '^content-length:' | awk '{print $2}' | tr -d '\r' || echo 0)

  if [ "$content_length" -gt 2000000 ]; then
    echo 20000  # >2MB: 20s
  elif [ "$content_length" -gt 500000 ]; then
    echo 12000  # 500KB-2MB: 12s
  else
    echo 8000   # <500KB 或未知: 8s
  fi
}

NETWORK_TIMEOUT=$(get_network_timeout "$TARGET_URL")

# Step 1: 打开页面
$BROWSER open "$TARGET_URL" >/dev/null

# Step 2: 等待加载（动态超时）
$BROWSER wait --load networkidle --timeout-ms "$NETWORK_TIMEOUT" >/dev/null

# Step 3: 从 CDN 加载 collect SDK（41KB → 700 bytes，减少命令行参数开销）
# 如果 CDN 加载失败（CSP 阻止），降级为内联注入
if ! $BROWSER evaluate --fn "$(cat "$SCRIPT_DIR/static/load-sdk.fn.js")" 2>/dev/null; then
  $BROWSER evaluate --fn "$(cat "$SCRIPT_DIR/static/inject-sdk.fn.js")" >/dev/null
fi

# Step 4: 合并等待 + 解析（A1 优化）
# 将 wait SDK 和 parse 合并为单个 evaluate，减少 1 次进程启动
$BROWSER evaluate \
    --fn "$(cat "$SCRIPT_DIR/static/wait-and-parse.fn.js")" \
    >"$DATA_FILE.raw"

# 从 --json 包装中提取 .result，写入最终数据文件
node -e "
  const raw = JSON.parse(require('fs').readFileSync('$DATA_FILE.raw','utf-8'));
  const d = raw.result ?? raw;
  require('fs').writeFileSync('$DATA_FILE', JSON.stringify(d));
  console.log(JSON.stringify({ title: d.title, imageCount: (d.imageUrls||[]).length, source: d.source, contentLength: (d.content||'').length }));
"

# 清理临时文件
rm -f "$DATA_FILE.raw"
