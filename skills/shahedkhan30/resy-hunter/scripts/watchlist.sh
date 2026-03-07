#!/usr/bin/env bash
# watchlist.sh — Manage the resy-hunter restaurant watchlist
# Usage:
#   ./watchlist.sh list                  — Show all watched restaurants
#   ./watchlist.sh add '<json>'          — Add a restaurant to the watchlist
#   ./watchlist.sh remove <id>           — Remove a restaurant by ID
#   ./watchlist.sh get <id>              — Get a single restaurant by ID
#
# Watchlist file: ~/.openclaw/skills/resy-hunter/watchlist.json

set -euo pipefail

WATCHLIST_DIR="$HOME/.openclaw/skills/resy-hunter"
WATCHLIST_FILE="${WATCHLIST_DIR}/watchlist.json"

# Initialize watchlist if it doesn't exist
if [[ ! -f "$WATCHLIST_FILE" ]]; then
  mkdir -p "$WATCHLIST_DIR"
  echo '{"restaurants":[]}' > "$WATCHLIST_FILE"
fi

ACTION="${1:-}"

case "$ACTION" in
  list)
    entries=$(jq '.restaurants | length' "$WATCHLIST_FILE")
    if [[ "$entries" == "0" ]]; then
      echo '{"restaurants":[],"count":0,"message":"Watchlist is empty. Add restaurants to start monitoring."}'
    else
      jq '{restaurants: .restaurants, count: (.restaurants | length)}' "$WATCHLIST_FILE"
    fi
    ;;

  add)
    if [[ $# -lt 2 ]]; then
      echo '{"error": "Usage: watchlist.sh add '\''<json>'\''"}' >&2
      exit 1
    fi
    ENTRY="$2"

    # Validate the JSON entry has required fields
    if ! echo "$ENTRY" | jq -e '.name and .platform and .party_size and .dates' > /dev/null 2>&1; then
      echo '{"error": "Entry must include: name, platform (resy/opentable/tock), party_size, dates array. Platform-specific: venue_id (resy), restaurant_id (opentable), slug (tock)."}' >&2
      exit 1
    fi

    platform=$(echo "$ENTRY" | jq -r '.platform')

    # Validate platform-specific identifier
    case "$platform" in
      resy)
        if ! echo "$ENTRY" | jq -e '.venue_id' > /dev/null 2>&1; then
          echo '{"error": "Resy entries require venue_id (integer)"}' >&2
          exit 1
        fi
        ;;
      opentable)
        if ! echo "$ENTRY" | jq -e '.restaurant_id' > /dev/null 2>&1; then
          echo '{"error": "OpenTable entries require restaurant_id (integer)"}' >&2
          exit 1
        fi
        ;;
      tock)
        if ! echo "$ENTRY" | jq -e '.slug' > /dev/null 2>&1; then
          echo '{"error": "Tock entries require slug (string)"}' >&2
          exit 1
        fi
        ;;
      *)
        echo "{\"error\": \"Unknown platform: ${platform}. Use resy, opentable, or tock.\"}" >&2
        exit 1
        ;;
    esac

    # Generate next ID
    max_id=$(jq '[.restaurants[].id // 0] | max // 0' "$WATCHLIST_FILE")
    next_id=$((max_id + 1))

    # Add the entry with auto-generated fields
    added_at=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

    updated=$(jq --argjson id "$next_id" \
      --arg added_at "$added_at" \
      --argjson entry "$ENTRY" \
      '.restaurants += [$entry + {id: $id, added_at: $added_at, active: true}]' \
      "$WATCHLIST_FILE")

    echo "$updated" > "$WATCHLIST_FILE"

    echo "$updated" | jq --argjson id "$next_id" '{added: (.restaurants[] | select(.id == $id)), total: (.restaurants | length)}'
    ;;

  remove)
    if [[ $# -lt 2 ]]; then
      echo '{"error": "Usage: watchlist.sh remove <id>"}' >&2
      exit 1
    fi
    ID="$2"

    # Check if the ID exists
    exists=$(jq --argjson id "$ID" '[.restaurants[] | select(.id == ($id | tonumber))] | length' "$WATCHLIST_FILE")
    if [[ "$exists" == "0" ]]; then
      echo "{\"error\": \"No entry with id ${ID}\"}" >&2
      exit 1
    fi

    removed_name=$(jq -r --argjson id "$ID" '.restaurants[] | select(.id == ($id | tonumber)) | .name' "$WATCHLIST_FILE")

    updated=$(jq --argjson id "$ID" '.restaurants = [.restaurants[] | select(.id != ($id | tonumber))]' "$WATCHLIST_FILE")
    echo "$updated" > "$WATCHLIST_FILE"

    echo "{\"removed\": \"${removed_name}\", \"id\": ${ID}, \"remaining\": $(echo "$updated" | jq '.restaurants | length')}"
    ;;

  get)
    if [[ $# -lt 2 ]]; then
      echo '{"error": "Usage: watchlist.sh get <id>"}' >&2
      exit 1
    fi
    ID="$2"
    result=$(jq --argjson id "$ID" '.restaurants[] | select(.id == ($id | tonumber))' "$WATCHLIST_FILE")
    if [[ -z "$result" ]]; then
      echo "{\"error\": \"No entry with id ${ID}\"}" >&2
      exit 1
    fi
    echo "$result"
    ;;

  *)
    echo '{"error": "Usage: watchlist.sh list|add|remove|get"}' >&2
    exit 1
    ;;
esac
