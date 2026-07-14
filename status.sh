#!/usr/bin/env bash

# Displays status for local CodeLens AI services and Ollama.

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PID_DIR="$ROOT_DIR/.pids"

GREEN="\033[0;32m"
RED="\033[0;31m"
NC="\033[0m"

is_running() {
  local pid="$1"
  [[ -n "$pid" ]] && kill -0 "$pid" >/dev/null 2>&1
}

print_status() {
  local label="$1"
  local pid_file="$2"

  if [[ -f "$pid_file" ]] && is_running "$(cat "$pid_file")"; then
    printf "%-12s ${GREEN}✓ Running${NC}\n" "$label"
  else
    printf "%-12s ${RED}✗ Not Running${NC}\n" "$label"
  fi
}

print_ollama_status() {
  if command -v ollama >/dev/null 2>&1 && ollama list >/dev/null 2>&1; then
    printf "%-12s ${GREEN}✓ Running${NC}\n" "Ollama"
  else
    printf "%-12s ${RED}✗ Not Running${NC}\n" "Ollama"
  fi
}

main() {
  print_status "Backend" "$PID_DIR/backend.pid"
  print_status "SQL Backend" "$PID_DIR/sql_backend.pid"
  print_status "Frontend" "$PID_DIR/frontend.pid"
  print_ollama_status
}

main "$@"
