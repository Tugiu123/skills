#!/usr/bin/env python3
"""
Unified async polling script (channel-agnostic)
Subcommands:
  register  -- start background polling process
  check     -- single status check (for manual debugging)
  cancel    -- cancel polling

Delivers results via openclaw message send, supports all channels (Feishu/Telegram/QQ Bot etc.).
"""

import argparse
import glob
import json
import os
import signal
import shutil
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import plume_api
import video_utils

# task metadata directory
TASKS_DIR = Path.home() / ".openclaw" / "media" / "plume" / "cron_tasks"

# result file download directory
MEDIA_DIR = Path.home() / ".openclaw" / "media" / "plume"

# limits
MAX_ACTIVE_TASKS = 5
DEFAULT_MAX_DURATION = 1800  # 30 minutes
DEFAULT_INTERVAL = 10  # seconds


def log(msg: str):
    print(f"[plume-poll] {msg}", file=sys.stderr, flush=True)


def output(data: dict):
    print(json.dumps(data, ensure_ascii=False))


# ─── utilities ──────────────────────────────────────────────

def _find_openclaw_cmd() -> str:
    """Find the full path to the openclaw command"""
    path = shutil.which("openclaw")
    if path:
        return path

    try:
        shell = os.environ.get("SHELL", "/bin/bash")
        result = subprocess.run(
            [shell, "-l", "-c", "which openclaw"],
            capture_output=True, text=True, timeout=5,
        )
        if result.returncode == 0 and result.stdout.strip():
            p = result.stdout.strip()
            if os.path.isfile(p) and os.access(p, os.X_OK):
                return p
    except Exception:
        pass

    for pattern in [
        "/usr/local/bin/openclaw",
        os.path.expanduser("~/.nvm/versions/node/*/bin/openclaw"),
        os.path.expanduser("~/.local/bin/openclaw"),
    ]:
        matches = glob.glob(pattern)
        if matches and os.path.isfile(matches[0]) and os.access(matches[0], os.X_OK):
            return matches[0]

    raise FileNotFoundError("openclaw command not found, please confirm it is installed")


def _ensure_dirs():
    TASKS_DIR.mkdir(parents=True, exist_ok=True)
    MEDIA_DIR.mkdir(parents=True, exist_ok=True)


def _save_meta(task_id: str, meta: dict):
    _ensure_dirs()
    (TASKS_DIR / f"{task_id}.json").write_text(
        json.dumps(meta, ensure_ascii=False), encoding="utf-8"
    )


def _load_meta(task_id: str) -> dict | None:
    path = TASKS_DIR / f"{task_id}.json"
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return None


def _delete_meta(task_id: str):
    path = TASKS_DIR / f"{task_id}.json"
    try:
        path.unlink(missing_ok=True)
    except OSError:
        pass


def _count_active_tasks() -> int:
    if not TASKS_DIR.exists():
        return 0
    return len(list(TASKS_DIR.glob("*.json")))


def _deliver(channel: str, target: str, message: str, media_path: str = None):
    """Deliver message/media via openclaw message send"""
    try:
        openclaw_cmd = _find_openclaw_cmd()
    except FileNotFoundError:
        log("openclaw command not found, cannot deliver")
        return

    cmd = [openclaw_cmd, "message", "send", "--channel", channel, "--target", target]

    if media_path and os.path.isfile(media_path):
        cmd += ["--media", media_path]
        if message:
            cmd += ["--message", message]
    elif message:
        cmd += ["--message", message]
    else:
        return

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        if result.returncode != 0:
            log(f"Delivery failed: {result.stderr.strip()}")
        else:
            log(f"Delivered: channel={channel}, target={target}")
    except subprocess.TimeoutExpired:
        log("Delivery timed out")
    except Exception as e:
        log(f"Delivery error: {e}")


def _download_file(url: str, output_path: str, timeout: int = 120) -> bool:
    """Download file to local"""
    import ssl
    import urllib.request
    import urllib.error

    ctx = ssl.create_default_context()
    req = urllib.request.Request(url, headers={"User-Agent": "Plume-Image/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=timeout, context=ctx) as resp:
            with open(output_path, "wb") as f:
                while True:
                    chunk = resp.read(1024 * 1024)
                    if not chunk:
                        break
                    f.write(chunk)
        if os.path.getsize(output_path) == 0:
            os.remove(output_path)
            return False
        return True
    except Exception as e:
        log(f"Download failed: {e}")
        try:
            if os.path.exists(output_path):
                os.remove(output_path)
        except OSError:
            pass
        return False


def _extract_result_url(task_result: dict) -> tuple[str | None, str]:
    """Extract result URL from task result, returns (url, media_type)"""
    if not isinstance(task_result, dict):
        return None, "image"

    # video: result.parts[0].videoUrl
    parts = task_result.get("parts")
    if isinstance(parts, list) and parts:
        first = parts[0]
        if isinstance(first, dict) and first.get("videoUrl"):
            return first["videoUrl"], "video"

    # image: imageUrl / url / imageUrls[0]
    url = task_result.get("imageUrl") or task_result.get("url")
    if not url and task_result.get("imageUrls"):
        url = task_result["imageUrls"][0]
    if not url and isinstance(parts, list) and parts:
        first = parts[0]
        if isinstance(first, dict):
            url = first.get("imageUrl") or first.get("url")

    # nested data.file (remove-watermark etc.)
    if not url:
        data = task_result.get("data")
        if isinstance(data, dict):
            url = data.get("file") or data.get("imageUrl") or data.get("url")

    return url, "image"


def _handle_completed(task_id: str, task: dict, channel: str, target: str):
    """Handle completed task (success/failure)"""
    status = task.get("status", 0)

    if status == 3:
        # success
        task_result = task.get("result")
        if isinstance(task_result, str):
            try:
                task_result = json.loads(task_result)
            except json.JSONDecodeError:
                pass

        result_url, media_type = _extract_result_url(task_result)

        if result_url:
            video_suffix = video_utils.get_video_suffix(result_url)
            if video_suffix:
                suffix = video_suffix
                media_type = "video"
            elif ".jpg" in result_url.lower() or ".jpeg" in result_url.lower():
                suffix = ".jpg"
            elif ".webp" in result_url.lower():
                suffix = ".webp"
            else:
                suffix = ".png"

            _ensure_dirs()
            local_file = str(MEDIA_DIR / f"result_{task_id}{suffix}")
            dl_timeout = 300 if media_type == "video" else 120

            if _download_file(result_url, local_file, timeout=dl_timeout):
                log(f"Result downloaded to {local_file}")

                # save last_result for subsequent image-to-image use (isolated by channel to prevent cross-channel mix-up)
                try:
                    last_result = {
                        "task_id": task_id,
                        "result_url": result_url,
                        "local_file": local_file,
                        "media_type": media_type,
                        "created_at": time.time(),
                    }
                    filename = f"last_result_{channel}.json" if channel else "last_result.json"
                    (MEDIA_DIR / filename).write_text(
                        json.dumps(last_result, ensure_ascii=False), encoding="utf-8"
                    )
                except Exception as e:
                    log(f"Failed to write last_result: {e}")

                label = "video" if media_type == "video" else "image"
                _deliver(channel, target, f"✅ {label} generation complete!", local_file)
                return {"success": True, "status": status, "media_type": media_type,
                        "local_file": local_file, "delivered": True}
            else:
                _deliver(channel, target, f"✅ Task #{task_id} completed, but download failed. Result URL: {result_url}")
                return {"success": True, "status": status, "download_failed": True, "result_url": result_url}
        else:
            _deliver(channel, target, f"✅ Task #{task_id} completed, but no result file found.")
            return {"success": True, "status": status, "no_result_url": True}
    else:
        # failed / timeout / cancelled
        status_map = {4: "failed", 5: "timeout", 6: "cancelled"}
        status_text = status_map.get(status, f"unknown({status})")
        error_info = task.get("result", "")
        msg = f"❌ Task #{task_id} {status_text}"
        if error_info:
            msg += f"\n{error_info}"
        _deliver(channel, target, msg)
        return {"success": False, "status": status, "status_text": status_text}


# ─── background polling process ─────────────────────────────────────────

def _poll_loop(task_id: str, channel: str, target: str, interval: int, max_duration: int):
    """Background polling main loop (executed by forked child process)"""
    start_time = time.time()

    while True:
        elapsed = time.time() - start_time

        # timeout check
        if elapsed > max_duration:
            log(f"Task {task_id} timed out ({elapsed:.0f}s > {max_duration}s)")
            _deliver(channel, target, f"⏰ Task #{task_id} has been waiting {int(elapsed)}s without completion, polling cancelled.")
            _delete_meta(task_id)
            return

        # query task status
        try:
            result = plume_api.get_task(task_id)
        except Exception as e:
            log(f"Task {task_id} query error: {e}, retrying in {interval}s")
            time.sleep(interval)
            continue

        if not result.get("success"):
            log(f"Task {task_id} query failed, retrying in {interval}s")
            time.sleep(interval)
            continue

        task = result.get("data", {})
        status = task.get("status", 0)

        # not done, keep waiting
        if status < 3:
            log(f"Task {task_id} processing (status={status}, elapsed={elapsed:.0f}s)")
            time.sleep(interval)
            continue

        # terminal state: handle result
        log(f"Task {task_id} terminal status={status}")
        _handle_completed(task_id, task, channel, target)
        _delete_meta(task_id)
        return


# ─── register subcommand ────────────────────────────────────────

def cmd_register(args):
    """Start background polling process"""
    task_id = args.task_id
    channel = args.channel
    target = args.target
    interval = args.interval or DEFAULT_INTERVAL
    max_duration = args.max_duration or DEFAULT_MAX_DURATION

    # check active task limit
    active = _count_active_tasks()
    if active >= MAX_ACTIVE_TASKS:
        output({
            "success": False,
            "error": f"Active poll tasks at limit ({MAX_ACTIVE_TASKS}), wait for existing tasks to complete before adding more.",
        })
        return

    # verify openclaw is available
    try:
        _find_openclaw_cmd()
    except FileNotFoundError as e:
        output({"success": False, "error": str(e)})
        return

    # save metadata
    meta = {
        "task_id": task_id,
        "channel": channel,
        "target": target,
        "interval": interval,
        "max_duration": max_duration,
        "created_at": time.time(),
    }

    # fork background process for polling
    script_path = os.path.abspath(__file__)
    env = os.environ.copy()
    proc = subprocess.Popen(
        [sys.executable, script_path, "_poll",
         f"--task-id={task_id}",
         f"--channel={channel}",
         f"--target={target}",
         f"--interval={interval}",
         f"--max-duration={max_duration}"],
        stdout=subprocess.DEVNULL,
        stderr=open(str(MEDIA_DIR / f"poll_{task_id}.log"), "a"),
        stdin=subprocess.DEVNULL,
        env=env,
        start_new_session=True,
    )

    meta["pid"] = proc.pid
    _save_meta(task_id, meta)

    log(f"register: task_id={task_id}, pid={proc.pid}, interval={interval}s")

    output({
        "success": True,
        "task_id": task_id,
        "pid": proc.pid,
        "message": f"Background polling started, checking every {interval}s, max {max_duration}s",
    })


# ─── _poll subcommand (internal use) ────────────────────────────────

def cmd_poll_internal(args):
    """Background polling process entry point (called by register fork)"""
    log(f"Background poll started: task_id={args.task_id}, pid={os.getpid()}")
    _poll_loop(
        task_id=args.task_id,
        channel=args.channel,
        target=args.target,
        interval=args.interval,
        max_duration=args.max_duration,
    )
    log(f"Background poll ended: task_id={args.task_id}")


# ─── check subcommand ───────────────────────────────────────────

def cmd_check(args):
    """Single status check (for manual debugging)"""
    task_id = args.task_id

    meta = _load_meta(task_id)
    channel = meta["channel"] if meta else "unknown"
    target = meta["target"] if meta else "unknown"

    # query task status
    result = plume_api.get_task(task_id)
    if not result.get("success"):
        output({"success": False, "error": "Task query failed"})
        return

    task = result.get("data", {})
    status = task.get("status", 0)

    if status < 3:
        output({"success": True, "status": status, "waiting": True})
    else:
        check_result = _handle_completed(task_id, task, channel, target)
        if meta:
            _delete_meta(task_id)
        output(check_result)


# ─── cancel subcommand ──────────────────────────────────────────

def cmd_cancel(args):
    """Cancel polling"""
    task_id = args.task_id

    meta = _load_meta(task_id)
    if not meta:
        output({"success": False, "error": f"No poll info found for task {task_id}"})
        return

    # terminate background process
    pid = meta.get("pid")
    if pid:
        try:
            os.kill(pid, signal.SIGTERM)
            log(f"Terminated poll process pid={pid}")
        except ProcessLookupError:
            log(f"Process pid={pid} no longer exists")
        except Exception as e:
            log(f"Failed to terminate process pid={pid}: {e}")

    _delete_meta(task_id)
    output({"success": True, "message": f"Polling cancelled for task {task_id}"})


# ─── CLI entry point ──────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Plume unified polling script")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # register
    p_reg = subparsers.add_parser("register", help="Start background polling")
    p_reg.add_argument("--task-id", required=True, help="Plume task ID")
    p_reg.add_argument("--channel", required=True, help="Delivery channel (feishu/telegram/discord/...)")
    p_reg.add_argument("--target", required=True, help="Delivery target (ou_xxx/oc_xxx/user_id/channel_id)")
    p_reg.add_argument("--interval", type=int, default=DEFAULT_INTERVAL, help=f"Poll interval in seconds (default {DEFAULT_INTERVAL})")
    p_reg.add_argument("--max-duration", type=int, default=DEFAULT_MAX_DURATION, help=f"Max duration in seconds (default {DEFAULT_MAX_DURATION})")

    # _poll (internal use, not shown in help)
    p_poll = subparsers.add_parser("_poll")
    p_poll.add_argument("--task-id", required=True)
    p_poll.add_argument("--channel", required=True)
    p_poll.add_argument("--target", required=True)
    p_poll.add_argument("--interval", type=int, required=True)
    p_poll.add_argument("--max-duration", type=int, required=True)

    # check
    p_check = subparsers.add_parser("check", help="Single status check (for manual debugging)")
    p_check.add_argument("--task-id", required=True, help="Plume task ID")

    # cancel
    p_cancel = subparsers.add_parser("cancel", help="Cancel polling")
    p_cancel.add_argument("--task-id", required=True, help="Plume task ID")

    args = parser.parse_args()
    commands = {
        "register": cmd_register,
        "_poll": cmd_poll_internal,
        "check": cmd_check,
        "cancel": cmd_cancel,
    }

    try:
        log(f"=== poll_cron.py {args.command} called, argv={sys.argv[1:]} ===")
        commands[args.command](args)
    except Exception as e:
        output({"success": False, "error": str(e)})
        sys.exit(1)


if __name__ == "__main__":
    main()
