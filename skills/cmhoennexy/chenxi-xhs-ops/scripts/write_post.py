#!/usr/bin/env python3
"""Post writing prompt generator and content auditor."""
import sys
import os
import re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mcp_client import check_sensitive

WRITE_PROMPT = """你是一个小红书技术类内容创作者。请根据以下选题写一篇小红书帖子。

选题方向：{topic}

参考素材（如有）：
{reference}

写作要求：
1. 标题：20字以内，用数字/痛点/对比/好奇四选一
2. 正文结构：
   - 开门见山（1-2句）
   - 核心内容（2-4个要点，用📌/📊/🧠等 emoji 做序号）
   - 具体细节（数字、命令、真实案例）
   - 互动问句（结尾一句）
3. 话题标签：5-8个
4. 字数：500字以内

风格：接地气、直接、像程序员说话。能用数字就用数字。短句换行，移动端友好。

输出格式：
---标题---
（标题）
---正文---
（正文）
---标签---
（标签）"""


def get_write_prompt(topic, reference=""):
    return WRITE_PROMPT.format(topic=topic, reference=reference or "（无）")


def audit_post(title, body, tags=""):
    """Audit post content. Returns dict with passed, issues, stats."""
    full_text = f"{title} {body} {tags}"
    issues = []

    hits = check_sensitive(full_text)
    if hits:
        issues.append(f"❌ Sensitive words: {', '.join(hits)}")

    if len(title) > 20:
        issues.append(f"⚠️  Title too long: {len(title)} chars (max 20)")
    if len(body) > 600:
        issues.append(f"⚠️  Body too long: {len(body)} chars (target ≤500)")

    has_question = any(c in body[-100:] for c in "？?")
    if not has_question:
        issues.append("⚠️  No trailing question for engagement")

    has_numbers = bool(re.search(r'\d+', body))
    if not has_numbers:
        issues.append("⚠️  No specific numbers found")

    tag_list = [t.strip() for t in tags.replace("，", " ").replace(",", " ").split() if t.strip().startswith("#")]
    if len(tag_list) < 3:
        issues.append(f"⚠️  Too few tags: {len(tag_list)} (recommend 5-8)")

    passed = not any(i.startswith("❌") for i in issues)
    return {
        "passed": passed,
        "issues": issues,
        "stats": {
            "title_len": len(title), "body_len": len(body),
            "tag_count": len(tag_list), "has_question": has_question,
            "has_numbers": has_numbers
        }
    }


def format_audit_report(result):
    lines = ["📋 Audit Report:"]
    lines.append("✅ PASSED" if result["passed"] else "❌ FAILED")
    for issue in result["issues"]:
        lines.append(f"  {issue}")
    s = result["stats"]
    lines.append(f"\n📊 Title:{s['title_len']}ch | Body:{s['body_len']}ch | Tags:{s['tag_count']}")
    return "\n".join(lines)


def main():
    topic = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else ""
    if not topic:
        print("Usage: python3 write_post.py <topic>")
        print("Generates a writing prompt for LLM. Use audit_post() to validate output.")
        return
    print(get_write_prompt(topic))


if __name__ == "__main__":
    main()
