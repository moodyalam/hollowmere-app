#!/usr/bin/env bash
# Lecturer only: start the stack with the phone tunnel, then print the public
# address and open the crew screen (the QR code) on it.
#   cd ops && ./phones.sh
set -euo pipefail
cd "$(dirname "$0")"
docker compose --profile phones up -d
echo "Waiting for the tunnel's address..."
for _ in $(seq 1 30); do
  url=$(docker compose logs tunnel 2>/dev/null | grep -Eo 'https://[a-z0-9-]+\.trycloudflare\.com' | tail -1 || true)
  [ -n "$url" ] && break
  sleep 1
done
if [ -z "${url:-}" ]; then
  echo "No tunnel address after 30 s. Check: docker compose logs tunnel" >&2
  echo "Fallback: Cloud Run (ops/cloudrun/README.md) or laptop only (the crowd service keeps the graphs alive)." >&2
  exit 1
fi
echo "Phones join at: $url/join"
echo "Crew screen:    $url/crew"
# Open the crew screen in the default browser (macOS: open; Linux: xdg-open).
(open "$url/crew" 2>/dev/null || xdg-open "$url/crew" 2>/dev/null || true)
