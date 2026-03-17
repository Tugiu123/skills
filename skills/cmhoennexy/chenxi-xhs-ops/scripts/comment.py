#!/usr/bin/env python3
"""Automated commenting on Xiaohongshu posts."""
import sys
import os
import json
import time
import random
import argparse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mcp_client import MCPClient, load_config, check_sensitive

RESULTS_PATH = "/tmp/xhs-search-results.json"


def load_search_results():
    if not os.path.exists(RESULTS_PATH):
        return None
    with open(RESULTS_PATH) as f:
        return json.load(f)


def generate_comment_prompt(title, detail_text=""):
    return f"""Write a comment for this Xiaohongshu post.

Title: {title}
Summary: {detail_text[:500] if detail_text else '(none)'}

Rules:
- Add a real opinion or experience not mentioned in the post
- Include specific details, no fluff
- No ads, no account mentions, no follow solicitation
- 50-120 characters
- No sensitive words: Telegram, 微信, WeChat, API, MCP, Binance, 币安, SOL, ETH

Output the comment only, no prefix or explanation."""


def post_single_comment(feed_id, xsec_token, comment_text, mcp_url=None):
    """Post a single comment. Returns status dict."""
    hits = check_sensitive(comment_text)
    if hits:
        return {"status": "blocked", "reason": f"Sensitive words: {', '.join(hits)}"}
    config = load_config()
    mcp = MCPClient(mcp_url or config.get("mcp_url"))
    mcp.initialize()
    result = mcp.post_comment(feed_id, xsec_token, comment_text)
    return {"status": "ok", "result": result}


def run_comments(dry_run=False, count=10):
    config = load_config()
    feeds = load_search_results()
    if not feeds:
        print("⚠️  No search results. Run search_hot.py first.")
        return []

    feeds = feeds[:count]
    results = []
    interval_min = config.get("comment_interval_min", 180)
    interval_max = config.get("comment_interval_max", 480)

    for i, feed in enumerate(feeds):
        title = feed.get("title", "")
        feed_id = feed.get("id", "")
        print(f"\n📝 [{i+1}/{len(feeds)}] {title}")

        prompt = generate_comment_prompt(title)

        if dry_run:
            print(f"   [DRY RUN] Prompt generated")
            results.append({"feed_id": feed_id, "title": title, "status": "dry_run", "prompt": prompt})
        else:
            print(f"   ⚠️  Actual posting requires Agent (LLM generates comment → post_single_comment)")
            results.append({
                "feed_id": feed_id, "xsec_token": feed.get("xsec_token", ""),
                "title": title, "status": "pending", "prompt": prompt
            })

        if not dry_run and i < len(feeds) - 1:
            wait = random.randint(interval_min, interval_max)
            print(f"   ⏳ Waiting {wait}s...")
            time.sleep(wait)

    print(f"\n{'='*40}\n📊 Done: {len(results)} posts processed")
    return results


def main():
    parser = argparse.ArgumentParser(description="XHS auto-comment")
    parser.add_argument("--dry-run", action="store_true", help="Generate prompts only")
    parser.add_argument("--count", type=int, default=10, help="Number of comments")
    args = parser.parse_args()
    run_comments(dry_run=args.dry_run, count=args.count)


if __name__ == "__main__":
    main()
