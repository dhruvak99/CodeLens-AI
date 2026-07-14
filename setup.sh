#!/usr/bin/env bash

# CodeLens AI setup script.
# Idempotently prepares Python backends, the Next.js frontend, env files,
# and required Ollama models for local development.

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

RED="\033[0;31m"
GREEN="\033[0;32m"
YELLOW="\033[1;33m"
BLUE="\033[0;34m"
NC="\033[0m"

info() { printf "${BLUE}==>${NC} %s\n" "$1"; }
ok() { printf "${GREEN}✓${NC} %s\n" "$1"; }
warn() { printf "${YELLOW}!${NC} %s\n" "$1"; }
fail() { printf "${RED}✗${NC} %s\n" "$1"; exit 1; }

require_command() {
  local command_name="$1"
  local display_name="$2"
  if ! command -v "$command_name" >/dev/null 2>&1; then
    fail "$display_name is required but was not found in PATH."
  fi
  ok "$display_name found"
}

python_command() {
  if command -v python3 >/dev/null 2>&1; then
    printf "python3"
    return
  fi
  if command -v python >/dev/null 2>&1; then
    printf "python"
    return
  fi
  fail "Python 3.11+ is required but was not found."
}

verify_python() {
  local py
  py="$(python_command)"
  if ! "$py" - <<'PY'
import sys
if sys.version_info < (3, 11):
    raise SystemExit(1)
PY
  then
    fail "Python 3.11+ is required."
  fi
  ok "Python 3.11+ found ($("$py" --version 2>&1))"
}

create_file_if_missing() {
  local target="$1"
  local content="$2"
  if [[ -f "$target" ]]; then
    ok "$target already exists"
    return
  fi
  printf "%s\n" "$content" > "$target"
  ok "Created $target"
}

copy_env_example_if_missing() {
  local example="$1"
  local target="$2"
  if [[ -f "$target" ]]; then
    ok "$target already exists"
    return
  fi
  if [[ -f "$example" ]]; then
    cp "$example" "$target"
    ok "Created $target from $example"
  else
    warn "$example is missing; creating $target from defaults"
  fi
}

install_python_project() {
  local project_dir="$1"
  local install_command="$2"
  local py
  py="$(python_command)"

  info "Preparing $project_dir"
  cd "$ROOT_DIR/$project_dir"
  if [[ ! -d ".venv" ]]; then
    "$py" -m venv .venv
    ok "Created $project_dir/.venv"
  else
    ok "$project_dir/.venv already exists"
  fi

  .venv/bin/python -m pip install --upgrade pip
  eval "$install_command"
  ok "Installed dependencies for $project_dir"
}

ollama_model_installed() {
  local model="$1"
  ollama list 2>/dev/null | awk 'NR > 1 {print $1}' | grep -Fxq "$model"
}

pull_ollama_model_if_missing() {
  local model="$1"
  if ollama_model_installed "$model"; then
    ok "Ollama model $model already exists"
    return
  fi
  info "Pulling Ollama model $model"
  ollama pull "$model"
  ok "Pulled Ollama model $model"
}

main() {
  cd "$ROOT_DIR"
  local ollama_models_skipped=false

  info "Checking required tools"
  verify_python
  require_command node "Node.js"
  require_command npm "npm"
  require_command git "Git"
  require_command ollama "Ollama"
  if ! ollama list >/dev/null 2>&1; then
    warn "Ollama is installed but is not currently running. Skipping model download."
    ollama_models_skipped=true
  fi

  info "Creating environment files without overwriting existing files"
  create_file_if_missing "$ROOT_DIR/backend/.env.example" "OLLAMA_URL=http://localhost:11434
OLLAMA_MODEL=qwen3:4b"
  copy_env_example_if_missing "$ROOT_DIR/backend/.env.example" "$ROOT_DIR/backend/.env"

  create_file_if_missing "$ROOT_DIR/sql_backend/.env.example" "APP_NAME=SemanticSQL API
ENVIRONMENT=development
API_V1_PREFIX=/api/v1
REDIS_URL=redis://localhost:6379/0
SEMANTIC_CACHE_SIMILARITY_THRESHOLD=0.9
SEMANTIC_CACHE_MODEL_NAME=all-MiniLM-L6-v2
LLM_MODEL=llama3.1:8b
BACKEND_CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:3000,http://localhost:5173,http://127.0.0.1:5173,http://localhost:5174,http://127.0.0.1:5174"
  copy_env_example_if_missing "$ROOT_DIR/sql_backend/.env.example" "$ROOT_DIR/sql_backend/.env"

  create_file_if_missing "$ROOT_DIR/frontend/.env.example" "NEXT_PUBLIC_CODELENS_API=http://localhost:8000
NEXT_PUBLIC_SQL_API=http://localhost:8001"
  copy_env_example_if_missing "$ROOT_DIR/frontend/.env.example" "$ROOT_DIR/frontend/.env.local"

  install_python_project "backend" ".venv/bin/python -m pip install -e ."
  install_python_project "sql_backend" ".venv/bin/python -m pip install -r requirements.txt"

  info "Installing frontend dependencies"
  cd "$ROOT_DIR/frontend"
  npm install
  ok "Installed frontend dependencies"

  if [[ "$ollama_models_skipped" == false ]]; then
    info "Checking Ollama models"
    pull_ollama_model_if_missing "llama3.1"
    pull_ollama_model_if_missing "qwen2.5:7b"
  fi

  if [[ "$ollama_models_skipped" == true ]]; then
    printf "\n${GREEN}====================================${NC}\n\n"
    printf "${GREEN}Setup Complete${NC}\n\n"
    printf "${YELLOW}Ollama models were not installed because the Ollama server was not running.${NC}\n\n"
    printf "To finish setup:\n\n"
    printf "1. Start Ollama\n\n"
    printf "    ${BLUE}ollama serve${NC}\n\n"
    printf "2. Pull the required models\n\n"
    printf "    ${BLUE}ollama pull llama3.1${NC}\n"
    printf "    ${BLUE}ollama pull qwen2.5:7b${NC}\n\n"
    printf "Then run:\n\n"
    printf "    ${BLUE}./run.sh${NC}\n\n"
    printf "${GREEN}====================================${NC}\n"
  else
    printf "\n${GREEN}CodeLens AI setup complete.${NC}\n"
    printf "Start Ollama with: ${BLUE}ollama serve${NC}\n"
    printf "Run the app with: ${BLUE}./run.sh${NC}\n"
  fi
}

main "$@"
