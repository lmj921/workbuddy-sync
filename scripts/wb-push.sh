#!/bin/bash
# ============================================
# WorkBuddy 推送脚本 — 关机前/切电脑前执行
# 用法：bash ~/.workbuddy/scripts/wb-push.sh
# ============================================
set -e

WB_DIR="$HOME/.workbuddy"
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

cd "$WB_DIR"

# ── 确保 WorkBuddy 已退出 ──
if pgrep -x "WorkBuddy" > /dev/null; then
    echo -e "${RED}⚠️  WorkBuddy 还在运行！请先彻底退出后再推送。${NC}"
    exit 1
fi

echo -e "${YELLOW}📦 暂存变更...${NC}"
git add -A

if git diff --cached --quiet; then
    echo -e "${GREEN}  没有新变更，跳过 commit${NC}"
else
    TIMESTAMP=$(date "+%Y-%m-%d %H:%M")
    HOSTNAME_SHORT=$(hostname -s)
    git commit -m "sync: ${TIMESTAMP} @ ${HOSTNAME_SHORT}"
    echo -e "${GREEN}  ✓ 已提交${NC}"
fi

echo -e "${YELLOW}🚀 推送到 GitHub...${NC}"
git push
echo -e "${GREEN}✅ 推送完成，可以安全关机/切电脑了${NC}"
