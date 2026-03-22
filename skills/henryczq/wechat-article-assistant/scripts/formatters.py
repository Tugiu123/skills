#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Formatters for WeChat article skill output."""

from typing import Any, Dict, List


def format_articles_list(articles: List[Dict[str, Any]]) -> str:
    """Format a list of articles for display."""
    if not articles:
        return "No articles found."

    lines = [f"Found {len(articles)} articles:", ""]
    for index, article in enumerate(articles, 1):
        lines.append(f"{index}. {article.get('title', 'No title')}")
        lines.append(f"   ID: {article.get('aid', 'N/A')}")
        lines.append(f"   Time: {article.get('create_time_formatted', 'N/A')}")
        if article.get("link"):
            lines.append(f"   Link: {article['link']}")
        digest = (article.get("digest") or "").strip()
        if digest:
            if len(digest) > 100:
                digest = f"{digest[:100]}..."
            lines.append(f"   Summary: {digest}")
        lines.append("")
    return "\n".join(lines).rstrip()


def format_article_detail(article: Dict[str, Any]) -> str:
    """Format a single article detail for display."""
    if not article:
        return "Article not found."

    lines = [
        f"Title: {article.get('title', 'No title')}",
        f"Author: {article.get('author_name', 'N/A')}",
        f"Published: {article.get('create_time_formatted', 'N/A')}",
        f"Article ID: {article.get('aid', 'N/A')}",
        f"Link: {article.get('link', 'N/A')}",
    ]

    digest = article.get("digest")
    if digest:
        lines.append(f"Summary: {digest}")

    lines.append("")

    if article.get("hasContent") and article.get("content"):
        lines.append("--- Content ---")
        lines.append("")
        lines.append(article["content"])
    else:
        lines.append("(Article content not available)")

    return "\n".join(lines)


def format_sync_result(message: str, fakeid: str) -> str:
    """Format a sync result message."""
    return f"{message}\nFakeid: {fakeid}"


def format_login_qrcode(sid: str, web_ui_url: str) -> str:
    """Format login QR code information."""
    formatted_text = f"Login Session Created.\nSession ID: {sid}\n\n"
    formatted_text += f"Please open the following URL in your browser:\n"
    formatted_text += f"  {web_ui_url}\n\n"
    formatted_text += "Then click 'Login' button and scan the QR code with WeChat.\n"
    formatted_text += f"After scanning, check status with:\n"
    formatted_text += f"  python3 scripts/wechat_article_skill.py login-status --sid {sid}"
    return formatted_text


def format_login_status_waiting(sid: str, status_text: str) -> str:
    """Format login status when waiting."""
    formatted_text = f"Login status: {status_text}\n"
    formatted_text += f"Session ID: {sid}\n\n"
    formatted_text += f"Check again with: python3 scripts/wechat_article_skill.py login-status --sid {sid}"
    return formatted_text


def format_login_status_success(sid: str, nickname: str) -> str:
    """Format login status when successful."""
    formatted_text = f"Login successful!\n"
    formatted_text += f"Nickname: {nickname}\n"
    formatted_text += f"Session ID: {sid}"
    return formatted_text


def format_login_status_expired(status_text: str) -> str:
    """Format login status when QR code expired."""
    return f"QR code expired. Please generate a new one.\nStatus: {status_text}"


def format_accounts_list(keyword: str, accounts: List[Dict[str, Any]]) -> str:
    """Format a list of accounts for display."""
    formatted_text = f"Found {len(accounts)} accounts for keyword '{keyword}':\n\n"
    for idx, acc in enumerate(accounts, 1):
        formatted_text += f"{idx}. {acc['nickname']}\n"
        formatted_text += f"   FakeID: {acc['fakeid']}\n"
        if acc.get('alias'):
            formatted_text += f"   Alias: {acc['alias']}\n"
        formatted_text += "\n"
    return formatted_text


def format_local_accounts_list(accounts: List[Dict[str, Any]]) -> str:
    """Format the locally added account list for display."""
    if not accounts:
        return "No local accounts found."

    lines = [f"Found {len(accounts)} local accounts:", ""]
    for index, account in enumerate(accounts, 1):
        lines.append(f"{index}. {account.get('nickname') or 'Unnamed account'}")
        lines.append(f"   FakeID: {account.get('fakeid', 'N/A')}")
        lines.append(f"   Completed: {account.get('completed', False)}")
        lines.append(f"   New Count: {account.get('count', 0)}")
        lines.append(f"   Synced Articles: {account.get('articles', 0)}")
        lines.append(f"   Total Count: {account.get('total_count', 0)}")
        if account.get("update_time_formatted"):
            lines.append(f"   Updated: {account['update_time_formatted']}")
        if account.get("last_update_time_formatted"):
            lines.append(f"   Last Fetch: {account['last_update_time_formatted']}")
        lines.append("")
    return "\n".join(lines).rstrip()


def format_sync_accounts_list(accounts: List[Dict[str, Any]]) -> str:
    """Format the sync-config account list for display."""
    if not accounts:
        return "No sync accounts configured."

    lines = [f"Found {len(accounts)} sync accounts:", ""]
    for index, account in enumerate(accounts, 1):
        lines.append(f"{index}. {account.get('nickname') or 'Unnamed account'}")
        lines.append(f"   FakeID: {account.get('fakeid', 'N/A')}")
        lines.append(f"   Enabled: {account.get('enabled', False)}")
        lines.append(f"   Sync Time: {account.get('sync_time', 'N/A')}")
        if account.get("last_sync_time_formatted"):
            lines.append(f"   Last Sync Time: {account['last_sync_time_formatted']}")
        if account.get("last_sync_status"):
            lines.append(f"   Last Sync Status: {account['last_sync_status']}")
        if account.get("last_sync_message"):
            lines.append(f"   Last Sync Message: {account['last_sync_message']}")
        lines.append("")
    return "\n".join(lines).rstrip()


def format_add_account(fakeid: str, nickname: str, sync_success: bool, sync_error: str = "") -> str:
    """Format add account result."""
    formatted_text = f"Added account: {nickname} ({fakeid})\n"
    if sync_success:
        formatted_text += "First page sync triggered."
    else:
        formatted_text += f"Sync warning: {sync_error}"
    return formatted_text


def format_add_account_by_keyword(
    keyword: str,
    account: Dict[str, Any],
    match_type: str,
    sync_success: bool,
    sync_error: str = "",
) -> str:
    """Format add-account-by-keyword result."""
    match_type_label = {
        "exact_nickname": "exact nickname",
        "exact_alias": "exact alias",
        "single_result": "single search result",
    }.get(match_type, match_type)

    lines = [
        f"Resolved keyword: {keyword}",
        f"Matched account: {account.get('nickname', 'Unknown')} ({account.get('fakeid', 'N/A')})",
        f"Match type: {match_type_label}",
    ]

    if sync_success:
        lines.append("First page sync triggered.")
    else:
        lines.append(f"Sync warning: {sync_error}")

    return "\n".join(lines)


def format_add_account_by_keyword_conflict(keyword: str, accounts: List[Dict[str, Any]]) -> str:
    """Format the ambiguity result for add-account-by-keyword."""
    lines = [
        f"Found multiple accounts for keyword '{keyword}', and no unique exact match was found.",
        "Please refine the keyword or use addAccount with fakeid directly.",
        "",
        "Candidates:",
    ]

    for index, account in enumerate(accounts, 1):
        lines.append(f"{index}. {account.get('nickname', 'Unknown')}")
        lines.append(f"   FakeID: {account.get('fakeid', 'N/A')}")
        alias = account.get("alias")
        if alias:
            lines.append(f"   Alias: {alias}")
        lines.append("")

    return "\n".join(lines).rstrip()


def format_delete_account(fakeid: str) -> str:
    """Format delete account result."""
    return f"Deleted account: {fakeid}\nAll data has been removed."


def format_article_detail_v2(article: Dict[str, Any]) -> str:
    """Format article detail in new format for display."""
    if not article:
        return "Article not found."

    lines = [
        f"Title: {article.get('title', 'No title')}",
        f"Source: {article.get('source_url', 'N/A')}",
        f"Created: {article.get('created_at', 'N/A')}",
        f"Note: {article.get('note', '')}",
    ]

    images = article.get('images', [])
    if images:
        lines.append(f"Images ({len(images)}):")
        for img in images:
            lines.append(f"  - {img}")

    lines.append("")
    lines.append("--- Content (Markdown) ---")
    lines.append("")

    content = article.get('content', '')
    if content:
        # 显示 HTML 内容的前 500 字符，避免过长
        preview = content[:500] if len(content) > 500 else content
        lines.append(preview)
        if len(content) > 500:
            lines.append(f"\n... (Content truncated, total length: {len(content)} chars)")
    else:
        lines.append("(Article content not available)")

    return "\n".join(lines)


def format_sync_all_result(success_count: int, failed_count: int, total: int) -> str:
    """Format sync all accounts result."""
    lines = [
        f"同步全部公众号完成",
        f"总计: {total} 个公众号",
        f"成功: {success_count} 个",
        f"失败: {failed_count} 个",
    ]
    return "\n".join(lines)
