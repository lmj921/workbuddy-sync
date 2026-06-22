---
name: wechat-game-chart-tracker
description: 微信小游戏榜单每日追踪系统。从应用宝(sj.qq.com)自动采集热门榜/畅销榜/新游榜数据，检测新进榜、出榜、排名变化和名称变更，通过企微私聊推送Markdown日报摘要，同时生成Excel存档。触发词：小游戏榜单、畅销榜、新游榜、微信小游戏排行、榜单追踪、游戏榜单日报。
description_zh: 微信小游戏榜单追踪
description_en: WeChat Mini Game Chart Tracker
disable: false
agent_created: true
---

# wechat-game-chart-tracker

## When to use
- 用户要求查看/追踪微信小游戏榜单数据
- 用户询问小游戏畅销榜、新游榜、热门榜排名
- 用户需要分析小游戏市场趋势、新进榜游戏、名称变更
- 每日自动化执行(automation-1779527692172, 11:00 CST)

## 项目路径
- 工作目录: `/Users/a1_builder/WorkBuddy/mini_game`
- Python venv: `/Users/a1_builder/.workbuddy/binaries/python/envs/default/bin/python3`
- 主脚本: `scripts/main.py`
- 数据库: `data/db/charts.db`
- Excel存档: `data/excel/chart_YYYY-MM-DD.xlsx`

## 数据源
- 应用宝微信小游戏: `https://sj.qq.com/wechat-game`
  - 热门榜: `/wechat-game/popular-game-rank`
  - 畅销榜: `/wechat-game/best-sell-game-rank`
  - 新游榜: `/wechat-game/new-game-rank`
- 每个榜单静态HTML首屏20条，无限滚动加载更多（当前仅抓取首屏）
- 页面CSS类名为模块化命名，解析需用 `[class*='xxx']` 选择器匹配
- 关键类名: `GameCard_name`(游戏名), `TagList_tagName`(分类标签), `rankNumber`(排名), `GameIcon_icon`(图标)

## Steps

### 1. 运行完整流程（采集→分析→推送→存档）
```bash
cd /Users/a1_builder/WorkBuddy/mini_game && /Users/a1_builder/.workbuddy/binaries/python/envs/default/bin/python3 scripts/main.py
```

### 2. 仅采集数据（不推送）
```bash
cd /Users/a1_builder/WorkBuddy/mini_game && /Users/a1_builder/.workbuddy/binaries/python/envs/default/bin/python3 scripts/main.py --skip-push
```

### 3. 指定日期运行
```bash
cd /Users/a1_builder/WorkBuddy/mini_game && /Users/a1_builder/.workbuddy/binaries/python/envs/default/bin/python3 scripts/main.py --date 2026-05-20 --skip-push
```

### 4. 手动推送测试
```python
import sys; sys.path.insert(0, 'scripts')
from push_wechat import push_markdown
push_markdown("🎮 测试消息")
```

### 5. 查看某日数据
```python
import sys; sys.path.insert(0, 'scripts')
from db import get_chart_data, init_db
init_db()
data = get_chart_data('2026-05-23', 'bestselling')  # popular/bestselling/newgame
for r in data[:5]: print(f"#{r['rank']} {r['game_name']}")
```

## 架构说明
```
scripts/
├── main.py          # 主入口，串联全流程
├── fetch_charts.py  # 数据采集（应用宝静态HTML抓取）
├── db.py            # SQLite数据库管理
├── analyze.py       # 分析引擎（新进榜/出榜/排名变化/名称变更/品类分布）
├── push_wechat.py   # 企微Webhook推送（chatid: jokerlu）
└── excel_export.py  # Excel存档（含样式和条件高亮）
```

## 企微推送配置
- Webhook Key: `78fa51e9-438c-484f-a823-1769ee9b4cbc`
- ChatID: `jokerlu`（私聊模式）
- 消息格式: Markdown，限制4096字节（超长自动分段）

## Pitfalls
- **CSS类名变化**: 应用宝前端可能更新CSS类名hash，导致解析失败。如果采集到0条数据，用浏览器F12检查新的类名模式
- **请求频率**: 三个榜单请求间隔1秒，避免被封IP
- **首日无对比**: 系统首日运行时，所有游戏都标记为"新进榜"，第二天开始才有对比数据
- **无限滚动数据**: 当前仅抓取静态HTML首屏20条，更多数据需模拟滚动或找到动态API
- **企微消息长度**: Markdown消息超4096字节会自动分段推送，但分段间有2秒延迟避免频率限制
- **AppId提取**: 使用正则 `wx[a-f0-9]{16}` 从href中提取

## Verification
1. 运行 `main.py --skip-push` 确认输出60条数据(3榜×20条)
2. 检查 `data/db/charts.db` 中有数据
3. 检查 `data/excel/chart_YYYY-MM-DD.xlsx` 已生成
4. 企微收到Markdown格式的榜单日报消息

## 扩展方向
- [ ] 找到应用宝动态加载API，获取Top 50-100完整榜单
- [ ] 接入DataEye ADX API获取更全面的榜单数据
- [ ] 添加游戏详情页信息（开发商、评分等）
- [ ] 品类趋势周报/月报
- [ ] 新游上线追踪（首次出现在新游榜的游戏）
