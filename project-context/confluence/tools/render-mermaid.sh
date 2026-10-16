#!/usr/bin/env bash
# Render mọi *.mmd trong confluence/images thành PNG (scale 2, nền trắng).
# Cần: npm i -g @mermaid-js/mermaid-cli   (hoặc npx -y @mermaid-js/mermaid-cli)
set -uo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
IMG="${1:-$HERE/../images}"
MMDC="${MMDC:-$(command -v mmdc || echo "npx -y @mermaid-js/mermaid-cli")}"
ok=0; fail=0
for f in "$IMG"/*.mmd; do
  b="$(basename "$f" .mmd)"
  if $MMDC -i "$f" -o "$IMG/$b.png" -b white -s 2 \
        -p "$HERE/puppeteer.json" -c "$HERE/mermaid.json" >/dev/null 2>&1; then
    echo "OK   $b.png"; ok=$((ok+1))
  else
    echo "FAIL $b"; fail=$((fail+1))
  fi
done
echo "=== $ok ok, $fail fail ==="
