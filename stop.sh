#!/usr/bin/env bash
# web — 停止 Hermes Social Media Console
set -euo pipefail

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
  echo "Stopping $TARGET on port $PORT..."
  kill $PIDS 2>/dev/null || true
  echo "✓ Stopped."
else
  echo "web is not running."
fi
