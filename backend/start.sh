#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

# ── 載入 .env（本機開發用；Docker 內無此檔，變數由 compose 提供）──
if [ -f .env ]; then
  set -a; source .env; set +a
fi

# ── 找出 python3.12（可執行檔名可能是 python3.12 或 python3）──
PYTHON=""
for candidate in python3.12 python3; do
  if command -v "$candidate" &>/dev/null; then
    ver=$("$candidate" --version 2>&1)
    if echo "$ver" | grep -qE 'Python 3\.12\.'; then
      PYTHON="$candidate"
      break
    fi
  fi
done

if [ -z "$PYTHON" ]; then
  echo "❌ 找不到 Python 3.12（已嘗試 python3.12 / python3）"
  echo "   macOS: brew install python@3.12"
  echo "   Ubuntu: sudo apt install python3.12 python3.12-venv"
  exit 1
fi

echo "✅ Python: $($PYTHON --version)"

# ── 建立 / 啟動 venv ──
VENV_DIR="$SCRIPT_DIR/.venv"
if [ ! -f "$VENV_DIR/bin/activate" ]; then
  echo "📦 建立虛擬環境 ..."
  $PYTHON -m venv "$VENV_DIR"
fi
source "$VENV_DIR/bin/activate"
echo "✅ venv 已啟動"

# ── 安裝依賴 ──
if [ -f requirements.txt ]; then
  echo "📦 安裝 Python 依賴 ..."
  pip install -q -r requirements.txt
fi

# ── 啟動 API ──
BACKEND_PORT="${PORT:-8001}"
echo ""
echo "🚀 啟動 NovelForge API (http://0.0.0.0:$BACKEND_PORT) ..."
exec uvicorn main:app --host 0.0.0.0 --port "$BACKEND_PORT" --reload
