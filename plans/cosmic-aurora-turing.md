# 微信小游戏榜单每日追踪系统

## 需求概述
每天自动获取微信小游戏三大核心榜单（畅销榜/畅玩榜/人气榜），整理数据并分析新进榜和名称变化，通过企微推送摘要 + 本地Excel存档。

## 数据源现状
- **DataEye ADX API**：最完整方案，¥12,000/年起，有REST API + Bearer Token鉴权
- **微信CPS API**：免费但需CPS服务商企业资质
- **没有免费公开API**

> **前置确认**：需要确认Joker是否已有DataEye账号/是否有公司预算订阅

## 方案设计

### 架构总览

```
[数据采集层] → [数据存储层] → [分析引擎] → [输出层]
     ↓              ↓              ↓            ↓
  DataEye API    SQLite/CSV     变化检测      企微Markdown
  (或手动输入)    历史数据       趋势分析      Excel文件
```

### Step 1: 项目初始化 & 数据存储

创建项目结构：
```
/Users/a1_builder/WorkBuddy/mini_game/
├── .workbuddy/
│   ├── memory/
│   ├── skills/
│   └── automations/
├── data/
│   ├── db/              # SQLite数据库（历史数据）
│   ├── excel/           # 每日Excel存档
│   └── logs/            # 运行日志
├── scripts/
│   ├── fetch_charts.py  # 数据采集脚本
│   ├── analyze.py       # 分析引擎
│   ├── push_wechat.py   # 企微推送
│   └── main.py          # 主入口
└── config/
    └── config.yaml      # 配置文件（API Key、Webhook等）
```

SQLite表设计：
- `chart_records`: 每日榜单快照（日期、榜单类型、排名、游戏名、appid、分数等）
- `game_profiles`: 游戏信息表（appid、名称、开发商、品类、首次入榜日期等）
- `name_changes`: 名称变更记录（游戏appid、旧名、新名、变更日期）
- `daily_summary`: 每日摘要（新进榜数量、出榜数量、名称变化等）

### Step 2: 数据采集脚本 (`fetch_charts.py`)

**方案A - DataEye API（优先）**：
- 调用 DataEye ADX 榜单接口获取三大榜单 Top 100
- 鉴权：Bearer Token（存于config.yaml）
- 每日 ~10:30 执行（DataEye T+1更新约10:00）

**方案B - 手动输入（兜底）**：
- 提供一个简单的输入接口（命令行/文件模板）
- 用户从微信客户端或DataEye网页复制粘贴数据
- 解析并入库

**方案C - 浏览器自动化（实验性）**：
- 使用 playwright/agent-browser 自动登录 DataEye 网页版抓取
- 依赖已有账号，无需额外API费用

> 初始版本先实现方案B（手动输入），确保流程跑通，再接入API

### Step 3: 分析引擎 (`analyze.py`)

核心分析逻辑：

1. **新进榜检测**：对比前一天榜单，识别新出现的游戏 → 记录入榜日期
2. **出榜检测**：识别跌出榜单的游戏 → 记录出榜日期
3. **排名变化**：计算每款游戏的排名升降 → 标注大幅升降（±10名以上）
4. **名称变更检测**：通过appid匹配，检测同一游戏名称变化 → 记录名称变更历史
5. **持续在榜统计**：计算每款游戏的连续在榜天数
6. **品类分布分析**：统计各品类在榜数量变化

### Step 4: 企微推送 (`push_wechat.py`)

复用已有企微Webhook体系（`chatid: jokerlu`）：

推送格式（Markdown）：
```
🎮 微信小游戏榜单日报 | 2026-05-21

📊 三榜概览
| 榜单 | 新进 | 出榜 | 平均变动 |
|------|------|------|---------|
| 畅销榜 | 3 | 2 | ↑2.1 |
| 畅玩榜 | 5 | 4 | ↓1.3 |
| 人气榜 | 4 | 3 | ↑0.8 |

🆕 新进榜游戏
| 游戏 | 榜单 | 首次排名 |
|------|------|---------|
| XX游戏 | 畅销榜 | #15 |
| YY游戏 | 畅玩榜 | #8 |

🔄 名称变更
| 旧名 | 新名 | 榜单 |
|------|------|------|
| XX改名前 | XX改名后 | 畅销榜 |

📈 大幅上升（↑10+）
| 游戏 | 榜单 | 昨日→今日 |
|------|------|----------|
| ZZ游戏 | 畅销榜 | #35→#12 |

📉 大幅下降（↓10+）
...
```

### Step 5: Excel存档

每日生成Excel文件 `data/excel/chart_YYYY-MM-DD.xlsx`，包含：
- Sheet1: 畅销榜快照
- Sheet2: 畅玩榜快照
- Sheet3: 人气榜快照
- Sheet4: 变化分析汇总
- Sheet5: 名称变更记录

### Step 6: 自动化调度

创建 automation，每日 11:00 执行（DataEye T+1约10:00更新）：
- 调用 `main.py` 完成采集→分析→推送→存档全流程
- 失败时推送告警消息

## 实施优先级

| 优先级 | 任务 | 预计工作量 |
|--------|------|-----------|
| P0 | 项目初始化 + SQLite建表 | 小 |
| P0 | 手动输入数据流程（方案B） | 中 |
| P0 | 分析引擎（新进榜/名称变更/排名变化） | 中 |
| P0 | 企微推送 | 小（复用已有体系） |
| P0 | Excel存档 | 中 |
| P0 | 每日自动化 | 小 |
| P1 | DataEye API接入（方案A） | 中（需API Key） |
| P2 | 浏览器自动化采集（方案C） | 大 |

## 关键文件清单

需要创建的文件：
- `/Users/a1_builder/WorkBuddy/mini_game/scripts/fetch_charts.py`
- `/Users/a1_builder/WorkBuddy/mini_game/scripts/analyze.py`
- `/Users/a1_builder/WorkBuddy/mini_game/scripts/push_wechat.py`
- `/Users/a1_builder/WorkBuddy/mini_game/scripts/main.py`
- `/Users/a1_builder/WorkBuddy/mini_game/config/config.yaml`
- `/Users/a1_builder/WorkBuddy/mini_game/.workbuddy/memory/MEMORY.md`

## 待确认

1. **DataEye账号**：是否已有DataEye ADX订阅？如没有，是否可以申请公司预算？
2. **初始先用方案B（手动输入）是否OK？** 后续再接入API
3. **榜单深度**：默认抓取Top 100，是否需要更多？
4. **推送时间**：11:00合适吗？
