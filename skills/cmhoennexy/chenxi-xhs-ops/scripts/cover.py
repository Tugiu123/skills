#!/usr/bin/env python3
"""Generate Xiaohongshu cover images from HTML template."""
import sys
import os
import argparse
import http.server
import threading
import time
import re


def modify_template(template_path, title, subtitle=""):
    with open(template_path, "r") as f:
        html = f.read()

    def replace_h1(m):
        return m.group(1) + title + m.group(3)
    html = re.sub(r'(<h1[^>]*>)(.*?)(</h1>)', replace_h1, html, count=1, flags=re.DOTALL)

    if subtitle:
        def replace_h2(m):
            return m.group(1) + subtitle + m.group(3)
        html = re.sub(r'(<h2[^>]*>)(.*?)(</h2>)', replace_h2, html, count=1, flags=re.DOTALL)

    return html


def start_server(html_content, port=9988):
    class Handler(http.server.BaseHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(html_content.encode("utf-8"))
        def log_message(self, format, *args):
            pass

    server = http.server.HTTPServer(("127.0.0.1", port), Handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    return server


def screenshot(output_path, port=9988):
    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        browser = p.chromium.launch()
        ctx = browser.new_context(viewport={"width": 600, "height": 800}, device_scale_factor=2)
        page = ctx.new_page()
        page.goto(f"http://127.0.0.1:{port}/")
        page.wait_for_timeout(2500)
        page.screenshot(path=output_path)
        browser.close()
    print(f"✅ Cover saved: {output_path} (1200×1600)")


def main():
    parser = argparse.ArgumentParser(description="Generate XHS cover image")
    parser.add_argument("title", help="Main title")
    parser.add_argument("subtitle", nargs="?", default="", help="Subtitle (optional)")
    parser.add_argument("--output", "-o", default=None, help="Output path")
    parser.add_argument("--port", type=int, default=9988, help="HTTP server port")
    parser.add_argument("--template", "-t", default=None, help="Custom template path")
    args = parser.parse_args()

    # Locate template
    skill_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    template = args.template or os.path.join(skill_dir, "assets", "cover_template.html")
    if not os.path.exists(template):
        print(f"❌ Template not found: {template}")
        sys.exit(1)

    output = args.output or os.path.expanduser(f"~/covers/cover_{int(time.time())}.png")
    os.makedirs(os.path.dirname(output), exist_ok=True)

    html = modify_template(template, args.title, args.subtitle)
    server = start_server(html, args.port)
    try:
        screenshot(output, args.port)
    finally:
        server.shutdown()


if __name__ == "__main__":
    main()
