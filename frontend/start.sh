#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

# ── 檢查 node ──
if ! command -v node &>/dev/null; then
  echo "❌ 找不到 Node.js，請先安裝"
  echo "   macOS: brew install node"
  echo "   或到 https://nodejs.org 下載安裝"
  exit 1
fi

echo "✅ Node.js: $(node --version)"

# ── 檢查 npm ──
if ! command -v npm &>/dev/null; then
  echo "❌ 找不到 npm"
  exit 1
fi

echo "✅ npm: $(npm --version)"

# ── 安裝依賴 ──
echo "📦 安裝前端依賴 ..."
npm install

# ── 啟動 dev server ──
echo ""
echo "🚀 啟動 NovelForge Frontend ..."
npm run dev -- --host 0.0.0.0
