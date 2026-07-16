#!/usr/bin/env bash

# Optional CodeLens AI cleanup helper.
# Frees only the local ports used by this project after user confirmation.

set -euo pipefail

RED="\033[0;31m"
GREEN="\033[0;32m"
YELLOW="\033[1;33m"
NC="\033[0m"

ok() { printf "${GREEN}✓${NC} %s\n" "$1"; }
warn() { printf "${YELLOW}!${NC} %s\n" "$1"; }
fail() { printf "${RED}✗${NC} %s\n" "$1"; exit 1; }

PORTS=(3000 8000 8001)

main() {
  if ! command -v lsof >/dev/null 2>&1; then
    fail "lsof is required but was not found in PATH."
  fi

  local rows=()
  local seen_pids=" "
  local port

  for port in "${PORTS[@]}"; do
    # The -t flag is not used because the confirmation table also needs
    # a readable process name, not just a PID.
    while IFS= read -r line; do
      [[ -n "$line" ]] || continue

      local pid
      local process
      pid="$(awk '{print $2}' <<< "$line")"
      process="$(awk '{print $1}' <<< "$line")"

      [[ -n "$pid" && -n "$process" ]] || continue

      if [[ "$seen_pids" == *" $pid "* ]]; then
        continue
      fi

      seen_pids+="$pid "
      rows+=("$port|$pid|$process")
    done < <(lsof -nP -iTCP:"$port" -sTCP:LISTEN 2>/dev/null | awk 'NR > 1' || true)
  done

  if [[ "${#rows[@]}" -eq 0 ]]; then
    ok "No processes found using CodeLens AI ports."
    exit 0
  fi

  printf "%-8s %-8s %s\n" "Port" "PID" "Process"
  printf "%-8s %-8s %s\n" "--------" "--------" "----------------"

  local row
  for row in "${rows[@]}"; do
    IFS="|" read -r port pid process <<< "$row"
    printf "%-8s %-8s %s\n" "$port" "$pid" "$process"
  done

  printf "\n${YELLOW}Kill these processes? (y/N):${NC} "
  local answer
  read -r answer

  if [[ "$answer" != "y" ]]; then
    warn "Cleanup cancelled."
    exit 0
  fi

  for row in "${rows[@]}"; do
    IFS="|" read -r _ pid _ <<< "$row"
    if kill -0 "$pid" >/dev/null 2>&1; then
      kill "$pid" >/dev/null 2>&1 || true
      ok "Killed PID $pid"
    else
      warn "PID $pid already terminated"
    fi
  done

  ok "Cleanup complete."
}

main "$@"
