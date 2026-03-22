#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CLI argument parsing and main entry point for WeChat article skill."""

import argparse
import json
import sys
from typing import Any, Dict, List

from commands import (
    add_account,
    add_account_by_keyword,
    check_login_status,
    delete_account,
    get_article_detail,
    get_login_info,
    get_login_qrcode,
    get_recent_articles,
    get_sync_logs,
    list_accounts,
    list_sync_accounts,
    search_account,
    trigger_sync,
    trigger_sync_all,
)
from utils import failure, parse_input, validate_positive_int


def configure_stdio() -> None:
    """Prefer UTF-8 stdio so JSON output works reliably on Windows consoles."""
    for stream_name in ("stdin", "stdout", "stderr"):
        stream = getattr(sys, stream_name, None)
        if stream is not None and hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")


def build_parser() -> argparse.ArgumentParser:
    """Build the argument parser for CLI."""
    parser = argparse.ArgumentParser(
        description="Fetch WeChat official-account articles from the local sync service."
    )
    output_parent = argparse.ArgumentParser(add_help=False)
    output_parent.add_argument("--json", action="store_true", help="Output raw JSON instead of text")

    subparsers = parser.add_subparsers(dest="command")

    # recent command
    recent_parser = subparsers.add_parser(
        "recent",
        parents=[output_parent],
        help="Fetch recent articles",
    )
    recent_parser.add_argument("--hours", type=int, default=24, help="Time window in hours")
    recent_parser.add_argument("--limit", type=int, default=50, help="Max article count")

    subparsers.add_parser(
        "list-accounts",
        parents=[output_parent],
        help="List locally added official accounts",
    )

    subparsers.add_parser(
        "list-sync-accounts",
        parents=[output_parent],
        help="List current sync-config accounts",
    )

    # article command
    article_parser = subparsers.add_parser(
        "article",
        parents=[output_parent],
        help="Fetch article details by aid or link",
    )
    article_group = article_parser.add_mutually_exclusive_group(required=True)
    article_group.add_argument("--aid", help="Article aid")
    article_group.add_argument("--link", help="Article URL")
    article_parser.add_argument("--download-images", action="store_true", help="Download article images")
    article_parser.add_argument("--no-save", action="store_true", help="Do not save article content to local files")

    # sync command
    sync_parser = subparsers.add_parser(
        "sync",
        parents=[output_parent],
        help="Trigger article sync for a fakeid",
    )
    sync_parser.add_argument("--fakeid", required=True, help="WeChat official-account fakeid")

    # sync-all command
    subparsers.add_parser(
        "sync-all",
        parents=[output_parent],
        help="Trigger article sync for all configured accounts",
    )

    # add-account command
    add_parser = subparsers.add_parser(
        "add-account",
        parents=[output_parent],
        help="Add a WeChat official account",
    )
    add_parser.add_argument("--fakeid", required=True, help="WeChat official-account fakeid")
    add_parser.add_argument("--nickname", required=True, help="Account nickname")
    add_parser.add_argument("--avatar", default="", help="Account avatar URL (optional)")

    add_by_keyword_parser = subparsers.add_parser(
        "add-account-by-keyword",
        parents=[output_parent],
        help="Search and add a WeChat official account by keyword",
    )
    add_by_keyword_parser.add_argument("keyword", help="Keyword or exact account name")

    # search command
    search_parser = subparsers.add_parser(
        "search",
        parents=[output_parent],
        help="Search for a WeChat official account by keyword",
    )
    search_parser.add_argument("keyword", help="Search keyword (account name)")
    search_parser.add_argument("--limit", type=int, default=10, help="Max results to return")

    # delete command
    delete_parser = subparsers.add_parser(
        "delete",
        parents=[output_parent],
        help="Delete a WeChat official account and all its data",
    )
    delete_group = delete_parser.add_mutually_exclusive_group(required=True)
    delete_group.add_argument("--fakeid", help="WeChat official-account fakeid to delete")
    delete_group.add_argument("--nickname", help="WeChat official-account nickname to delete")

    # login command
    subparsers.add_parser(
        "login",
        parents=[output_parent],
        help="Get login QR code for WeChat official account",
    )

    # login-status command
    login_status_parser = subparsers.add_parser(
        "login-status",
        parents=[output_parent],
        help="Check login status",
    )
    login_status_parser.add_argument("--sid", required=True, help="Session ID from login command")

    # login-info command
    subparsers.add_parser(
        "login-info",
        parents=[output_parent],
        help="Get current login information",
    )

    # sync-logs command
    sync_logs_parser = subparsers.add_parser(
        "sync-logs",
        parents=[output_parent],
        help="Get sync task logs",
    )
    sync_logs_parser.add_argument("--fakeid", default="", help="Filter by specific fakeid (optional)")
    sync_logs_parser.add_argument("--limit", type=int, default=50, help="Max logs to return (default: 50)")

    return parser


def dispatch_request(tool_name: str, params: Dict[str, Any]) -> Dict[str, Any]:
    """Dispatch a request to the appropriate command handler."""
    if tool_name == "getRecentArticles":
        hours = params.get("hours", 24)
        limit = params.get("limit", 50)

        hours, error = validate_positive_int(hours, "hours")
        if error:
            return error

        limit, error = validate_positive_int(limit, "limit")
        if error:
            return error

        return get_recent_articles(hours, limit)

    if tool_name == "listAccounts":
        return list_accounts()

    if tool_name == "listSyncAccounts":
        return list_sync_accounts()

    if tool_name == "getArticleDetail":
        return get_article_detail(
            params.get("aid"),
            params.get("link"),
            params.get("download_images", False),
            params.get("save_local", True),
        )

    if tool_name == "triggerSync":
        return trigger_sync(params.get("fakeid"))

    if tool_name == "triggerSyncAll":
        return trigger_sync_all()

    if tool_name == "addAccount":
        return add_account(
            params.get("fakeid", ""),
            params.get("nickname", ""),
            params.get("avatar", ""),
        )

    if tool_name == "addAccountByKeyword":
        return add_account_by_keyword(params.get("keyword", ""))

    if tool_name == "searchAccount":
        return search_account(params.get("keyword", ""))

    if tool_name == "deleteAccount":
        return delete_account(
            params.get("fakeid", ""),
            params.get("nickname", ""),
        )

    if tool_name == "getLoginQrcode":
        return get_login_qrcode()

    if tool_name == "checkLoginStatus":
        return check_login_status(params.get("sid", ""))

    if tool_name == "getLoginInfo":
        return get_login_info()

    if tool_name == "getSyncLogs":
        return get_sync_logs(
            params.get("fakeid", ""),
            params.get("limit", 50),
        )

    return failure(f"Unknown tool: {tool_name}")


def run_json_mode() -> int:
    """Run in JSON mode (reading from stdin)."""
    input_data, error = parse_input()
    if error:
        print(json.dumps(error, ensure_ascii=False))
        return 1

    tool_name = input_data.get("tool")
    params = input_data.get("params", {})
    if not isinstance(params, dict):
        print(json.dumps(failure("params must be a JSON object"), ensure_ascii=False))
        return 1

    result = dispatch_request(tool_name, params)
    print(json.dumps(result, ensure_ascii=False))
    return 0 if result.get("success") else 1


def run_cli_mode(argv: List[str]) -> int:
    """Run in CLI mode (parsing arguments)."""
    parser = build_parser()
    args = parser.parse_args(argv)

    if not args.command:
        parser.print_help(sys.stderr)
        return 1

    result: Dict[str, Any] = {}
    output_json: bool = False

    if args.command == "recent":
        result = dispatch_request(
            "getRecentArticles",
            {"hours": args.hours, "limit": args.limit},
        )
        output_json = args.json
    elif args.command == "list-accounts":
        result = dispatch_request("listAccounts", {})
        output_json = args.json
    elif args.command == "list-sync-accounts":
        result = dispatch_request("listSyncAccounts", {})
        output_json = args.json
    elif args.command == "article":
        result = dispatch_request(
            "getArticleDetail",
            {
                "aid": getattr(args, "aid", None),
                "link": getattr(args, "link", None),
                "download_images": getattr(args, "download_images", False),
                "save_local": not getattr(args, "no_save", False),
            },
        )
        output_json = args.json
    elif args.command == "add-account":
        result = dispatch_request(
            "addAccount",
            {
                "fakeid": args.fakeid,
                "nickname": args.nickname,
                "avatar": args.avatar,
            },
        )
        output_json = args.json
    elif args.command == "search":
        result = dispatch_request(
            "searchAccount",
            {"keyword": args.keyword},
        )
        output_json = args.json
    elif args.command == "add-account-by-keyword":
        result = dispatch_request(
            "addAccountByKeyword",
            {"keyword": args.keyword},
        )
        output_json = args.json
    elif args.command == "delete":
        result = dispatch_request(
            "deleteAccount",
            {
                "fakeid": getattr(args, "fakeid", None),
                "nickname": getattr(args, "nickname", None),
            },
        )
        output_json = args.json
    elif args.command == "login":
        result = dispatch_request("getLoginQrcode", {})
        output_json = args.json
    elif args.command == "login-status":
        result = dispatch_request(
            "checkLoginStatus",
            {"sid": args.sid},
        )
        output_json = args.json
    elif args.command == "login-info":
        result = dispatch_request("getLoginInfo", {})
        output_json = args.json
    elif args.command == "sync-logs":
        result = dispatch_request(
            "getSyncLogs",
            {"fakeid": args.fakeid, "limit": args.limit},
        )
        output_json = args.json
    elif args.command == "sync-all":
        result = dispatch_request("triggerSyncAll", {})
        output_json = args.json
    elif args.command == "sync":
        result = dispatch_request(
            "triggerSync",
            {"fakeid": args.fakeid},
        )
        output_json = args.json
    else:
        parser.print_help(sys.stderr)
        return 1

    if output_json:
        print(json.dumps(result, ensure_ascii=False))
    elif result.get("success"):
        print(result.get("formatted_text") or json.dumps(result.get("data", {}), ensure_ascii=False, indent=2))
    else:
        print(result.get("error", "Unknown error"), file=sys.stderr)

    return 0 if result.get("success") else 1


def main() -> int:
    """Main entry point."""
    configure_stdio()
    if len(sys.argv) > 1:
        return run_cli_mode(sys.argv[1:])
    return run_json_mode()


if __name__ == "__main__":
    raise SystemExit(main())
