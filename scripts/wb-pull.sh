#!/bin/bash
# ============================================
# WorkBuddy 拉取脚本 — 开机后/切电脑后执行
# 用法：bash ~/.workbuddy/scripts/wb-pull.sh
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
    echo -e "${RED}⚠️  WorkBuddy 还在运行！请先彻底退出后再拉取。${NC}"
    exit 1
fi

echo -e "${YELLOW}⬇️  拉取远程更新...${NC}"
git fetch origin

LOCAL=$(git rev-parse master 2>/dev/null)
REMOTE=$(git rev-parse origin/master 2>/dev/null)

if [ "$LOCAL" = "$REMOTE" ]; then
    echo -e "${GREEN}  已是最新，无需同步${NC}"
    echo -e "${GREEN}✅ 可以打开 WorkBuddy 了${NC}"
    exit 0
fi

echo -e "${YELLOW}  发现新变更，正在合并...${NC}"
if git merge origin/master --no-edit; then
    echo ""
    echo -e "${GREEN}✅ 同步完成！${NC}"
    echo ""
    # 显示变更摘要
    echo -e "${YELLOW}── 变更文件 ──${NC}"
    git --no-pager diff --stat "$LOCAL..$REMOTE" 2>/dev/null || true
else
    echo -e "${RED}❌ 合并冲突！请手动处理:${NC}"
    echo -e "${RED}   cd ~/.workbuddy && git status${NC}"
    exit 1
fi
