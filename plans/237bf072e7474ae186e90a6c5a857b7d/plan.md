## 用户需求

分析 2026-04-19 英超默西塞德德比 **埃弗顿（主） vs 利物浦（客）**，给出 **¥50** 预算下的赛前投注方案。

## 核心交付

- **赛前分析文件**：`analyses/everton-vs-liverpool-20260419.md`（遵循 v5/v5.2/v5.3 规范，三段式 + 11 大模块）
- **投注方案**：2–3 注分散，总仓位 ¥50，必须包含角球/BTTS 等多市场评估
- **实时数据验证**：赔率实拉（Bet365/sgodds/Marathonbet），伤停核实（Sports Mole/官方），重点确认 Salah / Isak / Van Dijk / Virgil 等利物浦核心，以及埃弗顿主力后卫/中场状态

## 关键功能点

- 纯模型输出（`predict_single.py --xgb`）：1X2/亚盘/大小球/BTTS/比分矩阵/Elo/λ/EV/Kelly
- 纯脑算：阵容、战意（埃弗顿保级压力 vs 利物浦争冠/欧冠席位）、默西塞德德比氛围、主客场、盘口变化
- 融合方案（60/40）：含角球专项（德比+1.5 修正）、纯模型高 EV(>+10%) 注单≥50% 仓位保留
- 风控：XGB Draw EV>+50% 忽略、深度负 EV(<-30%) 提示、Isotonic Draw shift 校正、handicap_prob 修复后 AH sanity check
- 输出：完整 MD 文件 + 注单一致性检查 + 纯模型假设结算对比

## 技术栈

- **Python 3** + 项目现有模型体系：`models/E0/`（Poisson + Isotonic Calibrator + Elo + Meta + XGB）
- **预测脚本**：`scripts/predict_single.py --model-dir models/E0 --home Everton --away Liverpool --xgb --bankroll 50 --json`（`--xgb` 为 MEMORY 强制）
- **赔率抓取**：`scripts/odds_api.py`（Bet365/Marathonbet/Sbobet/sgodds）
- **数据源**：`data/E0.csv`（英超 25/26 赛季），必要时 `scripts/refresh_data.py --league E0`
- **外部信息**：Sports Mole / Football Faithful / 官方俱乐部 X 账号（伤停）、sgodds.com（实时盘口变化）

## 实施策略

1. **数据预检** → 2. **纯模型跑数** → 3. **伤停+战意核实** → 4. **脑算修正** → 5. **融合+角球专项** → 6. **一致性检查** → 7. **落盘 MD**

- 严格按 `config/analysis-template.md` 三段式 + 11 模块
- 角球模块：近 5 场均值 + 对抗度 + 德比+1.5 修正 → 本场预期 → 盘口 EV 判断
- 资金分配：Kelly × 0.25 分数凯利，总仓位 ¥50，单注上限 ¥25，避免 all-in
- 赔率差利用：若融合 O2.5 概率>60% 且 O2.75@>1.75，优先 O2.75（v5.3 规则）

## 执行要点（防回归）

- **赔率铁律**：所有 EV 用的赔率必须实拉，禁止脑补（v5 教训，BTTS 曾脑补 1.55 实际 1.34 导致方向反）
- **handicap_prob 修复后**：AH sanity check 确认 sum(P_home_cover + P_push + P_away_cover) ≈ 1.0
- **XGB Draw 幻觉过滤**：若 XGB Draw EV > +50% 直接忽略
- **Isotonic Draw shift**：若 calibration_shift["draw"]>0.20，draw 市场仓位额外 −30%
- **纯模型高 EV 保留**：纯模型 EV>+10% 注单，融合方案保留≥50% 仓位（v5.3 切vs曼联反差教训）
- **德比角球修正**：默认 +1.5；若一方控球<35% 极端回缩则反向 −3~4（例外）
- **进球荒/崩盘叙事反转**：检查双方近 N 场进球趋势，必要时反转 U2.5→O2.5（v5.3 狼队 vs 利兹教训）
- **转会验证**：Isak 已在利物浦；名单必须交叉验证

## 目录影响

```
football-betting/
├── analyses/
│   └── everton-vs-liverpool-20260419.md   # [NEW] 赛前分析主文件（三段式+11模块+投注方案）
├── data/E0.csv                              # [READ] 英超数据（必要时 refresh_data.py 刷新）
└── .workbuddy/memory/2026-04-19.md          # [NEW/APPEND] 当日关键决策与教训记录
```

## 分析文件结构（MD 骨架）

1. 基础信息（比赛/时间/场地/赔率快照）
2. Part1 纯模型（概率/λ/EV/Kelly/比分矩阵/AH/OU/BTTS/Elo）
3. Part2 纯脑算（阵容/伤停/战意/战术/主客场/盘口变化）
4. Part3 融合方案（60/40，含角球专项）
5. xG 深度分析
6. 命中矩阵
7. 注单一致性检查
8. 临场调整清单
9. 同类比赛对比（近 3 次默西塞德德比）
10. 经验教训检查（v5/v5.2/v5.3 规则逐条核对）
11. 角球专项分析表
12. 纯模型假设结算 vs 融合方案对比
13. 最终投注方案（2–3 注，总 ¥50）

## Agent Extensions

### Skill

- **football-betting-analyst**
- Purpose: 驱动完整的足球博彩分析流程，覆盖 xG/盘口价值/凯利分配/分层投注/角球专项
- Expected outcome: 产出符合 v5 规范的三段式结构化分析与注单

### Skill

- **neodata-financial-search**（备用）
- Purpose: 如需即时查询英超最新联赛积分榜、球队数据等通用信息时作为补充
- Expected outcome: 补齐战意/排名维度所需的实时信息

### SubAgent

- **code-explorer**
- Purpose: 快速定位 `scripts/predict_single.py`、`odds_api.py`、`config/analysis-template.md` 的最新参数与模板结构
- Expected outcome: 确保脚本调用参数正确、模板字段与 v5 规范一致