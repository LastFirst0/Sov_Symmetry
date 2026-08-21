#!/usr/bin/env bash
# ======================================================================
# SOVEREIGN ENGINE ONE-CLICK LAUNCH SCRIPT
# ======================================================================
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"
export PYTHONPATH="$SCRIPT_DIR:$PYTHONPATH"

echo "======================================================================"
echo "           SOVEREIGN ENGINE - BOOTSTRAP LAUNCHER                    "
echo "======================================================================"

# 1. Check for uv package manager
if ! command -v uv &> /dev/null; then
    echo "[!] 'uv' not found in PATH. Checking ~/.local/bin..."
    if [ -f "$HOME/.local/bin/uv" ]; then
        export PATH="$HOME/.local/bin:$PATH"
    else
        echo "[X] Error: 'uv' is required to run Sovereign Engine cleanly."
        echo "    Please install uv via: curl -LsSf https://astral.sh/uv/install.sh | sh"
        exit 1
    fi
fi

echo "[✓] Environment Ready: $(uv --version)"

# 2. Dispatch modes
if [ "$1" == "--test" ]; then
    echo "[*] Executing System Self-Check Diagnostics..."
    uv run python scripts/sovereign_workbench.py --test
    uv run python scripts/sovereign_ollama_server.py --test
    uv run python scripts/sovereign_mcp_server.py --test
    echo "======================================================================"
    echo "       ALL SOVEREIGN ENGINE DIAGNOSTICS PASSED PERFECTLY!            "
    echo "======================================================================"
elif [ "$1" == "--ollama" ]; then
    echo "[*] Starting Sovereign Ollama/OpenAI REST Server on http://0.0.0.0:11434..."
    exec uv run python scripts/sovereign_ollama_server.py "${@:2}"
elif [ "$1" == "--mcp" ]; then
    echo "[*] Starting Sovereign Model Context Protocol (MCP) Server over stdio..."
    exec uv run python scripts/sovereign_mcp_server.py "${@:2}"
elif [ "$1" == "--web" ]; then
    echo "[*] Starting Sovereign Web UI Dashboard on http://0.0.0.0:8080..."
    exec uv run python scripts/web_ui_server.py "${@:2}"
else
    echo "[*] Launching Sovereign Interactive Terminal Workbench..."
    exec uv run python scripts/sovereign_workbench.py "$@"
fi
