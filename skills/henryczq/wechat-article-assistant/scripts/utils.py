#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Utility functions for WeChat article skill."""

import json
import sys
from datetime import datetime
from typing import Any, Dict, Optional, Tuple


def failure(message: str, data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Return a failure response."""
    result: Dict[str, Any] = {"success": False, "error": message}
    if data is not None:
        result["data"] = data
    return result


def success(data: Dict[str, Any], formatted_text: Optional[str] = None) -> Dict[str, Any]:
    """Return a success response."""
    result: Dict[str, Any] = {"success": True, "data": data}
    if formatted_text:
        result["formatted_text"] = formatted_text
    return result


def format_timestamp(timestamp: Optional[int]) -> str:
    """Format a Unix timestamp to a human-readable string."""
    if not timestamp:
        return ""
    try:
        return datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")
    except (OverflowError, OSError, ValueError):
        return ""


def validate_positive_int(value: Any, name: str) -> Tuple[Optional[int], Optional[Dict[str, Any]]]:
    """Validate that a value is a positive integer."""
    if isinstance(value, bool) or not isinstance(value, int):
        return None, failure(f"{name} must be an integer")
    if value <= 0:
        return None, failure(f"{name} must be greater than 0")
    return value, None


def parse_input() -> Tuple[Optional[Dict[str, Any]], Optional[Dict[str, Any]]]:
    """Parse JSON input from stdin."""
    raw_input = sys.stdin.read().strip()
    if not raw_input:
        return None, failure("Empty JSON input")

    try:
        input_data = json.loads(raw_input)
    except json.JSONDecodeError as exc:
        return None, failure(f"Invalid JSON input: {exc}")

    if not isinstance(input_data, dict):
        return None, failure("Input must be a JSON object")

    return input_data, None
