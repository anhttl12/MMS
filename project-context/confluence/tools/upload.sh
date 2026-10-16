#!/usr/bin/env bash
# TÙY CHỌN — đẩy 1 trang lên Confluence Cloud qua REST API (tạo mới hoặc cập nhật)
# rồi upload kèm mọi ảnh sơ đồ của trang đó làm attachment.
#
#   export CONF_BASE="https://<site>.atlassian.net/wiki"
#   export CONF_USER="ban@viettel.com.vn"
#   export CONF_TOKEN="<API token: id.atlassian.com/manage-profile/security/api-tokens>"
#   export CONF_SPACE="MMS"
#   ./upload.sh PeyeHaiti_PRD "PRD — Giải pháp Merchant Peye-Haiti" [PARENT_PAGE_ID]
#
# Ghi chú: script GHI dữ liệu lên Confluence. Kiểm tra biến môi trường trước khi chạy.
set -euo pipefail
: "${CONF_BASE:?}" "${CONF_USER:?}" "${CONF_TOKEN:?}" "${CONF_SPACE:?}"
SLUG="${1:?slug, vd PeyeHaiti_PRD}"; TITLE="${2:?tiêu đề trang}"; PARENT="${3:-}"
HERE="$(cd "$(dirname "$0")" && pwd)"; OUT="$HERE/.."
AUTH=(-u "$CONF_USER:$CONF_TOKEN" -H 'Content-Type: application/json')
BODY="$(python3 -c 'import json,sys;print(json.dumps(open(sys.argv[1],encoding="utf-8").read()))' "$OUT/$SLUG.storage.html")"

EXIST="$(curl -s "${AUTH[@]}" --get "$CONF_BASE/rest/api/content" \
  --data-urlencode "spaceKey=$CONF_SPACE" --data-urlencode "title=$TITLE" \
  --data-urlencode 'expand=version')"
PID="$(python3 -c 'import json,sys;r=json.load(sys.stdin)["results"];print(r[0]["id"] if r else "")' <<<"$EXIST")"
VER="$(python3 -c 'import json,sys;r=json.load(sys.stdin)["results"];print(r[0]["version"]["number"] if r else 0)' <<<"$EXIST")"

if [ -n "$PID" ]; then
  echo "→ cập nhật page $PID (v$((VER+1)))"
  curl -s "${AUTH[@]}" -X PUT "$CONF_BASE/rest/api/content/$PID" -d @- >/dev/null <<JSON
{"id":"$PID","type":"page","title":$(python3 -c 'import json,sys;print(json.dumps(sys.argv[1]))' "$TITLE"),
 "space":{"key":"$CONF_SPACE"},"version":{"number":$((VER+1))},
 "body":{"storage":{"value":$BODY,"representation":"storage"}}}
JSON
else
  echo "→ tạo page mới"
  ANC=""; [ -n "$PARENT" ] && ANC=",\"ancestors\":[{\"id\":\"$PARENT\"}]"
  PID="$(curl -s "${AUTH[@]}" -X POST "$CONF_BASE/rest/api/content" -d @- <<JSON | python3 -c 'import json,sys;print(json.load(sys.stdin)["id"])'
{"type":"page","title":$(python3 -c 'import json,sys;print(json.dumps(sys.argv[1]))' "$TITLE"),
 "space":{"key":"$CONF_SPACE"}$ANC,
 "body":{"storage":{"value":$BODY,"representation":"storage"}}}
JSON
)"
  echo "  page id = $PID"
fi

shopt -s nullglob
for img in "$OUT/images/$SLUG-diagram-"*.png; do
  echo "  ↑ $(basename "$img")"
  curl -s -u "$CONF_USER:$CONF_TOKEN" -H 'X-Atlassian-Token: no-check' \
    -X PUT "$CONF_BASE/rest/api/content/$PID/child/attachment" \
    -F "file=@$img" -F 'minorEdit=true' >/dev/null
done
echo "✓ xong: $CONF_BASE/pages/viewpage.action?pageId=$PID"
