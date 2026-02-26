#!/usr/bin/env bash
# Deployment verification script for Bot Monitoring Dashboard
# Usage: DASHBOARD_URL=https://dashboard.a2xautonomy.com ./scripts/verify_deployment.sh

set -euo pipefail

URL="${DASHBOARD_URL:-http://localhost:8000}"
USER="${DASHBOARD_USER:-admin}"
PASS="${DASHBOARD_PASS:-changeme}"

pass=0
fail=0

check() {
    local desc="$1"
    local result="$2"
    if [ "$result" = "0" ]; then
        echo "  [PASS] $desc"
        ((pass++))
    else
        echo "  [FAIL] $desc"
        ((fail++))
    fi
}

echo "=== Bot Dashboard Deployment Verification ==="
echo "URL: $URL"
echo ""

# 1. Backend health
echo "--- Backend ---"
status=$(curl -s -o /dev/null -w "%{http_code}" "$URL/api/bots" -u "$USER:$PASS" 2>/dev/null || echo "000")
check "GET /api/bots returns 200" "$([ "$status" = "200" ] && echo 0 || echo 1)"

status=$(curl -s -o /dev/null -w "%{http_code}" "$URL/api/bots" 2>/dev/null || echo "000")
check "GET /api/bots without auth returns 401" "$([ "$status" = "401" ] && echo 0 || echo 1)"

# 2. Registration
echo ""
echo "--- Registration ---"
reg_response=$(curl -s -X POST "$URL/api/register" \
    -H "Content-Type: application/json" \
    -d '{"name":"Verify Bot","bot_class":"test"}' \
    -u "$USER:$PASS" 2>/dev/null || echo "{}")
bot_id=$(echo "$reg_response" | python3 -c "import sys,json; print(json.load(sys.stdin).get('bot_id',''))" 2>/dev/null || echo "")
token=$(echo "$reg_response" | python3 -c "import sys,json; print(json.load(sys.stdin).get('token',''))" 2>/dev/null || echo "")
check "POST /api/register creates bot" "$([ -n "$bot_id" ] && echo 0 || echo 1)"

# 3. Ingestion
echo ""
echo "--- Ingestion ---"
if [ -n "$token" ]; then
    ingest_status=$(curl -s -o /dev/null -w "%{http_code}" -X POST "$URL/api/ingest" \
        -H "Content-Type: application/json" \
        -H "Authorization: Bearer $token" \
        -d "[{\"timestamp\":\"$(date -u +%Y-%m-%dT%H:%M:%SZ)\",\"bot_id\":\"$bot_id\",\"event_type\":\"heartbeat\",\"payload\":{\"uptime_seconds\":1}}]" \
        2>/dev/null || echo "000")
    check "POST /api/ingest with valid token returns 200" "$([ "$ingest_status" = "200" ] && echo 0 || echo 1)"
fi

ingest_bad=$(curl -s -o /dev/null -w "%{http_code}" -X POST "$URL/api/ingest" \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer invalidtoken" \
    -d "[{\"timestamp\":\"2026-01-01T00:00:00Z\",\"bot_id\":\"fake\",\"event_type\":\"heartbeat\",\"payload\":{}}]" \
    2>/dev/null || echo "000")
check "POST /api/ingest with bad token returns 401" "$([ "$ingest_bad" = "401" ] && echo 0 || echo 1)"

# 4. Bot detail
echo ""
echo "--- Bot Detail ---"
if [ -n "$bot_id" ]; then
    detail_status=$(curl -s -o /dev/null -w "%{http_code}" "$URL/api/bots/$bot_id" -u "$USER:$PASS" 2>/dev/null || echo "000")
    check "GET /api/bots/:id returns 200" "$([ "$detail_status" = "200" ] && echo 0 || echo 1)"
fi

# 5. Frontend
echo ""
echo "--- Frontend ---"
fe_status=$(curl -s -o /dev/null -w "%{http_code}" "$URL/" 2>/dev/null || echo "000")
check "GET / serves frontend (200 or 404 if not built)" "$([ "$fe_status" = "200" ] || [ "$fe_status" = "404" ] && echo 0 || echo 1)"

# Summary
echo ""
echo "=== Results: $pass passed, $fail failed ==="
exit "$fail"
