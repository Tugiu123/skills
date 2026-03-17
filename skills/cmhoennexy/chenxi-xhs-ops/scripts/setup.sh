#!/bin/bash
set -e

echo "🔧 Installing xhs-ops dependencies..."

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

# Python deps
pip3 install requests playwright 2>/dev/null || pip3 install --break-system-packages requests playwright

# Playwright browser
playwright install chromium 2>/dev/null || python3 -m playwright install chromium

# xiaohongshu-mcp binary
MCP_DIR="${XHS_MCP_DIR:-$HOME/tools/xiaohongshu-mcp}"
if [ ! -f "$MCP_DIR/xiaohongshu-mcp-darwin-arm64" ]; then
    echo ""
    echo "📦 xiaohongshu-mcp not found at $MCP_DIR"
    echo "   Download from: https://github.com/xpzouying/xiaohongshu-mcp/releases"
    echo ""
    echo "   Quick install:"
    echo "   mkdir -p $MCP_DIR && cd $MCP_DIR"
    echo "   curl -L -o mcp.tar.gz https://github.com/xpzouying/xiaohongshu-mcp/releases/latest/download/xiaohongshu-mcp-darwin-arm64.tar.gz"
    echo "   tar xzf mcp.tar.gz && chmod +x xiaohongshu-*"
    echo ""
    echo "   Then login: ./xiaohongshu-login-darwin-arm64"
    echo "   Then start:  nohup ./xiaohongshu-mcp-darwin-arm64 -headless > /tmp/xiaohongshu-mcp.log 2>&1 &"
else
    echo "✅ xiaohongshu-mcp found at $MCP_DIR"
    # Check if running
    if curl -s http://localhost:18060/mcp > /dev/null 2>&1; then
        echo "✅ MCP service is running"
    else
        echo "⚠️  MCP not running. Start with:"
        echo "   cd $MCP_DIR && nohup ./xiaohongshu-mcp-darwin-arm64 -headless > /tmp/xiaohongshu-mcp.log 2>&1 &"
    fi
fi

echo ""
echo "✅ Setup complete"
