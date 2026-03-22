#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""API client for WeChat article service."""

import json
import urllib.parse
import urllib.request
from typing import Any, Dict, Optional

BASE_URL = "http://localhost:3010/api/public/v1"
DEFAULT_TIMEOUT = 30


def make_request(url: str, method: str = "GET", data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Send an HTTP request and return the parsed JSON response."""
    try:
        # 对于 GET 请求，将 data 参数编码到 URL 中
        if method == "GET" and data is not None:
            query_params = urllib.parse.urlencode({k: v for k, v in data.items() if v is not None})
            if query_params:
                url = f"{url}&{query_params}" if "?" in url else f"{url}?{query_params}"
            req = urllib.request.Request(url, method=method)
        # 对于 POST 和 DELETE 请求，将 data 放到 body 中
        elif data is not None:
            json_data = json.dumps(data).encode("utf-8")
            req = urllib.request.Request(
                url,
                data=json_data,
                headers={"Content-Type": "application/json"},
                method=method,
            )
        else:
            req = urllib.request.Request(url, method=method)

        with urllib.request.urlopen(req, timeout=DEFAULT_TIMEOUT) as response:
            response_data = response.read().decode("utf-8")
            return json.loads(response_data)
    except urllib.error.HTTPError as exc:
        return {"success": False, "error": f"HTTP error {exc.code}: {exc.reason}"}
    except urllib.error.URLError as exc:
        return {"success": False, "error": f"URL error: {exc.reason}"}
    except json.JSONDecodeError as exc:
        return {"success": False, "error": f"JSON decode error: {exc}"}
    except Exception as exc:  # pragma: no cover - safety net for transport errors
        return {"success": False, "error": f"Request error: {exc}"}


def extract_api_error(response: Dict[str, Any], fallback: str) -> Optional[Dict[str, Any]]:
    """Extract error from API response if present."""
    if response.get("success") is False and "code" not in response:
        return {"success": False, "error": response.get("error", fallback)}
    base_resp = response.get("base_resp")
    if isinstance(base_resp, dict) and base_resp.get("ret") not in (None, 0):
        return {"success": False, "error": base_resp.get("err_msg") or fallback}
    if "code" in response and response.get("code") != 0:
        return {"success": False, "error": response.get("msg") or response.get("error") or fallback}
    return None
