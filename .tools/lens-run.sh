#!/usr/bin/env bash
# lens-run.sh — tmux launcher for agentlens wait
#
# Usage:
#   ./out/lens-run.sh [OPTIONS] -- COMMAND [ARGS...]
#
# Options:
#   -o DIR    Output directory for exported files (default: results)
#   -s NAME   Override auto-generated session name
#
# Examples:
#   ./out/lens-run.sh -- claude -p "refactor auth"
#   ./out/lens-run.sh -o results/my-test -s my-test -- python my_agent.py

set -euo pipefail

# ---------------------------------------------------------------------------
# Parse arguments
# ---------------------------------------------------------------------------

OUTPUT="results"
SESSION_NAME=""
TMUX_SESSION="agentlens"

while [[ $# -gt 0 ]]; do
    case "$1" in
        -o)
            OUTPUT="$2"
            shift 2
            ;;
        -s)
            SESSION_NAME="$2"
            shift 2
            ;;
        --)
            shift
            break
            ;;
        *)
            echo "Unknown option: $1" >&2
            echo "Usage: $0 [-o DIR] [-s NAME] -- COMMAND [ARGS...]" >&2
            exit 1
            ;;
    esac
done

if [[ $# -eq 0 ]]; then
    echo "Error: no command specified after --" >&2
    echo "Usage: $0 [-o DIR] [-s NAME] -- COMMAND [ARGS...]" >&2
    exit 1
fi

# ---------------------------------------------------------------------------
# Shell-quote helper (for embedding values in tmux command strings)
# ---------------------------------------------------------------------------

quote() { printf '%s' "'${1//\'/\'\\\'\'}'"; }

# ---------------------------------------------------------------------------
# Build agentlens wait command
# ---------------------------------------------------------------------------

WAIT_CMD="uv run agentlens wait --output $(quote "$OUTPUT") --no-open"
if [[ -n "$SESSION_NAME" ]]; then
    WAIT_CMD="${WAIT_CMD} --session-name $(quote "$SESSION_NAME")"
fi

# ---------------------------------------------------------------------------
# Build user command (preserve quoting for args with spaces)
# ---------------------------------------------------------------------------

USER_CMD=""
for arg in "$@"; do
    USER_CMD="${USER_CMD:+$USER_CMD }$(quote "$arg")"
done

# ---------------------------------------------------------------------------
# Proxy env vars
# ---------------------------------------------------------------------------

PROXY="http://127.0.0.1:8080"
CA="${HOME}/.mitmproxy/mitmproxy-ca-cert.pem"

# ---------------------------------------------------------------------------
# Launch tmux
# ---------------------------------------------------------------------------

tmux kill-session -t "$TMUX_SESSION" 2>/dev/null || true
tmux new-session -d -s "$TMUX_SESSION" "$WAIT_CMD; exec ${SHELL:-bash}"
tmux split-window -h -t "$TMUX_SESSION" \
    "sleep 2 && \
     HTTP_PROXY=${PROXY} HTTPS_PROXY=${PROXY} \
     NODE_EXTRA_CA_CERTS=${CA} SSL_CERT_FILE=${CA} \
     REQUESTS_CA_BUNDLE=${CA} CURL_CA_BUNDLE=${CA} \
     ${USER_CMD}"
tmux select-pane -t "$TMUX_SESSION:0.1"
exec tmux attach -t "$TMUX_SESSION"
