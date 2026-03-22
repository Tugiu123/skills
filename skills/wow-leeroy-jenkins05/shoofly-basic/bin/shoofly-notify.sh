#!/usr/bin/env bash
# shoofly-notify — delivers alert messages via Telegram or WhatsApp
# Usage: shoofly-notify <channel> <message>
# Reads config from ~/.shoofly/config.json

set -euo pipefail

CONFIG_FILE="$HOME/.shoofly/config.json"

usage() {
  echo "Usage: shoofly-notify <channel> <message>" >&2
  echo "Channels: telegram, whatsapp" >&2
  exit 1
}

if [ $# -lt 2 ]; then
  usage
fi

CHANNEL="$1"
MESSAGE="$2"

if [ ! -f "$CONFIG_FILE" ]; then
  echo "Error: config file not found at $CONFIG_FILE" >&2
  exit 1
fi

case "$CHANNEL" in
  telegram)
    BOT_TOKEN=$(cat "$CONFIG_FILE" | grep -o '"bot_token"\s*:\s*"[^"]*"' | head -1 | sed 's/.*:.*"\([^"]*\)"/\1/')
    CHAT_ID=$(cat "$CONFIG_FILE" | grep -o '"chat_id"\s*:\s*"[^"]*"' | head -1 | sed 's/.*:.*"\([^"]*\)"/\1/')

    if [ -z "$BOT_TOKEN" ] || [ -z "$CHAT_ID" ]; then
      echo "Error: telegram requires bot_token and chat_id in $CONFIG_FILE" >&2
      exit 1
    fi

    curl -s -X POST "https://api.telegram.org/bot${BOT_TOKEN}/sendMessage" \
      -H "Content-Type: application/json" \
      -d "{\"chat_id\":\"${CHAT_ID}\",\"text\":$(printf '%s' "$MESSAGE" | python3 -c 'import sys,json; print(json.dumps(sys.stdin.read()))')}" \
      > /dev/null

    exit 0
    ;;

  whatsapp)
    API_URL=$(cat "$CONFIG_FILE" | grep -o '"api_url"\s*:\s*"[^"]*"' | head -1 | sed 's/.*:.*"\([^"]*\)"/\1/')

    if [ -z "$API_URL" ]; then
      echo "Error: whatsapp requires api_url in $CONFIG_FILE" >&2
      exit 1
    fi

    curl -s -X POST "$API_URL" \
      -H "Content-Type: application/json" \
      -d "{\"message\":$(printf '%s' "$MESSAGE" | python3 -c 'import sys,json; print(json.dumps(sys.stdin.read()))')}" \
      > /dev/null

    exit 0
    ;;

  *)
    echo "Error: unknown channel '$CHANNEL'. Supported: telegram, whatsapp" >&2
    exit 1
    ;;
esac
