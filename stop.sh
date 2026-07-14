#!/usr/bin/env bash

# Stops only processes started by run.sh. Ollama is intentionally left running.

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PID_DIR="$ROOT_DIR/.pids"

GREEN="\033[0;32m"
YELLOW="\033[1;33m"
NC="\033[0m"

ok() { printf "${GREEN}✓${NC} %s\n" "$1"; }
warn() { printf "${YELLOW}!${NC} %s\n" "$1"; }

stop_pid_file() {
  local label="$1"
  local pid_file="$2"

  if [[ ! -f "$pid_file" ]]; then
    warn "$label is not managed by run.sh"
    return
  fi

  local pid
  pid="$(cat "$pid_file")"
  if kill -0 "$pid" >/dev/null 2>&1; then
    kill "$pid" >/dev/null 2>&1 || true
    sleep 1
    if kill -0 "$pid" >/dev/null 2>&1; then
      kill -TERM "$pid" >/dev/null 2>&1 || true
    fi
    ok "Stopped $label (PID $pid)"
  else
    warn "$label PID was stale"
  fi

  rm -f "$pid_file"
}

main() {
  stop_pid_file "Backend" "$PID_DIR/backend.pid"
  stop_pid_file "SQL Backend" "$PID_DIR/sql_backend.pid"
  stop_pid_file "Frontend" "$PID_DIR/frontend.pid"

  rm -f "$PID_DIR/backend.log" "$PID_DIR/sql_backend.log" "$PID_DIR/frontend.log"
  rmdir "$PID_DIR" >/dev/null 2>&1 || true
  ok "Stopped managed CodeLens AI services. Ollama was left untouched."
}

main "$@"
