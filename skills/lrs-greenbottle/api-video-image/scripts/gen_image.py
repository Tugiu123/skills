#!/usr/bin/env python3
"""Image generation using Gemini API.
Reads API URL and Key from USER.md configuration.
Supports both text-to-image and image-to-image (style transfer).
"""

import requests
import json
import sys
import base64
import os
import re

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
        
        # Find 图片生成 section
        lines = content.split('\n')
        in_img_section = False
        for line in lines:
            # Detect section change - use exact section headers
            stripped = line.strip()
            if stripped.startswith('###'):
                # Entering a new section
                if '图片生成' in line:
                    in_img_section = True
                else:
                    in_img_section = False
                continue
            
            if in_img_section:
                # Match "中转站API 地址: https://..." or "中转地址: https://..."
                url_match = re.search(r'(?:中转站API\s*地址|中转地址|API地址|URL|uri)[:\s]*(https?://[^\s]+)', line, re.IGNORECASE)
                if url_match:
                    config['url'] = url_match.group(1).rstrip('/')
                
                # Match "API Key: sk-..." or "Key: sk-..."
                key_match = re.search(r'(?:API\s*Key|Key|密钥)[:\s]*(sk-[a-zA-Z0-9]+)', line)
                if key_match:
                    config['key'] = key_match.group(1)
        
        if 'url' not in config or 'key' not in config:
            print(f"[IMG] Config not found in USER.md. Please add 图片生成 API config.")
            sys.exit(1)
        
        CONFIG = config
        return config
    except Exception as e:
        print(f"[IMG] Failed to read USER.md: {e}")
        sys.exit(1)


def generate_image(prompt: str, output_path: str = None, ref_image_path: str = None):
    """Generate an image from text, optionally with a reference image.
    
    If ref_image_path is provided, does image-to-image style transfer.
    """
    if output_path is None:
        output_path = os.path.expanduser("~/Desktop/generated_image.png")

    config = load_config()
    url = config['url']
    api_key = config['key']

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }

    parts = []

    if ref_image_path:
        # Image-to-image: attach reference image
        with open(ref_image_path, "rb") as f:
            img_b64 = base64.b64encode(f.read()).decode()
        parts.append({"inlineData": {"mimeType": "image/jpeg", "data": img_b64}})
        parts.append({"text": prompt})
        print(f"[IMG] Image-to-image mode, ref={ref_image_path}")
    else:
        # Text-to-image
        parts.append({"text": prompt})

    payload = {
        "contents": [{"role": "user", "parts": parts}],
        "generationConfig": {"responseModalities": ["IMAGE", "TEXT"]},
    }

    print(f"[IMG] Generating... prompt={prompt[:60]}")
    print(f"[IMG] URL: {url}")

    response = requests.post(url, headers=headers, json=payload, timeout=120)
    if response.status_code != 200:
        print(f"[IMG] Error: {response.status_code}")
        print(response.text[:300])
        return None

    result = response.json()
    if "candidates" in result:
        for candidate in result["candidates"]:
            if "content" in candidate:
                for part in candidate["content"].get("parts", []):
                    if "inlineData" in part:
                        image_data = part["inlineData"].get("data")
                        if image_data:
                            with open(output_path, "wb") as f:
                                f.write(base64.b64decode(image_data))
                            print(f"[IMG] Saved: {output_path}")
                            return output_path

    print("[IMG] No image in response")
    return None


if __name__ == "__main__":
    # Usage:
    # Text-to-image:
    #   python3 gen_image.py "描述" [输出路径]
    # Image-to-image (style transfer):
    #   python3 gen_image.py "描述" [输出路径] [参考图路径]
    args = sys.argv[1:]
    if not args:
        print("Usage:")
        print("  Text-to-image: python3 gen_image.py <prompt> [output_path]")
        print("  Image-to-image: python3 gen_image.py <prompt> [output_path] <ref_image_path>")
        sys.exit(1)

    prompt = args[0]
    output_path = args[1] if len(args) > 1 else None
    ref_image = args[2] if len(args) > 2 else None

    result = generate_image(prompt, output_path, ref_image)
    if result:
        print(f"SUCCESS: {result}")
    else:
        print("FAILED")
        sys.exit(1)
