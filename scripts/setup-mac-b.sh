#!/bin/bash
# ============================================
# WorkBuddy Mac B 初始化脚本
# 用法：bash ~/.workbuddy/scripts/setup-mac-b.sh
# ============================================
set -e

REPO="git@github.com:lmj921/workbuddy-sync.git"
WB_DIR="$HOME/.workbuddy"

# ── 颜色 ──
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${GREEN}┌──────────────────────────────────────────────┐${NC}"
echo -e "${GREEN}│   WorkBuddy 双机同步 — Mac B 初始化           │${NC}"
echo -e "${GREEN}└──────────────────────────────────────────────┘${NC}"
echo ""

# ── 0. 备份数据库 ──
if [ -f "$WB_DIR/workbuddy.db" ]; then
    BACKUP="$HOME/Desktop/workbuddy.db.bak.$(date +%Y%m%d)"
    echo -e "${YELLOW}[0/3] 备份数据库 → ${BACKUP}${NC}"
    cp "$WB_DIR/workbuddy.db" "$BACKUP"
    echo -e "${GREEN}  ✓ 备份完成${NC}"
else
    echo -e "${YELLOW}[0/3] 未找到现有数据库，跳过备份${NC}"
fi
echo ""

# ── 1. 初始化 Git ──
echo -e "${YELLOW}[1/3] 初始化 Git 仓库...${NC}"
cd "$WB_DIR"
if [ -d .git ]; then
    echo -e "${YELLOW}  Git 仓库已存在，跳过 init${NC}"
else
    git init
fi

# 设置 remote（如果已存在则更新）
if git remote | grep -q origin; then
    git remote set-url origin "$REPO"
else
    git remote add origin "$REPO"
fi
git fetch origin
echo -e "${GREEN}  ✓ Git 就绪${NC}"
echo ""

# ── 2. 同步文件 ──
echo -e "${YELLOW}[2/3] 拉取远程文件...${NC}"
git checkout origin/master -- .gitignore .gitattributes
git reset --hard origin/master
git branch --set-upstream-to=origin/master master 2>/dev/null || true
echo -e "${GREEN}  ✓ 文件同步完成${NC}"
echo ""

# ── 3. 验证 ──
echo -e "${YELLOW}[3/3] 验证同步结果...${NC}"
SKILL_COUNT=$(ls -d "$WB_DIR/skills"/*/ 2>/dev/null | wc -l)
AUTO_COUNT=$(ls "$WB_DIR/automation-backups"/*.json 2>/dev/null | wc -l)
DB_EXISTS="❌"
[ -f "$WB_DIR/workbuddy.db" ] && DB_EXISTS="✅"

echo -e "  用户级 Skills:     ${GREEN}${SKILL_COUNT} 个${NC}"
echo -e "  Automation 备份:   ${GREEN}${AUTO_COUNT} 个${NC}"
echo -e "  数据库未丢失:      ${GREEN}${DB_EXISTS}${NC}"

echo ""
echo -e "${GREEN}┌──────────────────────────────────────────────┐${NC}"
echo -e "${GREEN}│  ✅ 初始化完成！重新打开 WorkBuddy 即可使用    │${NC}"
echo -e "${GREEN}└──────────────────────────────────────────────┘${NC}"
echo ""
echo -e "日常同步："
echo -e "  推送: ${YELLOW}bash ~/.workbuddy/scripts/wb-push.sh${NC}"
echo -e "  拉取: ${YELLOW}bash ~/.workbuddy/scripts/wb-pull.sh${NC}"
