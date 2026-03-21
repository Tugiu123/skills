#!/usr/bin/env python3
"""Video generation using API.
Reads API URL and Key from USER.md configuration.
Supports Sora/veo models via relay service.
"""

import requests
import json
import sys
import os
import re
import time

CONFIG = None


def load_config():
    """Load API URL and Key from USER.md"""
    global CONFIG
    if CONFIG:
        return CONFIG
    
    user_md = os.path.expanduser("~/.openclaw/workspace/USER.md")
    try:
        with open(user_md, "r") as f:
            content = f.read()
        
        config = {}
        
        # Find 视频生成 section
        lines = content.split('\n')
        in_vid_section = False
        for line in lines:
            # Detect section change - use exact section headers
            stripped = line.strip()
            if stripped.startswith('###'):
                # Entering a new section
                if '视频生成' in line:
                    in_vid_section = True
                else:
                    in_vid_section = False
                continue
            
            if in_vid_section:
                # Match "中转站API 地址: https://..." or "中转地址: https://..."
                url_match = re.search(r'(?:中转站API\s*地址|中转地址|API地址|URL|uri)[:\s]*(https?://[^\s]+)', line, re.IGNORECASE)
                if url_match:
                    config['url'] = url_match.group(1).rstrip('/')
                
                # Match "API Key: sk-..." or "Key: sk-..."
                key_match = re.search(r'(?:API\s*Key|Key|密钥)[:\s]*(sk-[a-zA-Z0-9]+)', line)
                if key_match:
                    config['key'] = key_match.group(1)
        
        if 'url' not in config or 'key' not in config:
            print(f"[VID] Config not found in USER.md. Please add 视频生成 API config.")
            sys.exit(1)
        
        CONFIG = config
        return config
    except Exception as e:
        print(f"[VID] Failed to read USER.md: {e}")
        sys.exit(1)


def generate_video(prompt: str, model: str = "sora-2-pro-all", size: str = "16:9", output_path: str = None):
    """Generate video from text prompt.
    
    Args:
        prompt: Video description
        model: Model to use (sora-2-pro-all or veo_3_1-4K)
        size: Aspect ratio (16:9 or 9:16)
        output_path: Output file path
    """
    if output_path is None:
        output_path = os.path.expanduser("~/Desktop/generated_video.mp4")

    config = load_config()
    base_url = config['url']
    api_key = config['key']

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }

    # Size mapping
    size_map = {
        "16:9": {"width": 1920, "height": 1080},
        "9:16": {"width": 1080, "height": 1920},
    }
    dimensions = size_map.get(size, size_map["16:9"])

    payload = {
        "model": model,
        "prompt": prompt,
        "duration": 5,
        "aspect_ratio": size,
        "resolution": f"{dimensions['width']}x{dimensions['height']}",
    }

    print(f"[VID] Generating video...")
    print(f"[VID] Model: {model}, Size: {size}")
    print(f"[VID] Prompt: {prompt[:80]}")
    print(f"[VID] URL: {base_url}")

    # Create task
    create_url = base_url
    response = requests.post(create_url, headers=headers, json=payload, timeout=30)
    
    if response.status_code != 200:
        print(f"[VID] Create error: {response.status_code}")
        print(response.text[:300])
        return None

    result = response.json()
    task_id = result.get("task_id")
    if not task_id:
        print(f"[VID] No task_id in response")
        print(json.dumps(result, indent=2)[:500])
        return None

    print(f"[VID] Task created: {task_id}")

    # Poll for completion
    query_url = base_url.replace("/video/create", "/video/query")
    max_wait = 300  # 5 minutes
    interval = 5
    elapsed = 0

    while elapsed < max_wait:
        time.sleep(interval)
        elapsed += interval
        
        try:
            resp = requests.get(f"{query_url}?task_id={task_id}", headers=headers, timeout=10)
            if resp.status_code == 200:
                status = resp.json()
                state = status.get("state", "")
                print(f"[VID] Status: {state} ({elapsed}s)")
                
                if state == "completed":
                    video_url = status.get("video", {}).get("url")
                    if video_url:
                        # Download video
                        print(f"[VID] Downloading from: {video_url}")
                        video_resp = requests.get(video_url, timeout=60)
                        with open(output_path, "wb") as f:
                            f.write(video_resp.content)
                        print(f"[VID] Saved: {output_path}")
                        return output_path
                elif state in ["failed", "error"]:
                    print(f"[VID] Task failed: {status}")
                    return None
        except Exception as e:
            print(f"[VID] Poll error: {e}")

    print(f"[VID] Timeout after {max_wait}s")
    return None


if __name__ == "__main__":
    # Usage:
    #   python3 gen_video.py "描述" [model] [size] [output_path]
    args = sys.argv[1:]
    if not args:
        print("Usage:")
        print("  python3 gen_video.py <prompt> [model] [size] [output_path]")
        print("  model: sora-2-pro-all (default) or veo_3_1-4K")
        print("  size: 16:9 (default) or 9:16")
        sys.exit(1)

    prompt = args[0]
    model = args[1] if len(args) > 1 else "sora-2-pro-all"
    size = args[2] if len(args) > 2 else "16:9"
    output_path = args[3] if len(args) > 3 else None

    result = generate_video(prompt, model, size, output_path)
    if result:
        print(f"SUCCESS: {result}")
    else:
        print("FAILED")
        sys.exit(1)
