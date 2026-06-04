#!/bin/bash
#
# NEBians real-time (WebSocket) server bootstrap.
#
# Installs daphne + cloudflared, then starts them as background processes
# that survive the SSH session. Adds @reboot crontab entries so they
# automatically come back after a server restart.
#
# Two WebSocket endpoint options are supported:
#   1. Cloudflare quick tunnel (default — no account required)
#      → URL like https://xxx.trycloudflare.com (changes on restart)
#   2. Cloudflare named tunnel (stable URL — set CLOUDFLARED_TUNNEL=nebians-ws)
#      → URL like https://ws.nebians.consica.com.np (persistent)
#
# Usage:
#   bash setup_realtime.sh                 # quick tunnel (default)
#   CLOUDFLARED_TUNNEL=nebians-ws bash setup_realtime.sh   # named tunnel
#
# Idempotent — safe to re-run.
#
set -e

PROJECT_DIR="/home/consicac/nebians_api"
VENV_DIR="/home/consicac/virtualenv/nebians_api/3.13"
LOG_DIR="$PROJECT_DIR/logs"
DAPHNE_LOG="$LOG_DIR/daphne.log"
CLOUDFLARED_LOG="$LOG_DIR/cloudflared.log"
DAPHNE_PORT="${DAPHNE_PORT:-8001}"
CLOUDFLARED_CONFIG="$HOME/.cloudflared/config.yml"
NAMED_TUNNEL="${CLOUDFLARED_TUNNEL:-}"

mkdir -p "$LOG_DIR" "$HOME/.cloudflared"

echo "=== Step 1/5: Install Python deps ==="
"$VENV_DIR/bin/pip" install --quiet 'channels==4.2.0' 'channels-redis==4.2.1' 'daphne==4.1.2'

echo "=== Step 2/5: Stop any running daphne ==="
pkill -f "daphne -b 127.0.0.1 -p $DAPHNE_PORT" 2>/dev/null || true
sleep 1

echo "=== Step 3/5: Start daphne (ASGI server for WebSockets) ==="
cd "$PROJECT_DIR"
nohup "$VENV_DIR/bin/daphne" -b 127.0.0.1 -p "$DAPHNE_PORT" -v 2 nebians.asgi:application \
    > "$DAPHNE_LOG" 2>&1 &
DAPHNE_PID=$!
disown $DAPHNE_PID 2>/dev/null || true
echo "daphne started (pid=$DAPHNE_PID, port=$DAPHNE_PORT) → $DAPHNE_LOG"
sleep 2
if ! kill -0 $DAPHNE_PID 2>/dev/null; then
    echo "ERROR: daphne failed to start. Last log lines:"
    tail -30 "$DAPHNE_LOG"
    exit 1
fi

echo "=== Step 4/5: Install + start cloudflared ==="
if ! command -v cloudflared >/dev/null 2>&1 && [ ! -x "$HOME/.local/bin/cloudflared" ]; then
    echo "Downloading cloudflared..."
    mkdir -p "$HOME/.local/bin"
    cd /tmp
    curl -sSL -o cloudflared "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64"
    chmod +x cloudflared
    mv cloudflared "$HOME/.local/bin/cloudflared"
fi
CF_BIN="$HOME/.local/bin/cloudflared"

# Pick the cloudflared command based on what's configured.
if [ -n "$NAMED_TUNNEL" ] && [ -f "$CLOUDFLARED_CONFIG" ]; then
    # Stable named tunnel
    nohup "$CF_BIN" --config "$CLOUDFLARED_CONFIG" tunnel run "$NAMED_TUNNEL" \
        > "$CLOUDFLARED_LOG" 2>&1 &
    CF_PID=$!
    disown $CF_PID 2>/dev/null || true
    echo "cloudflared (named tunnel=$NAMED_TUNNEL) started (pid=$CF_PID) → $CLOUDFLARED_LOG"
elif [ -f "$CLOUDFLARED_CONFIG" ]; then
    # Config exists but no specific tunnel requested — run default
    nohup "$CF_BIN" --config "$CLOUDFLARED_CONFIG" tunnel run \
        > "$CLOUDFLARED_LOG" 2>&1 &
    CF_PID=$!
    disown $CF_PID 2>/dev/null || true
    echo "cloudflared (config default) started (pid=$CF_PID) → $CLOUDFLARED_LOG"
else
    # No config — use a quick tunnel. URL is logged on first run and
    # auto-detected by web/views.py::_get_ws_public_url() at request time.
    nohup "$CF_BIN" tunnel --no-autoupdate --protocol http2 \
        --url "http://127.0.0.1:$DAPHNE_PORT" \
        > "$CLOUDFLARED_LOG" 2>&1 &
    CF_PID=$!
    disown $CF_PID 2>/dev/null || true
    echo "cloudflared (quick tunnel) started (pid=$CF_PID) → $CLOUDFLARED_LOG"
    echo ""
    echo "  The trycloudflare URL will appear in $CLOUDFLARED_LOG"
    echo "  in a few seconds. It will be auto-detected and served to"
    echo "  clients via window.WS_CONFIG.url."
    echo ""
    echo "  To use a STABLE URL instead, set up a named tunnel:"
    echo "    1. Move nebians.consica.com.np DNS to Cloudflare"
    echo "    2. cloudflared tunnel login"
    echo "    3. cloudflared tunnel create nebians-ws"
    echo "    4. Create ~/.cloudflared/config.yml (see script comments)"
    echo "    5. Re-run with: CLOUDFLARED_TUNNEL=nebians-ws bash setup_realtime.sh"
fi

echo "=== Step 5/5: Install @reboot crontab entries ==="
CRON_FILE="/tmp/nebians-realtime-cron"
cat > "$CRON_FILE" <<EOF
@reboot $VENV_DIR/bin/daphne -b 127.0.0.1 -p $DAPHNE_PORT -v 2 $PROJECT_DIR/nebians.asgi:application >> $DAPHNE_LOG 2>&1
EOF
# Add cloudflared @reboot entry matching the mode we just started
if [ -n "$NAMED_TUNNEL" ] && [ -f "$CLOUDFLARED_CONFIG" ]; then
    echo "@reboot /usr/bin/env PATH=$HOME/.local/bin:/usr/bin:/bin $CF_BIN --config $CLOUDFLARED_CONFIG tunnel run $NAMED_TUNNEL >> $CLOUDFLARED_LOG 2>&1" >> "$CRON_FILE"
else
    echo "@reboot /usr/bin/env PATH=$HOME/.local/bin:/usr/bin:/bin $CF_BIN tunnel --no-autoupdate --protocol http2 --url http://127.0.0.1:$DAPHNE_PORT >> $CLOUDFLARED_LOG 2>&1" >> "$CRON_FILE"
fi

# Append to existing crontab (preserving other entries)
( crontab -l 2>/dev/null | grep -v -F -f <(awk '/^@reboot.*(daphne|cloudflared)/ {print $0}' <(crontab -l 2>/dev/null)) ; cat "$CRON_FILE" ) | crontab -
echo "Crontab updated. View with: crontab -l"

echo ""
echo "=== Bootstrap complete ==="
echo "  daphne:    $(pgrep -f "daphne -b 127.0.0.1 -p $DAPHNE_PORT" | head -1)"
echo "  log:       $DAPHNE_LOG"
echo "  test:      curl -i http://127.0.0.1:$DAPHNE_PORT/  (HTTP 404 from daphne = WS endpoint is alive)"
