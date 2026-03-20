#!/usr/bin/env bash
set -euo pipefail

VERSION="3.0.0"
BRAND="Powered by BytesAgain | bytesagain.com | hello@bytesagain.com"
DATA_DIR="${HOME}/.local/share/liquidity-monitor"
ALERTS_FILE="${DATA_DIR}/alerts.jsonl"
HISTORY_FILE="${DATA_DIR}/history.jsonl"
API_BASE="https://api.llama.fi"

mkdir -p "$DATA_DIR"
touch "$ALERTS_FILE" "$HISTORY_FILE"

# ── helpers ──────────────────────────────────────────────────────────────────
die() { echo "❌ $*" >&2; exit 1; }
ts() { date -u +"%Y-%m-%dT%H:%M:%SZ"; }

json_escape() {
  local s="$1"
  s="${s//\\/\\\\}"
  s="${s//\"/\\\"}"
  printf '%s' "$s"
}

format_usd() {
  local val="$1"
  # Handle scientific notation and large numbers
  awk "BEGIN { printf \"$%.2f\", ${val} }" 2>/dev/null || echo "\$${val}"
}

format_big() {
  local val="$1"
  awk "BEGIN {
    v = ${val} + 0
    if (v >= 1000000000) printf \"$%.2fB\", v/1000000000
    else if (v >= 1000000) printf \"$%.2fM\", v/1000000
    else if (v >= 1000) printf \"$%.2fK\", v/1000
    else printf \"$%.2f\", v
  }" 2>/dev/null || echo "\$${val}"
}

api_get() {
  local endpoint="$1"
  local result
  result=$(curl -s --max-time 15 "${API_BASE}${endpoint}" 2>/dev/null) || die "API request failed. Check connectivity."
  [[ -z "$result" ]] && die "Empty API response"
  echo "$result"
}

show_help() {
  cat <<EOF
╔══════════════════════════════════════════════════════╗
║        💧  Liquidity Monitor v${VERSION}               ║
╚══════════════════════════════════════════════════════╝

Usage: script.sh <command> [args...]

Commands:
  pool <pair>          Search for pool/pair info (e.g. ETH-USDC)
  tvl <protocol>       Show TVL for a protocol (e.g. uniswap, aave)
  top [count]          Show top protocols by TVL (default: 10)
  alerts               Show saved alerts
  history <pool>       Show local price/TVL history log
  yield <pool>         Search yield/APY data for a pool
  help                 Show this help
  version              Show version

Data source: DeFiLlama API (free, no key required)

Examples:
  script.sh tvl uniswap
  script.sh top 20
  script.sh pool ETH-USDC
  script.sh yield ETH

${BRAND}
EOF
}

# ── commands ─────────────────────────────────────────────────────────────────
cmd_pool() {
  local pair="${1:-}"
  [[ -z "$pair" ]] && die "Usage: pool <pair>  (e.g. ETH-USDC, WBTC)"

  echo "🔍 Searching pools for: ${pair}..."
  local data
  data=$(api_get "/protocols")

  # Search protocols whose name or symbol matches
  local search_term="${pair,,}"
  search_term="${search_term//-/ }"

  echo "╔══════════════════════════════════════════════════════════════╗"
  echo "║                  💧 Pool Search: ${pair}                     "
  echo "╠══════════════════════════════════════════════════════════════╣"

  local count=0
  # Parse JSON array — extract matching protocols
  echo "$data" | tr ',' '\n' | grep -i "\"name\"\|\"tvl\"\|\"symbol\"\|\"chain\"" | while read -r field; do
    if echo "$field" | grep -qi "\"name\".*${search_term}\|\"symbol\".*${search_term}"; then
      (( count++ )) || true
      local name tvl chain
      name=$(echo "$field" | sed 's/.*"name":"\([^"]*\)".*/\1/' 2>/dev/null || echo "$field")
      printf "║  Found: %-50s ║\n" "$name"
    fi
  done

  # Log to history
  echo "{\"query\":\"pool:${pair}\",\"timestamp\":\"$(ts)\"}" >> "$HISTORY_FILE"

  echo "╚══════════════════════════════════════════════════════════════╝"
  echo ""
  echo "  💡 Tip: Use 'tvl <protocol>' for detailed TVL data"
}

cmd_tvl() {
  local protocol="${1:-}"
  [[ -z "$protocol" ]] && die "Usage: tvl <protocol>  (e.g. uniswap, aave, lido)"

  echo "📊 Fetching TVL for: ${protocol}..."
  local data
  data=$(api_get "/protocol/${protocol}") || die "Protocol '${protocol}' not found"

  # Extract key metrics
  local name tvl chain description
  name=$(echo "$data" | grep -oP '"name"\s*:\s*"[^"]*"' | head -1 | sed 's/.*"name"\s*:\s*"\([^"]*\)".*/\1/') || name="$protocol"
  tvl=$(echo "$data" | grep -oP '"tvl"\s*:\s*[0-9.e+]*' | head -1 | sed 's/.*"tvl"\s*:\s*//') || tvl="N/A"
  description=$(echo "$data" | grep -oP '"description"\s*:\s*"[^"]*"' | head -1 | sed 's/.*"description"\s*:\s*"\([^"]*\)".*/\1/' | cut -c1-80) || description=""

  local chains
  chains=$(echo "$data" | grep -oP '"chains"\s*:\s*\[[^\]]*\]' | head -1 | sed 's/"chains"\s*:\s*\[//;s/\]//;s/"//g') || chains=""

  local formatted_tvl
  formatted_tvl=$(format_big "$tvl" 2>/dev/null || echo "$tvl")

  echo "╔══════════════════════════════════════════════════════════════╗"
  echo "║                    📊 Protocol TVL                           ║"
  echo "╠══════════════════════════════════════════════════════════════╣"
  printf "║  Name:        %-45s║\n" "$name"
  printf "║  TVL:         %-45s║\n" "$formatted_tvl"
  printf "║  Chains:      %-45s║\n" "${chains:-(unknown)}"
  if [[ -n "$description" ]]; then
    printf "║  Description: %-45s║\n" "$description"
  fi
  echo "╚══════════════════════════════════════════════════════════════╝"

  # Log
  echo "{\"query\":\"tvl:${protocol}\",\"tvl\":\"${tvl}\",\"timestamp\":\"$(ts)\"}" >> "$HISTORY_FILE"
}

cmd_top() {
  local count="${1:-10}"
  [[ "$count" =~ ^[0-9]+$ ]] || die "Count must be a number"
  (( count > 100 )) && count=100

  echo "🏆 Fetching top ${count} protocols by TVL..."
  local data
  data=$(api_get "/protocols")

  echo "╔══════════════════════════════════════════════════════════════════╗"
  echo "║                  🏆 Top Protocols by TVL                        ║"
  echo "╠══════════════════════════════════════════════════════════════════╣"
  printf "║ %4s │ %-25s │ %-15s │ %-12s ║\n" "Rank" "Protocol" "TVL" "Chain"
  echo "╠══════════════════════════════════════════════════════════════════╣"

  # Parse the JSON array — extract name, tvl, chain for top N
  # DeFiLlama returns protocols sorted by TVL descending
  local idx=0
  local current_name="" current_tvl="" current_chain=""

  echo "$data" | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    for i, p in enumerate(data[:${count}]):
        name = p.get('name', 'Unknown')[:25]
        tvl = p.get('tvl', 0)
        chain = p.get('chain', p.get('chains', ['?'])[0] if isinstance(p.get('chains'), list) and p.get('chains') else 'Multi')
        if isinstance(chain, list): chain = chain[0] if chain else 'Multi'
        chain = str(chain)[:12]
        if tvl >= 1e9:
            tvl_s = '\$%.2fB' % (tvl/1e9)
        elif tvl >= 1e6:
            tvl_s = '\$%.2fM' % (tvl/1e6)
        elif tvl >= 1e3:
            tvl_s = '\$%.2fK' % (tvl/1e3)
        else:
            tvl_s = '\$%.2f' % tvl
        print('║ %4d │ %-25s │ %15s │ %-12s ║' % (i+1, name, tvl_s, chain))
except Exception as e:
    print('║  Error parsing data: %s' % str(e))
" 2>/dev/null || echo "║  (Install python3 for formatted output or check connectivity)     ║"

  echo "╚══════════════════════════════════════════════════════════════════╝"
  echo "  Source: DeFiLlama API | $(date -u +%Y-%m-%d' '%H:%M' UTC')"
}

cmd_alerts() {
  if [[ ! -s "$ALERTS_FILE" ]]; then
    echo "🔔 No alerts configured."
    echo ""
    echo "  To add alerts, manually add JSONL entries to:"
    echo "  ${ALERTS_FILE}"
    echo ""
    echo "  Format: {\"protocol\":\"name\",\"metric\":\"tvl\",\"threshold\":1000000,\"direction\":\"below\"}"
    return
  fi

  echo "🔔 Saved Alerts"
  echo "════════════════════════════════════════"

  local count=0
  while IFS= read -r line; do
    local protocol metric threshold direction
    protocol=$(echo "$line" | sed 's/.*"protocol":"\([^"]*\)".*/\1/' 2>/dev/null) || protocol="?"
    metric=$(echo "$line" | sed 's/.*"metric":"\([^"]*\)".*/\1/' 2>/dev/null) || metric="?"
    threshold=$(echo "$line" | sed 's/.*"threshold":\([0-9.]*\).*/\1/' 2>/dev/null) || threshold="?"
    direction=$(echo "$line" | sed 's/.*"direction":"\([^"]*\)".*/\1/' 2>/dev/null) || direction="?"

    (( count++ )) || true
    echo "  [${count}] ${protocol}: alert when ${metric} goes ${direction} $(format_big "$threshold" 2>/dev/null || echo "$threshold")"
  done < "$ALERTS_FILE"

  echo ""
  echo "  Total: ${count} alert(s)"
}

cmd_history() {
  local pool="${1:-}"

  if [[ ! -s "$HISTORY_FILE" ]]; then
    echo "📜 No history logged yet."
    return
  fi

  echo "📜 Query History"
  echo "════════════════════════════════════════"

  if [[ -n "$pool" ]]; then
    grep -i "$pool" "$HISTORY_FILE" | tail -20 | while IFS= read -r line; do
      local query timestamp
      query=$(echo "$line" | sed 's/.*"query":"\([^"]*\)".*/\1/')
      timestamp=$(echo "$line" | sed 's/.*"timestamp":"\([^"]*\)".*/\1/')
      echo "  [${timestamp}] ${query}"
    done
  else
    tail -20 "$HISTORY_FILE" | while IFS= read -r line; do
      local query timestamp
      query=$(echo "$line" | sed 's/.*"query":"\([^"]*\)".*/\1/')
      timestamp=$(echo "$line" | sed 's/.*"timestamp":"\([^"]*\)".*/\1/')
      echo "  [${timestamp}] ${query}"
    done
  fi
}

cmd_yield() {
  local pool="${1:-}"
  [[ -z "$pool" ]] && die "Usage: yield <pool>  (e.g. ETH, USDC, WBTC)"

  echo "📈 Searching yield data for: ${pool}..."

  local data
  data=$(curl -s --max-time 15 "https://yields.llama.fi/pools" 2>/dev/null) || die "API request failed"

  echo "╔══════════════════════════════════════════════════════════════════════╗"
  printf "║                   📈 Yield Search: %-15s                   ║\n" "$pool"
  echo "╠══════════════════════════════════════════════════════════════════════╣"
  printf "║ %-20s │ %-10s │ %10s │ %12s │ %-8s ║\n" "Pool" "Chain" "APY" "TVL" "Project"
  echo "╠══════════════════════════════════════════════════════════════════════╣"

  echo "$data" | python3 -c "
import sys, json
try:
    resp = json.load(sys.stdin)
    pools = resp.get('data', []) if isinstance(resp, dict) else resp
    matches = []
    search = '${pool}'.upper()
    for p in pools:
        sym = str(p.get('symbol', '')).upper()
        if search in sym:
            matches.append(p)
    matches.sort(key=lambda x: x.get('tvlUsd', 0), reverse=True)
    for p in matches[:15]:
        name = str(p.get('symbol', '?'))[:20]
        chain = str(p.get('chain', '?'))[:10]
        apy = p.get('apy', 0)
        tvl = p.get('tvlUsd', 0)
        project = str(p.get('project', '?'))[:8]
        if tvl >= 1e9: tvl_s = '\$%.1fB' % (tvl/1e9)
        elif tvl >= 1e6: tvl_s = '\$%.1fM' % (tvl/1e6)
        elif tvl >= 1e3: tvl_s = '\$%.1fK' % (tvl/1e3)
        else: tvl_s = '\$%.0f' % tvl
        print('║ %-20s │ %-10s │ %9.2f%% │ %12s │ %-8s ║' % (name, chain, apy or 0, tvl_s, project))
    if not matches:
        print('║  No pools found matching: ${pool}')
except Exception as e:
    print('║  Error: %s' % str(e))
" 2>/dev/null || echo "║  (Install python3 for formatted output)                                    ║"

  echo "╚══════════════════════════════════════════════════════════════════════╝"
  echo "  Source: DeFiLlama Yields API | $(date -u +%Y-%m-%d' '%H:%M' UTC')"

  # Log
  echo "{\"query\":\"yield:${pool}\",\"timestamp\":\"$(ts)\"}" >> "$HISTORY_FILE"
}

# ── main ─────────────────────────────────────────────────────────────────────
cmd="${1:-help}"
shift || true

case "$cmd" in
  pool)    cmd_pool "$@" ;;
  tvl)     cmd_tvl "$@" ;;
  top)     cmd_top "$@" ;;
  alerts)  cmd_alerts ;;
  history) cmd_history "$@" ;;
  yield)   cmd_yield "$@" ;;
  version) echo "Liquidity Monitor v${VERSION}" ;;
  help|*)  show_help ;;
esac
