#!/usr/bin/env python3
"""
Upload HTML files to tiiny.host for instant sharing.

Usage:
    python scripts/share-tiiny.py presentation.html
    python scripts/share-tiiny.py presentation.html --email your@email.com
    python scripts/share-tiiny.py presentation.html --api-key YOUR_KEY

Anonymous uploads (--email) expire in 1 hour.
API key uploads are permanent (get key at https://tiiny.host).

Output: Prints the shareable URL.
"""

import argparse
import json
import mimetypes
import sys
import urllib.request
import urllib.error
from pathlib import Path
from email.message import EmailMessage


def encode_multipart(files: list[Path]) -> bytes:
    """Encode files as multipart/form-data using stdlib."""
    boundary = "----WebKitFormBoundary7MA4YWxkTrZu0gW"
    lines = []

    for filepath in files:
        filename = filepath.name
        mime_type = mimetypes.guess_type(filename)[0] or "application/octet-stream"
        content = filepath.read_bytes()

        lines.append(f"--{boundary}".encode())
        lines.append(
            f'Content-Disposition: form-data; name="files"; filename="{filename}"'.encode()
        )
        lines.append(f"Content-Type: {mime_type}".encode())
        lines.append(b"")
        lines.append(content)

    lines.append(f"--{boundary}--".encode())
    return b"\r\n".join(lines)


def upload(
    files: list[Path], email: str = None, api_key: str = None, domain: str = None
) -> str:
    """Upload files to tiiny.host. Returns shareable URL."""

    if not email and not api_key:
        raise ValueError("Must provide --email (anonymous) or --api-key (permanent)")

    # Build request
    url = "https://ext.tiiny.host/v1/upload"
    boundary = "----WebKitFormBoundary7MA4YWxkTrZu0gW"

    headers = {"Content-Type": f"multipart/form-data; boundary={boundary}"}

    if api_key:
        headers["x-api-key"] = api_key
    else:
        headers["x-email"] = email

    # Encode multipart body
    body_parts = []
    for filepath in files:
        filename = filepath.name
        mime_type = mimetypes.guess_type(filename)[0] or "application/octet-stream"
        content = filepath.read_bytes()

        body_parts.append(f"--{boundary}")
        body_parts.append(f'Content-Disposition: form-data; name="files"; filename="{filename}"')
        body_parts.append(f"Content-Type: {mime_type}")
        body_parts.append("")
        body_parts.append(content.decode("utf-8", errors="replace"))

    if domain:
        body_parts.append(f"--{boundary}")
        body_parts.append('Content-Disposition: form-data; name="domain"')
        body_parts.append("")
        body_parts.append(domain)

    body_parts.append(f"--{boundary}--")
    body = "\r\n".join(body_parts).encode("utf-8")

    # Send request
    req = urllib.request.Request(url, data=body, headers=headers, method="POST")

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            result = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8")
        raise RuntimeError(f"Upload failed ({e.code}): {error_body}")

    # Parse response
    # Expected: {"url": "https://xxx.tiiny.site", ...}
    if "url" in result:
        return result["url"]
    elif "domain" in result:
        return f"https://{result['domain']}"
    else:
        raise RuntimeError(f"Unexpected response: {result}")


def main():
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "files",
        nargs="+",
        type=Path,
        help="HTML file(s) to upload (first file is the entry point)",
    )
    parser.add_argument(
        "--email",
        help="Email for anonymous upload (expires in 1 hour)",
    )
    parser.add_argument(
        "--api-key",
        help="API key for permanent upload (get from https://tiiny.host)",
    )
    parser.add_argument(
        "--domain",
        help="Custom subdomain (e.g., 'mysite' -> mysite.tiiny.site)",
    )

    args = parser.parse_args()

    # Validate files exist
    for f in args.files:
        if not f.exists():
            print(f"Error: File not found: {f}", file=sys.stderr)
            sys.exit(1)

    # Upload
    try:
        url = upload(
            files=args.files,
            email=args.email,
            api_key=args.api_key,
            domain=args.domain,
        )
        print(f"✓ Published: {url}")
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()