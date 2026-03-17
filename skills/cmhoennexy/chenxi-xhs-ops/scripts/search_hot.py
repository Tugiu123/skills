#!/usr/bin/env python3
"""Search Xiaohongshu for trending posts by keyword."""
import sys
import os
import json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mcp_client import MCPClient, load_config

RESULTS_PATH = "/tmp/xhs-search-results.json"


def search_hot(keywords=None, top_n=10):
    config = load_config()
    keywords = keywords or config.get("keywords", [])
    mcp = MCPClient(config.get("mcp_url"))
    mcp.initialize()

    all_feeds = []
    seen_ids = set()

    for kw in keywords:
        try:
            result = mcp.search_feeds(kw, sort_by="最多点赞", note_type="图文")
            feeds = result.get("feeds", []) if isinstance(result, dict) else []
            for feed in feeds:
                fid = feed.get("id")
                if fid and fid not in seen_ids:
                    seen_ids.add(fid)
                    note = feed.get("noteCard", {})
                    user = note.get("user", {})
                    interact = note.get("interactInfo", {})
                    all_feeds.append({
                        "id": fid,
                        "xsec_token": feed.get("xsecToken", ""),
                        "title": note.get("displayTitle", "无标题"),
                        "author": user.get("nickname", "未知"),
                        "likes": int(interact.get("likedCount", "0") or "0"),
                        "collects": int(interact.get("collectedCount", "0") or "0"),
                        "comments": int(interact.get("commentCount", "0") or "0"),
                        "keyword": kw,
                    })
        except Exception as e:
            print(f"⚠️  Keyword '{kw}' search failed: {e}")

    all_feeds.sort(key=lambda x: x["likes"], reverse=True)
    return all_feeds[:top_n]


def format_output(feeds):
    if not feeds:
        return "❌ No results. Check keywords or MCP status."
    lines = [f"🔥 Top {len(feeds)} trending posts:\n"]
    for i, f in enumerate(feeds, 1):
        lines.append(
            f"{i}. [{f['author']}] {f['title']}\n"
            f"   👍{f['likes']} ⭐{f['collects']} 💬{f['comments']} | kw: {f['keyword']}\n"
        )
    return "\n".join(lines)


def main():
    keywords = sys.argv[1:] if len(sys.argv) > 1 else None
    feeds = search_hot(keywords)
    print(format_output(feeds))
    with open(RESULTS_PATH, "w") as f:
        json.dump(feeds, f, ensure_ascii=False, indent=2)
    print(f"💾 Results saved: {RESULTS_PATH}")


if __name__ == "__main__":
    main()
