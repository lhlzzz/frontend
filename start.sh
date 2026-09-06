#!/usr/bin/env bash
# web — 启动 Hermes Social Media Console
set -euo pipefail

WEB_DIR="$(cd "$(dirname "$0")" && pwd)"
TARGET="${1:-social}"

port_pids() {
  local port="$1"
  if command -v lsof >/dev/null 2>&1; then
    lsof -tiTCP:"$port" -sTCP:LISTEN 2>/dev/null || true
  fi
  if command -v ss >/dev/null 2>&1; then
    ss -ltnpH "sport = :$port" 2>/dev/null \
      | sed -n 's/.*pid=\([0-9][0-9]*\).*/\1/p'
  fi
}

case "$TARGET" in
  social) PORT=4000 ;;
  financial) PORT=3000 ;;
  *) echo "Usage: $0 [social|financial]" >&2; exit 2 ;;
esac

PIDS="$(port_pids "$PORT" | sort -u)"
if [[ -n "$PIDS" ]]; then
  echo "Port $PORT is in use; releasing it..."
  kill $PIDS 2>/dev/null || true
  sleep 1
fi

if [[ "$TARGET" == "social" ]]; then
  cd "$WEB_DIR"
  echo "Starting Hermes Social Media OS on port 4000..."
  exec python3 -m uvicorn social_console.main:app --host 127.0.0.1 --port 4000
fi

echo "Starting Hermes Financial OS on port 3000..."
exec npm --prefix "$WEB_DIR/../financial-os" run start --workspace financial-os-web -- --port 3000
