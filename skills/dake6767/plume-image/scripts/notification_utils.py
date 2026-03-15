#!/usr/bin/env python3
"""
Notification deduplication utility
Tracks notified notification IDs + timestamps in a local notified.json file,
along with notification.mute_duration for silence-period deduplication.

Shared by all cron scripts.
"""

import json
import time
from pathlib import Path

NOTIFIED_FILE = Path.home() / ".openclaw" / "media" / "plume" / "notified.json"


def _load_notified() -> dict:
    if not NOTIFIED_FILE.exists():
        return {}
    try:
        with open(NOTIFIED_FILE) as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return {}


def _save_notified(data: dict):
    NOTIFIED_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(NOTIFIED_FILE, "w") as f:
        json.dump(data, f, ensure_ascii=False)


def should_notify(notification: dict) -> bool:
    """Check if user should be notified (dedup by id + mute_duration)"""
    nid = notification.get("id")
    if not nid:
        return True

    mute_duration = notification.get("mute_duration", 0)
    if mute_duration <= 0:
        return True

    notified = _load_notified()
    last_time = notified.get(nid, 0)
    return (time.time() - last_time) > mute_duration


def mark_notified(notification: dict):
    """Mark notification as sent"""
    nid = notification.get("id")
    if not nid:
        return
    notified = _load_notified()
    notified[nid] = time.time()
    # purge records older than 30 days
    cutoff = time.time() - 30 * 86400
    notified = {k: v for k, v in notified.items() if v > cutoff}
    _save_notified(notified)
