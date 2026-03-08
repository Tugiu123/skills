#!/usr/bin/env python3
"""
Check Bitrix24 webhook availability from env vars or nearby .env files.

The script intentionally masks the webhook secret in output.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import socket
import sys
from pathlib import Path
from typing import Any
from urllib import error, request

WEBHOOK_RE = re.compile(r"^https://(?P<host>[^/]+)/rest/(?P<user_id>\d+)/(?P<secret>[^/]+)/?$")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Check a Bitrix24 webhook URL.")
    parser.add_argument("--url", help="Webhook URL to check")
    parser.add_argument(
        "--env-file",
        action="append",
        default=[],
        help="Read BITRIX24_WEBHOOK_URL from this env file (repeatable)",
    )
    parser.add_argument("--skip-http", action="store_true", help="Skip user.current probe")
    parser.add_argument("--json", action="store_true", help="Print JSON output")
    parser.add_argument("--timeout", type=float, default=10.0, help="HTTP timeout in seconds")
    return parser.parse_args()


def normalize_url(value: str) -> str:
    return value.strip().strip('"').strip("'").rstrip("/") + "/"


def mask_url(value: str) -> str:
    match = WEBHOOK_RE.match(value)
    if not match:
        return value
    secret = match.group("secret")
    if len(secret) <= 4:
        masked = "*" * len(secret)
    else:
        masked = f"{secret[:2]}***{secret[-2:]}"
    return f"https://{match.group('host')}/rest/{match.group('user_id')}/{masked}/"


def read_env_file(path: Path) -> str | None:
    if not path.is_file():
        return None

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("export "):
            line = line[7:].strip()
        if not line.startswith("BITRIX24_WEBHOOK_URL="):
            continue
        return line.split("=", 1)[1].strip()
    return None


def candidate_env_files(extra: list[str]) -> list[Path]:
    paths: list[Path] = []
    for item in extra:
        path = Path(item).expanduser()
        if path not in paths:
            paths.append(path)

    cwd = Path.cwd()
    for base in [cwd, cwd.parent]:
        for name in [".env", ".env.local", ".env.development", ".env.production"]:
            path = base / name
            if path not in paths:
                paths.append(path)
    return paths


def load_url(args: argparse.Namespace) -> tuple[str | None, str]:
    if args.url:
        return args.url, "arg:url"

    env_value = os.environ.get("BITRIX24_WEBHOOK_URL")
    if env_value:
        return env_value, "env:BITRIX24_WEBHOOK_URL"

    for path in candidate_env_files(args.env_file):
        value = read_env_file(path)
        if value:
            return value, f"env-file:{path}"

    return None, "missing"


def resolve_dns(host: str) -> tuple[bool, list[str], str | None]:
    try:
        infos = socket.getaddrinfo(host, 443, type=socket.SOCK_STREAM)
    except OSError as exc:
        return False, [], str(exc)

    ips = sorted({info[4][0] for info in infos if info[4]})
    return True, ips, None


def probe_user_current(url: str, timeout: float) -> tuple[bool, int | None, dict[str, Any] | None, str | None]:
    target = url + "user.current.json"
    req = request.Request(target, headers={"Accept": "application/json"})
    try:
        with request.urlopen(req, timeout=timeout) as response:
            status = response.getcode()
            payload = response.read().decode("utf-8", errors="replace")
    except error.HTTPError as exc:
        try:
            payload = exc.read().decode("utf-8", errors="replace")
        except Exception:
            payload = ""
        return False, exc.code, safe_json(payload), f"HTTP {exc.code}"
    except Exception as exc:
        return False, None, None, str(exc)

    data = safe_json(payload)
    if isinstance(data, dict) and data.get("error"):
        return False, status, data, str(data.get("error_description") or data["error"])
    return True, status, data, None


def safe_json(payload: str) -> dict[str, Any] | None:
    if not payload:
        return None
    try:
        value = json.loads(payload)
    except Exception:
        return None
    return value if isinstance(value, dict) else {"raw": value}


def build_result(args: argparse.Namespace) -> dict[str, Any]:
    raw_url, source = load_url(args)
    result: dict[str, Any] = {
        "source": source,
        "url_found": raw_url is not None,
        "format_ok": False,
        "dns_ok": False,
        "http_ok": None if args.skip_http else False,
    }

    if not raw_url:
        result["error"] = "BITRIX24_WEBHOOK_URL was not found in args, environment, or nearby env files"
        return result

    normalized = normalize_url(raw_url)
    result["masked_url"] = mask_url(normalized)

    match = WEBHOOK_RE.match(normalized)
    if not match:
        result["error"] = "Webhook format is invalid"
        return result

    host = match.group("host")
    result["format_ok"] = True
    result["host"] = host
    result["user_id"] = match.group("user_id")

    dns_ok, ips, dns_error = resolve_dns(host)
    result["dns_ok"] = dns_ok
    result["dns_ips"] = ips
    if dns_error:
        result["dns_error"] = dns_error
        return result

    if args.skip_http:
        return result

    http_ok, status, payload, http_error = probe_user_current(normalized, args.timeout)
    result["http_ok"] = http_ok
    result["http_status"] = status
    if payload is not None:
        result["http_payload"] = payload
    if http_error:
        result["http_error"] = http_error
    return result


def print_plain(result: dict[str, Any]) -> None:
    for key in [
        "source",
        "url_found",
        "masked_url",
        "format_ok",
        "host",
        "user_id",
        "dns_ok",
        "dns_ips",
        "dns_error",
        "http_ok",
        "http_status",
        "http_error",
        "error",
    ]:
        if key in result:
            print(f"{key}: {result[key]}")
    if "http_payload" in result:
        print("http_payload:")
        print(json.dumps(result["http_payload"], ensure_ascii=True, indent=2))


def main() -> int:
    args = parse_args()
    result = build_result(args)

    if args.json:
        print(json.dumps(result, ensure_ascii=True, indent=2))
    else:
        print_plain(result)

    if not result.get("url_found"):
        return 1
    if not result.get("format_ok"):
        return 1
    if not result.get("dns_ok"):
        return 1
    if result.get("http_ok") is False:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
