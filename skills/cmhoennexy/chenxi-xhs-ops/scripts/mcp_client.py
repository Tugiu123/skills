"""
Xiaohongshu MCP client — shared by all tools.
Handles session management, tool calls, and sensitive word filtering.
"""
import requests
import json
import os

DEFAULT_MCP_URL = "http://localhost:18060/mcp"

class MCPClient:
    def __init__(self, mcp_url=None):
        self.mcp_url = mcp_url or DEFAULT_MCP_URL
        self.session_id = None
        self._req_id = 0

    def _next_id(self):
        self._req_id += 1
        return self._req_id

    def initialize(self):
        """Initialize MCP session, return session_id."""
        resp = requests.post(self.mcp_url, json={
            "jsonrpc": "2.0",
            "id": self._next_id(),
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {"name": "xhs-ops", "version": "1.0"}
            }
        }, timeout=10)
        resp.raise_for_status()
        self.session_id = resp.headers.get("mcp-session-id") or resp.headers.get("Mcp-Session-Id")
        if not self.session_id:
            raise RuntimeError("MCP initialize did not return session-id")
        return self.session_id

    def call_tool(self, name, arguments=None):
        """Call an MCP tool, return parsed result."""
        if not self.session_id:
            self.initialize()
        resp = requests.post(self.mcp_url,
            headers={"mcp-session-id": self.session_id},
            json={
                "jsonrpc": "2.0",
                "id": self._next_id(),
                "method": "tools/call",
                "params": {"name": name, "arguments": arguments or {}}
            },
            timeout=30
        )
        resp.raise_for_status()
        data = resp.json()
        if "error" in data:
            raise RuntimeError(f"MCP tool {name} failed: {data['error']}")
        content = data.get("result", {}).get("content", [])
        texts = []
        for c in content:
            if c.get("type") == "text":
                text = c.get("text", "")
                try:
                    texts.append(json.loads(text))
                except (json.JSONDecodeError, TypeError):
                    texts.append(text)
        return texts[0] if len(texts) == 1 else texts

    def search_feeds(self, keyword, sort_by="最多点赞", note_type="图文"):
        return self.call_tool("search_feeds", {
            "keyword": keyword,
            "filters": {"sort_by": sort_by, "note_type": note_type}
        })

    def post_comment(self, feed_id, xsec_token, content):
        return self.call_tool("post_comment_to_feed", {
            "feed_id": feed_id, "xsec_token": xsec_token, "content": content
        })

    def get_feed_detail(self, feed_id, xsec_token):
        return self.call_tool("get_feed_detail", {
            "feed_id": feed_id, "xsec_token": xsec_token
        })


def load_config():
    config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.json")
    with open(config_path) as f:
        return json.load(f)


BLACKLIST = [
    "Telegram", "微信", "WeChat", "API", "MCP", "二维码",
    "加我", "私信", "关注我", "点进主页",
    "Binance", "币安", "SOL", "ETH", "加密货币", "合约",
    "收益", "回报", "盈利", "投资建议", "跟我做",
    "最", "第一", "100%", "绝对", "保证"
]

def check_sensitive(text):
    """Return list of blacklisted words found in text."""
    return [w for w in BLACKLIST if w.lower() in text.lower()]
