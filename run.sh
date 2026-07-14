#!/usr/bin/env bash

# Starts CodeLens AI local services started by this script only.
# Ollama is required, but intentionally not launched here.

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PID_DIR="$ROOT_DIR/.pids"

RED="\033[0;31m"
GREEN="\033[0;32m"
YELLOW="\033[1;33m"
BLUE="\033[0;34m"
NC="\033[0m"

ok() { printf "${GREEN}✓${NC} %s\n" "$1"; }
warn() { printf "${YELLOW}!${NC} %s\n" "$1"; }
fail() { printf "${RED}✗${NC} %s\n" "$1"; exit 1; }

is_running() {
  local pid="$1"
  [[ -n "$pid" ]] && kill -0 "$pid" >/dev/null 2>&1
}

start_service() {
  local name="$1"
  local pid_file="$2"
  local workdir="$3"
  shift 3

  if [[ -f "$pid_file" ]]; then
    local existing_pid
    existing_pid="$(cat "$pid_file")"
    if is_running "$existing_pid"; then
      ok "$name already running (PID $existing_pid)"
      return
    fi
    warn "Removing stale PID file for $name"
    rm -f "$pid_file"
  fi

  (
    cd "$workdir"
    "$@"
  ) > "$PID_DIR/${name}.log" 2>&1 &
  local pid=$!
  printf "%s\n" "$pid" > "$pid_file"
  ok "Started $name (PID $pid)"
}

main() {
  cd "$ROOT_DIR"

  if ! command -v ollama >/dev/null 2>&1 || ! ollama list >/dev/null 2>&1; then
    printf "${RED}Ollama is not running.${NC}\n"
    printf "Please start it using:\n\n"
    printf "${BLUE}ollama serve${NC}\n"
    exit 1
  fi

  [[ -d "$ROOT_DIR/backend/.venv" ]] || fail "backend/.venv is missing. Run ./setup.sh first."
  [[ -d "$ROOT_DIR/sql_backend/.venv" ]] || fail "sql_backend/.venv is missing. Run ./setup.sh first."
  [[ -d "$ROOT_DIR/frontend/node_modules" ]] || fail "frontend/node_modules is missing. Run ./setup.sh first."

  mkdir -p "$PID_DIR"

  start_service "backend" "$PID_DIR/backend.pid" "$ROOT_DIR/backend" \
    .venv/bin/python -m uvicorn app.main:app --host 127.0.0.1 --port 8000

  start_service "sql_backend" "$PID_DIR/sql_backend.pid" "$ROOT_DIR/sql_backend" \
    .venv/bin/python -m uvicorn app.main:app --host 127.0.0.1 --port 8001

  start_service "frontend" "$PID_DIR/frontend.pid" "$ROOT_DIR/frontend" \
    npm run dev -- --hostname 127.0.0.1 --port 3000

  printf "\n${GREEN}CodeLens AI is starting.${NC}\n"
  printf "Frontend URL:   ${BLUE}http://localhost:3000${NC}\n"
  printf "Python API URL: ${BLUE}http://localhost:8000${NC}\n"
  printf "SQL API URL:    ${BLUE}http://localhost:8001${NC}\n"
  printf "\nLogs are in ${BLUE}.pids/*.log${NC}\n"
}

main "$@"
