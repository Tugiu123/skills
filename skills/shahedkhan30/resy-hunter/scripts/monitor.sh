#!/usr/bin/env bash
# monitor.sh — Sweep the entire watchlist and report new availability
# Usage: ./monitor.sh
#
# Reads watchlist.json, checks each active entry on each target date,
# diffs against .last-seen.json to find newly appeared slots,
# and outputs a JSON report.

set -euo pipefail

# Ensure Node.js is on PATH (for Playwright scripts)
if [[ -d "$HOME/.local/node/bin" ]]; then
  export PATH="$HOME/.local/node/bin:$PATH"
fi

SKILL_DIR="$HOME/.openclaw/skills/resy-hunter"
SCRIPTS_DIR="${SKILL_DIR}/scripts"
WATCHLIST_FILE="${SKILL_DIR}/watchlist.json"
STATE_FILE="${SKILL_DIR}/.last-seen.json"

# Initialize state file if needed
if [[ ! -f "$STATE_FILE" ]]; then
  echo '{"seen":{}}' > "$STATE_FILE"
fi

# Initialize watchlist if needed
if [[ ! -f "$WATCHLIST_FILE" ]]; then
  echo '{"restaurants":[]}' > "$WATCHLIST_FILE"
fi

TODAY=$(date -u +"%Y-%m-%d")
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

# Read active entries
entries=$(jq -c '[.restaurants[] | select(.active == true)]' "$WATCHLIST_FILE")
entry_count=$(echo "$entries" | jq 'length')

if [[ "$entry_count" == "0" ]]; then
  jq -n --arg ts "$TIMESTAMP" '{
    timestamp: $ts,
    new_availability: [],
    total_checked: 0,
    total_with_availability: 0,
    message: "Watchlist is empty"
  }'
  exit 0
fi

# Pre-fetch Resy auth token once if any entries use Resy
has_resy=$(echo "$entries" | jq '[.[] | select(.platform == "resy")] | length')
if [[ "$has_resy" -gt 0 && -z "${RESY_AUTH_TOKEN:-}" ]]; then
  RESY_AUTH_TOKEN=$(bash "${SCRIPTS_DIR}/resy-auth.sh" 2>/dev/null || true)
  if [[ -n "$RESY_AUTH_TOKEN" ]]; then
    export RESY_AUTH_TOKEN
  fi
fi

all_results="[]"
total_checked=0
total_with_availability=0

for i in $(seq 0 $((entry_count - 1))); do
  entry=$(echo "$entries" | jq -c ".[$i]")
  name=$(echo "$entry" | jq -r '.name')
  platform=$(echo "$entry" | jq -r '.platform')
  party_size=$(echo "$entry" | jq -r '.party_size')
  earliest=$(echo "$entry" | jq -r '.preferred_times.earliest // ""')
  latest=$(echo "$entry" | jq -r '.preferred_times.latest // ""')

  # Get dates array
  dates=$(echo "$entry" | jq -r '.dates[]')

  for date in $dates; do
    # Skip dates in the past
    if [[ "$date" < "$TODAY" ]]; then
      continue
    fi

    total_checked=$((total_checked + 1))

    # Run the appropriate check script
    result=""
    case "$platform" in
      resy)
        venue_id=$(echo "$entry" | jq -r '.venue_id')
        result=$(bash "${SCRIPTS_DIR}/resy-check.sh" "$venue_id" "$date" "$party_size" 2>/dev/null || echo '{"slots":[]}')
        ;;
      opentable)
        restaurant_id=$(echo "$entry" | jq -r '.restaurant_id')
        result=$(node "${SCRIPTS_DIR}/opentable-check.js" "$restaurant_id" "$date" "$party_size" 2>/dev/null || echo '{"slots":[]}')
        ;;
      tock)
        slug=$(echo "$entry" | jq -r '.slug')
        result=$(node "${SCRIPTS_DIR}/tock-check.js" "$slug" "$date" "$party_size" 2>/dev/null || echo '{"slots":[]}')
        ;;
    esac

    # Extract slots
    slots=$(echo "$result" | jq -c '.slots // []')
    slot_count=$(echo "$slots" | jq 'length')

    if [[ "$slot_count" -gt 0 ]]; then
      # Filter by preferred time window if set
      if [[ -n "$earliest" && -n "$latest" ]]; then
        slots=$(echo "$slots" | jq -c --arg e "$earliest" --arg l "$latest" '[
          .[] | select(
            (.time_start | split(" ") | last | split("T") | last | .[0:5]) as $t |
            $t >= $e and $t <= $l
          )
        ]')
        slot_count=$(echo "$slots" | jq 'length')
      fi
    fi

    if [[ "$slot_count" -gt 0 ]]; then
      total_with_availability=$((total_with_availability + 1))

      # Build a state key for deduplication
      state_key="${platform}:$(echo "$entry" | jq -r '.venue_id // .restaurant_id // .slug'):${date}"

      # Get previously seen slots for this key
      prev_slots=$(jq -c --arg key "$state_key" '.seen[$key] // []' "$STATE_FILE")

      # Find new slots (not in previous state)
      new_slots=$(jq -c --argjson prev "$prev_slots" '[
        .[] | . as $slot |
        if ($prev | map(.time_start) | index($slot.time_start)) then empty
        else $slot end
      ]' <<< "$slots")

      new_count=$(echo "$new_slots" | jq 'length')

      if [[ "$new_count" -gt 0 ]]; then
        # Build booking URL
        booking_url=""
        case "$platform" in
          resy)
            slug=$(echo "$result" | jq -r '.venue_slug // ""')
            city=$(echo "$result" | jq -r '.venue_city // "ny"' | tr '[:upper:]' '[:lower:]' | tr ' ' '-')
            booking_url="https://resy.com/cities/${city}/${slug}?date=${date}&seats=${party_size}"
            ;;
          opentable)
            rid=$(echo "$entry" | jq -r '.restaurant_id')
            booking_url="https://www.opentable.com/booking/widget?rid=${rid}&datetime=${date}T19:00&covers=${party_size}"
            ;;
          tock)
            tslug=$(echo "$entry" | jq -r '.slug')
            booking_url="https://www.exploretock.com/${tslug}/search?date=${date}&size=${party_size}"
            ;;
        esac

        entry_result=$(jq -n \
          --arg name "$name" \
          --arg platform "$platform" \
          --arg date "$date" \
          --argjson party_size "$party_size" \
          --argjson slots "$new_slots" \
          --arg url "$booking_url" \
          '{
            restaurant: $name,
            platform: $platform,
            date: $date,
            party_size: $party_size,
            slots: $slots,
            booking_url: $url
          }')

        all_results=$(echo "$all_results" | jq --argjson entry "$entry_result" '. += [$entry]')
      fi

      # Update state with current slots
      state_update=$(jq --arg key "$state_key" --argjson slots "$slots" --arg ts "$TIMESTAMP" '
        .seen[$key] = [$slots[] | . + {first_seen: $ts}]
      ' "$STATE_FILE")
      echo "$state_update" > "$STATE_FILE"
    fi

    # Rate limit: sleep between API calls
    sleep 2
  done
done

# Clean up expired entries from state (dates in the past)
jq --arg today "$TODAY" '
  .seen = (.seen | to_entries | map(
    select((.key | split(":") | last) >= $today)
  ) | from_entries)
' "$STATE_FILE" > "${STATE_FILE}.tmp" && mv "${STATE_FILE}.tmp" "$STATE_FILE"

# Output the report
jq -n \
  --arg ts "$TIMESTAMP" \
  --argjson results "$all_results" \
  --argjson checked "$total_checked" \
  --argjson avail "$total_with_availability" \
  '{
    timestamp: $ts,
    new_availability: $results,
    total_checked: $checked,
    total_with_availability: $avail
  }'
