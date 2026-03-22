#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Command implementations for WeChat article skill."""

import json
import os
import urllib.parse
import urllib.request
from typing import Any, Dict, List, Optional

from api_client import BASE_URL, DEFAULT_TIMEOUT, extract_api_error, make_request
from formatters import (
    format_accounts_list,
    format_add_account,
    format_add_account_by_keyword,
    format_add_account_by_keyword_conflict,
    format_article_detail,
    format_article_detail_v2,
    format_articles_list,
    format_delete_account,
    format_login_qrcode,
    format_login_status_expired,
    format_login_status_success,
    format_login_status_waiting,
    format_local_accounts_list,
    format_sync_accounts_list,
    format_sync_result,
    format_sync_all_result,
)
from utils import failure, format_timestamp, success


def get_recent_articles(hours: int = 24, limit: int = 50) -> Dict[str, Any]:
    """Get recent articles from the sync service."""
    url = f"{BASE_URL}/sync?action=recent&hours={hours}&limit={limit}"
    response = make_request(url)

    error = extract_api_error(response, "Failed to get recent articles")
    if error:
        return error

    articles = response.get("data", {}).get("articles", [])
    formatted_articles: List[Dict[str, Any]] = []

    for article in articles:
        formatted_articles.append(
            {
                "aid": article.get("aid"),
                "title": article.get("title"),
                "link": article.get("link"),
                "digest": article.get("digest", ""),
                "create_time": article.get("create_time"),
                "create_time_formatted": format_timestamp(article.get("create_time")),
            }
        )

    return success(
        {
            "hours": hours,
            "total": len(formatted_articles),
            "articles": formatted_articles,
        },
        format_articles_list(formatted_articles),
    )


def list_accounts() -> Dict[str, Any]:
    """Return the locally added official account list."""
    url = f"{BASE_URL.replace('/public/v1', '')}/store/info?action=getAll"
    response = make_request(url, method="GET")

    if isinstance(response, dict) and response.get("success") is False:
        return failure(response.get("error", "Failed to get local accounts"))
    if not isinstance(response, list):
        return failure("Failed to get local accounts")

    accounts: List[Dict[str, Any]] = []
    for account in response:
        accounts.append(
            {
                "fakeid": account.get("fakeid"),
                "nickname": account.get("nickname"),
                "round_head_img": account.get("round_head_img"),
                "completed": account.get("completed", False),
                "count": account.get("count", 0),
                "articles": account.get("articles", 0),
                "total_count": account.get("total_count", 0),
                "create_time": account.get("create_time"),
                "create_time_formatted": format_timestamp(account.get("create_time")),
                "update_time": account.get("update_time"),
                "update_time_formatted": format_timestamp(account.get("update_time")),
                "last_update_time": account.get("last_update_time"),
                "last_update_time_formatted": format_timestamp(account.get("last_update_time")),
            }
        )

    return success(
        {
            "total": len(accounts),
            "accounts": accounts,
        },
        format_local_accounts_list(accounts),
    )


def list_sync_accounts() -> Dict[str, Any]:
    """Return the current sync-config account list."""
    url = f"{BASE_URL.replace('/public/v1', '')}/store/sync-config?action=getAll"
    response = make_request(url, method="GET")

    if isinstance(response, dict) and response.get("success") is False:
        return failure(response.get("error", "Failed to get sync accounts"))
    if not isinstance(response, list):
        return failure("Failed to get sync accounts")

    accounts: List[Dict[str, Any]] = []
    for account in response:
        sync_hour = account.get("syncHour", 8)
        sync_minute = account.get("syncMinute", 0)
        accounts.append(
            {
                "fakeid": account.get("fakeid"),
                "nickname": account.get("nickname"),
                "round_head_img": account.get("round_head_img"),
                "enabled": account.get("enabled", False),
                "sync_hour": sync_hour,
                "sync_minute": sync_minute,
                "sync_time": f"{int(sync_hour):02d}:{int(sync_minute):02d}",
                "last_sync_time": account.get("lastSyncTime"),
                "last_sync_time_formatted": format_timestamp(account.get("lastSyncTime")),
                "last_sync_status": account.get("lastSyncStatus", ""),
                "last_sync_message": account.get("lastSyncMessage", ""),
            }
        )

    return success(
        {
            "total": len(accounts),
            "accounts": accounts,
        },
        format_sync_accounts_list(accounts),
    )


def get_download_dir() -> str:
    """Get the download directory from environment variable or use default."""
    env_dir = os.environ.get("IMAGES_DOWNLOAD_DIR")
    if env_dir:
        return env_dir
    
    # Default path: ${HOME}/.openclaw/media/wechat-article-exporter
    home = os.environ.get("HOME") or os.environ.get("USERPROFILE") or ""
    if home:
        return os.path.join(home, ".openclaw", "media", "wechat-article-exporter")
    
    # Fallback to current directory
    return os.path.join(os.getcwd(), "downloads")


def sanitize_filename(filename: str) -> str:
    """Sanitize filename by removing invalid characters."""
    import re
    # Remove or replace invalid characters for filenames
    sanitized = re.sub(r'[<>:"/\\|?*]', '_', filename)
    # Limit length
    if len(sanitized) > 200:
        sanitized = sanitized[:200]
    return sanitized


def save_article_to_file(article: Dict[str, Any]) -> Dict[str, str]:
    """Save article content and metadata to local files.
    
    Returns:
        Dict with paths to saved files
    """
    download_dir = get_download_dir()
    articles_dir = os.path.join(download_dir, "articles")

    # Create directories if they don't exist
    os.makedirs(articles_dir, exist_ok=True)

    # Use aid as filename to avoid encoding issues
    aid = article.get("aid", "unknown")
    base_filename = aid

    saved_files = {}

    # Save the complete JSON response as-is
    json_path = os.path.join(articles_dir, f"{base_filename}.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(article, f, ensure_ascii=False, indent=2)
    saved_files["json"] = json_path

    return saved_files


def get_article_detail(aid: Optional[str] = None, link: Optional[str] = None, download_images: bool = False, save_local: bool = True) -> Dict[str, Any]:
    """Get article detail by aid or link.

    Args:
        aid: Article ID
        link: Article URL
        download_images: Whether to download article images
        save_local: Whether to save article content to local files (default: True)
    """
    if not aid and not link:
        return failure("Please provide either aid or link")

    if aid:
        url = f"{BASE_URL}/sync?action=article&aid={urllib.parse.quote(aid, safe='')}&downloadImages={'true' if download_images else 'false'}"
    else:
        url = f"{BASE_URL}/sync?action=article&link={urllib.parse.quote(link, safe='')}&downloadImages={'true' if download_images else 'false'}"

    article = make_request(url)
    if isinstance(article, dict) and article.get("success") is False:
        return failure(article.get("error", "Failed to get article detail"))

    # API 直接返回文章数据，检查必要字段
    if not article or not article.get("title"):
        return failure("Failed to get article detail")

    # Save to local files if enabled
    saved_files = {}
    if save_local:
        try:
            saved_files = save_article_to_file(article)
            article["saved_files"] = saved_files
            article["download_dir"] = get_download_dir()
        except Exception as e:
            article["save_error"] = str(e)

    # 直接返回文章数据（不再包装 success/data）
    return success(article, format_article_detail_v2(article))


def trigger_sync(fakeid: str) -> Dict[str, Any]:
    """Trigger article sync for a fakeid."""
    if not fakeid:
        return failure("Please provide fakeid")

    url = f"{BASE_URL}/sync?action=trigger"
    response = make_request(url, method="POST", data={"fakeid": fakeid})

    error = extract_api_error(response, "Failed to trigger sync")
    if error:
        return error

    return success(
        {
            "message": response.get("data", {}).get("message", "Sync task started"),
            "fakeid": fakeid,
        },
        format_sync_result(response.get("data", {}).get("message", "Sync task started"), fakeid),
    )


def trigger_sync_all() -> Dict[str, Any]:
    """Trigger article sync for all configured accounts."""
    # 首先获取所有已配置的公众号
    url = f"{BASE_URL}/sync?action=status"
    response = make_request(url)

    error = extract_api_error(response, "Failed to get account list")
    if error:
        return error

    accounts = response.get("data", {}).get("accounts", [])
    if not accounts:
        return success(
            {"message": "No accounts configured", "results": []},
            "No accounts configured for sync.",
        )

    # 逐个触发同步
    results = []
    success_count = 0
    failed_count = 0

    for account in accounts:
        fakeid = account.get("fakeid")
        if not fakeid:
            continue

        sync_url = f"{BASE_URL}/sync?action=trigger"
        sync_response = make_request(sync_url, method="POST", data={"fakeid": fakeid})

        if sync_response.get("success"):
            results.append({
                "fakeid": fakeid,
                "status": "success",
                "message": sync_response.get("data", {}).get("message", "Sync started"),
            })
            success_count += 1
        else:
            results.append({
                "fakeid": fakeid,
                "status": "failed",
                "message": sync_response.get("error", "Unknown error"),
            })
            failed_count += 1

    return success(
        {
            "total": len(accounts),
            "success": success_count,
            "failed": failed_count,
            "results": results,
        },
        format_sync_all_result(success_count, failed_count, len(accounts)),
    )


def _search_account_candidates(keyword: str, size: int = 20) -> Dict[str, Any]:
    """Search for candidate official accounts by keyword."""
    if not keyword:
        return failure("Please provide keyword")

    url = f"{BASE_URL.replace('/public/v1', '')}/web/mp/searchbiz?keyword={urllib.parse.quote(keyword)}&size={size}"
    response = make_request(url, method="GET")

    error = extract_api_error(response, "Failed to search account")
    if error:
        return error

    # Parse the response
    list_data = response.get("list", []) if isinstance(response, dict) else []

    formatted_accounts: List[Dict[str, Any]] = []
    for item in list_data:
        formatted_accounts.append({
            "fakeid": item.get("fakeid"),
            "nickname": item.get("nickname"),
            "alias": item.get("alias"),
            "round_head_img": item.get("round_head_img"),
            "service_type": item.get("service_type"),
        })

    return success(
        {
            "keyword": keyword,
            "total": len(formatted_accounts),
            "accounts": formatted_accounts,
        }
    )


def _normalize_match_value(value: Any) -> str:
    """Normalize account values for matching."""
    return str(value or "").strip().casefold()


def _resolve_account_by_keyword(keyword: str, accounts: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Resolve a single account from search results."""
    normalized_keyword = _normalize_match_value(keyword)
    exact_matches: List[Dict[str, Any]] = []
    seen_fakeids = set()

    for account in accounts:
        fakeid = account.get("fakeid")
        nickname_matches = _normalize_match_value(account.get("nickname")) == normalized_keyword
        alias_matches = _normalize_match_value(account.get("alias")) == normalized_keyword

        if (nickname_matches or alias_matches) and fakeid not in seen_fakeids:
            matched_account = dict(account)
            matched_account["match_type"] = "exact_nickname" if nickname_matches else "exact_alias"
            exact_matches.append(matched_account)
            seen_fakeids.add(fakeid)

    if len(exact_matches) == 1:
        return {
            "matched": True,
            "account": exact_matches[0],
            "match_type": exact_matches[0]["match_type"],
        }

    if len(exact_matches) > 1:
        return {
            "matched": False,
            "reason": "ambiguous_exact_match",
            "accounts": exact_matches,
        }

    if len(accounts) == 1:
        single_account = dict(accounts[0])
        single_account["match_type"] = "single_result"
        return {
            "matched": True,
            "account": single_account,
            "match_type": "single_result",
        }

    return {
        "matched": False,
        "reason": "ambiguous_search_results",
        "accounts": accounts,
    }


def search_account(keyword: str) -> Dict[str, Any]:
    """Search for a WeChat official account by keyword."""
    search_result = _search_account_candidates(keyword)
    if not search_result.get("success"):
        return search_result

    formatted_accounts = search_result.get("data", {}).get("accounts", [])
    formatted_text = format_accounts_list(keyword, formatted_accounts)

    return success(
        {
            "keyword": keyword,
            "total": len(formatted_accounts),
            "accounts": formatted_accounts,
        },
        formatted_text,
    )


def add_account_by_keyword(keyword: str) -> Dict[str, Any]:
    """Search and add an official account by keyword."""
    if not keyword:
        return failure("Please provide keyword")

    search_result = _search_account_candidates(keyword)
    if not search_result.get("success"):
        return search_result

    accounts = search_result.get("data", {}).get("accounts", [])
    if not accounts:
        return failure(
            f"No accounts found for keyword '{keyword}'",
            {
                "keyword": keyword,
                "total": 0,
                "accounts": [],
            },
        )

    resolve_result = _resolve_account_by_keyword(keyword, accounts)
    if not resolve_result.get("matched"):
        candidate_accounts = resolve_result.get("accounts", accounts)
        return failure(
            format_add_account_by_keyword_conflict(keyword, candidate_accounts),
            {
                "keyword": keyword,
                "total": len(candidate_accounts),
                "accounts": candidate_accounts,
                "reason": resolve_result.get("reason"),
            },
        )

    matched_account = resolve_result["account"]
    match_type = resolve_result["match_type"]
    add_result = add_account(
        matched_account.get("fakeid", ""),
        matched_account.get("nickname", ""),
        matched_account.get("round_head_img", ""),
    )
    if not add_result.get("success"):
        return add_result

    sync_result = add_result.get("data", {}).get("sync", {})
    sync_success = add_result.get("data", {}).get("sync_success", False)
    sync_error = add_result.get("data", {}).get("sync_error", "")

    return success(
        {
            "keyword": keyword,
            "fakeid": matched_account.get("fakeid"),
            "nickname": matched_account.get("nickname"),
            "match_type": match_type,
            "matched_account": matched_account,
            "sync": sync_result,
            "sync_success": sync_success,
            "sync_error": sync_error,
        },
        format_add_account_by_keyword(
            keyword,
            matched_account,
            match_type,
            sync_success,
            sync_error,
        ),
    )


def add_account(fakeid: str, nickname: str, avatar: str = "") -> Dict[str, Any]:
    """Add a WeChat official account via the store API."""
    if not fakeid:
        return failure("Please provide fakeid")
    if not nickname:
        return failure("Please provide nickname")

    # Use the store info API to add account
    url = f"{BASE_URL.replace('/public/v1', '')}/store/info"
    data = {
        "action": "upsert",
        "data": {
            "fakeid": fakeid,
            "nickname": nickname,
            "round_head_img": avatar,
            "completed": False,
            "count": 0,
            "articles": 0,
            "total_count": 0
        }
    }

    response = make_request(url, method="POST", data=data)

    # Check response - make_request returns the parsed JSON directly or a failure dict
    if isinstance(response, dict) and response.get("success") is False:
        return failure(response.get("error", "Failed to add account"))

    # Also trigger first page sync
    sync_result = trigger_sync(fakeid)

    formatted_text = format_add_account(
        fakeid,
        nickname,
        sync_result.get("success", False),
        sync_result.get("error", "unknown")
    )

    return success(
        {
            "fakeid": fakeid,
            "nickname": nickname,
            "sync": sync_result.get("data", {}),
            "sync_success": sync_result.get("success", False),
            "sync_error": sync_result.get("error", ""),
        },
        formatted_text,
    )


def delete_account(fakeid: str = "", nickname: str = "") -> Dict[str, Any]:
    """Delete a WeChat official account and all its data."""
    if not fakeid and not nickname:
        return failure("Please provide fakeid or nickname")

    # Use the public API to delete account
    url = f"{BASE_URL}/sync?action=account"
    data = {}
    if fakeid:
        data["fakeid"] = fakeid
    if nickname:
        data["nickname"] = nickname

    response = make_request(url, method="DELETE", data=data)

    # Check response
    if isinstance(response, dict) and response.get("success") is False:
        return failure(response.get("error", "Failed to delete account"))

    deleted_fakeid = response.get("data", {}).get("fakeid", fakeid or nickname)
    formatted_text = format_delete_account(deleted_fakeid)

    return success(
        {
            "fakeid": deleted_fakeid,
            "nickname": nickname if nickname else None,
            "message": "Account deleted successfully",
        },
        formatted_text,
    )


def get_login_qrcode(save_path: str = "") -> Dict[str, Any]:
    """Get login QR code for WeChat official account.

    Args:
        save_path: Path to save the QR code image. If empty, uses default path.
    """
    url = f"{BASE_URL}/login?action=qrcode"
    response = make_request(url, method="GET")

    error = extract_api_error(response, "Failed to get login QR code")
    if error:
        return error

    data = response.get("data", {})
    sid = data.get("sid")

    # Build web UI URL
    base_url = BASE_URL.replace('/api/public/v1', '')
    web_ui_url = base_url

    formatted_text = format_login_qrcode(sid, web_ui_url)

    return success(
        {
            "sid": sid,
            "webUiUrl": web_ui_url,
            "message": data.get("message", "Please use Web UI to login"),
        },
        formatted_text,
    )


def check_login_status(sid: str) -> Dict[str, Any]:
    """Check login status for a given session ID."""
    if not sid:
        return failure("Please provide session ID (sid)")

    url = f"{BASE_URL}/login?action=status&sid={sid}"
    response = make_request(url, method="GET")

    error = extract_api_error(response, "Failed to check login status")
    if error:
        return error

    data = response.get("data", {})
    status = data.get("status")
    status_text = data.get("statusText", "Unknown")

    if status == 1:
        # Login successful
        formatted_text = format_login_status_success(sid, data.get("nickname", "N/A"))

        return success(
            {
                "status": status,
                "statusText": status_text,
                "sid": sid,
                "nickname": data.get("nickname"),
                "token": data.get("token"),
                "loggedIn": True,
            },
            formatted_text,
        )
    elif data.get("needRefresh"):
        formatted_text = format_login_status_expired(status_text)

        return success(
            {
                "status": status,
                "statusText": status_text,
                "sid": sid,
                "needRefresh": True,
                "loggedIn": False,
            },
            formatted_text,
        )
    else:
        formatted_text = format_login_status_waiting(sid, status_text)

        return success(
            {
                "status": status,
                "statusText": status_text,
                "sid": sid,
                "loggedIn": False,
            },
            formatted_text,
        )


def get_login_info() -> Dict[str, Any]:
    """Get current login status information."""
    url = f"{BASE_URL}/login?action=info"
    response = make_request(url, method="GET")

    error = extract_api_error(response, "Failed to get login info")
    if error:
        return error

    data = response.get("data", {})
    logged_in = data.get("loggedIn", False)

    if logged_in:
        formatted_text = f"Login Status: Logged in\n"
        formatted_text += f"Nickname: {data.get('nickname', 'N/A')}\n"
        formatted_text += f"Auth Key: {data.get('authKey', 'N/A')}"

        return success(
            {
                "loggedIn": True,
                "nickname": data.get("nickname"),
                "authKey": data.get("authKey"),
                "message": data.get("message", "已登录"),
            },
            formatted_text,
        )
    else:
        formatted_text = f"Login Status: Not logged in\n"
        formatted_text += f"Message: {data.get('message', '请先扫码登录')}"

        return success(
            {
                "loggedIn": False,
                "message": data.get("message", "请先扫码登录"),
            },
            formatted_text,
        )


def get_sync_logs(fakeid: str = "", limit: int = 50) -> Dict[str, Any]:
    """Get sync task logs.

    Args:
        fakeid: Filter by specific fakeid (optional)
        limit: Maximum number of logs to return (default: 50)
    """
    url = f"{BASE_URL}/sync-logs?limit={limit}"
    if fakeid:
        url += f"&fakeid={urllib.parse.quote(fakeid, safe='')}"

    response = make_request(url, method="GET")

    error = extract_api_error(response, "Failed to get sync logs")
    if error:
        return error

    data = response.get("data", {})
    logs = data.get("logs", [])
    total = data.get("total", 0)

    # Format the logs for display
    formatted_logs = []
    for log in logs:
        formatted_logs.append({
            "id": log.get("id"),
            "fakeid": log.get("fakeid"),
            "nickname": log.get("nickname"),
            "status": log.get("status"),
            "message": log.get("message"),
            "articlesSynced": log.get("articlesSynced"),
            "createTime": log.get("createTime"),
            "createTimeFormatted": log.get("createTimeFormatted"),
        })

    formatted_text = f"Sync logs (total {total})\n"
    formatted_text += "=" * 60 + "\n\n"

    if not formatted_logs:
        formatted_text += "No sync logs found.\n"
    else:
        for log in formatted_logs:
            formatted_text += f"[{log.get('id')}] {log.get('createTimeFormatted')}\n"
            formatted_text += f"   Account: {log.get('nickname')} ({log.get('fakeid')})\n"
            formatted_text += f"   Status: {log.get('status')}\n"
            formatted_text += f"   Message: {log.get('message')}\n"
            formatted_text += f"   Articles Synced: {log.get('articlesSynced', 0)}\n"
            formatted_text += "-" * 60 + "\n"

    return success(
        {
            "total": total,
            "logs": formatted_logs,
        },
        formatted_text,
    )

    # Build formatted text
    formatted_text = f"同步任务日志 (共 {total} 条)\n"
    formatted_text += "=" * 60 + "\n\n"

    if not formatted_logs:
        formatted_text += "暂无同步记录\n"
    else:
        for log in formatted_logs:
            status_emoji = {
                "success": "✅",
                "failed": "❌",
                "running": "⏳",
            }.get(log.get("status", ""), "❓")

            formatted_text += f"{status_emoji} [{log.get('id')}] {log.get('createTimeFormatted')}\n"
            formatted_text += f"   公众号: {log.get('nickname')} ({log.get('fakeid')})\n"
            formatted_text += f"   状态: {log.get('status')}\n"
            formatted_text += f"   消息: {log.get('message')}\n"
            formatted_text += f"   同步文章数: {log.get('articlesSynced', 0)}\n"
            formatted_text += "-" * 60 + "\n"

    return success(
        {
            "total": total,
            "logs": formatted_logs,
        },
        formatted_text,
    )
