#!/usr/bin/env bash
# 速卖通 API 的 curl 示例：所有能力都发到同一个地址，只换 action 和 params。
# curl examples for the AliExpress API: every capability uses the same URL; only action and params change.
#
#   export EVERYINFRA_API_KEY=<your API key>
#   bash examples/curl.sh search "wireless earbuds"
#   bash examples/curl.sh product_detail "<product url>" # search 结果里的 url / the url from a search result
#   bash examples/curl.sh reviews "<product url>"
#   bash examples/curl.sh variants "<product url>"
set -euo pipefail
: "${EVERYINFRA_API_KEY:?Set EVERYINFRA_API_KEY first: https://everyinfra.com/docs#quickstart}"
action=${1:?"usage: bash examples/curl.sh <search|product_detail|reviews|variants> <value>"}
value=${2:?"value: a keyword or a product url"}

case "$action" in
  search)                              params="{\"keyword\":\"$value\"}" ;;
  product_detail | reviews | variants) params="{\"url\":\"$value\"}" ;;
  *) echo "unknown action: $action (use search, product_detail, reviews or variants)" >&2; exit 2 ;;
esac

curl -sS -X POST https://api.everyinfra.com/api/v1/social \
  -H "Authorization: Bearer $EVERYINFRA_API_KEY" \
  -H "Content-Type: application/json" \
  -d "{\"platform\":\"aliexpress\",\"action\":\"$action\",\"params\":$params}"
echo
