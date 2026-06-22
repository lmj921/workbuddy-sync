## 产品概述

对 2026 年 4 月 19 日英超第 33 轮 **曼城（主场）vs 阿森纳** 进行 v5 规范下的完整赛前分析，并在 **¥50 单场预算** 下给出 **A 方案（少而精，1-2 注核心 + 可选博冷/角球）** 投注建议。产出一份独立的赛前分析 Markdown 文件。

## 核心功能

1. **数据实拉**：用 `scripts/odds_api.py` + Web 搜索交叉验证，拉取 1X2 / 亚盘 / O/U 2.5 / O/U 3.5 / BTTS / 角球 O/U 的 Bet365 实时赔率（禁止脑补）。
2. **赛前伤停核实**：赛前 2 小时内通过 Web 搜索（Sports Mole / Football Faithful / 官方推特）核实曼城与阿森纳双方首发与伤停，重点关注 Haaland / De Bruyne / Rodri / Gvardiol / Saka / Ødegaard / Saliba / Gabriel / Rice / Gyökeres / Eze 的状态。转会信息强制交叉验证（Eze / Gyökeres 已在阿森纳、Isak 已在利物浦）。
3. **纯模型预测**：调用 `python3 scripts/predict_single.py --model-dir models/E0 --home "Man City" --away "Arsenal" --xgb --bankroll 50 --json`（必须加 `--xgb` 激活 73 因子 + 全部赔率参数）。
4. **纯脑算分析**：按 v5 权重体系（xG 28% / 主客场 25% / 近期战绩 18% / H2H 10% / 均值回归 12% / 心理 4%）评估五大维度，每个因子标注方向与幅度（单市场修正≤±15%）。
5. **融合方案**：模型 60% + 脑算 40%，输出最终投注表（核心/价值/博冷/角球分层，总仓位 ≤ ¥50 且单方向 ≤60%），保留纯模型 EV>+10% 的注单≥50% 仓位，O2.5 vs O2.75 赔率差利用。
6. **六项补充分析**：xG 深度对比、命中矩阵、注单一致性检查、临场调整清单、同类比赛对标（参考 chelsea-vs-mancity-20260412、arsenal-vs-bournemouth-20260411）、经验教训逐条核对。
7. **角球专项**（v5 必选）：曼城+阿森纳均为边路强队（Doku / Saka / Martinelli），冠军争夺收官战紧迫度高 → 系统性 +1.5 角球修正；若控球 <40% 则反向 -2~3 修正。
8. **纯模型假设结算**：对比纯模型 vs 融合方案预期 ROI，给出增减值分析。
9. **风控提示**：针对双强对攻 + 冠军争夺场景触发 v5 规则（拒绝小球、Isotonic Draw -30%、XGB Draw>+50% 过滤为幻觉、深度负 EV<-30% 标"🚨庄家抽水重灾区"）。
10. **最终交付**：对话中给出 ¥50 投注方案摘要表 + 文件路径；调用 `open_result_view` 展示完整 Markdown。

## 交付物

- 单一 Markdown 文件：`analyses/mancity-vs-arsenal-20260419.md`（严格遵循 `config/analysis-template.md` 11 大模块）

## 实施方式

### 1. 数据采集（只读）

- **赔率实拉**：`python3 scripts/odds_api.py --league epl --search "Man City" --json`，拉 h2h / totals / spreads / btts / corners；若 API 返回不全，Web 搜索 Bet365 / Marathonbet / sgodds 补齐。所有 EV 计算的赔率必须注明数据源与抓取时间。
- **伤停核实**：Web 搜索 Sports Mole、Football Faithful、官方推特最新推文（赛前 2 小时内）。
- **历史数据**：已有 `data/E0.csv` + `models/E0/` 可直接使用，无需跑 `refresh_data.py`。

### 2. 纯模型预测

- 命令：`python3 scripts/predict_single.py --model-dir models/E0 --home "Man City" --away "Arsenal" --xgb --home-odds X --draw-odds X --away-odds X --over-odds X --under-odds X --btts-yes-odds X --btts-no-odds X --ah-line X --ah-home-odds X --ah-away-odds X --bankroll 50 --json`
- 强制加 `--xgb`（否则只跑泊松+Isotonic MVP 子集）
- Sanity check：`ah_home_cover + ah_away_cover ≈ 1.0`（handicap_prob BUG 已修）
- 校准偏移：`calibration_shift["draw"]["shift"] > 0.20` 时 draw 市场仓位 ×0.7
- 过滤：XGB Draw EV > +50% 视为幻觉直接忽略

### 3. 纯脑算（v5 权重体系）

- 单市场修正幅度 ≤ ±15%（山东vs海港教训）
- 伤停双向评估（不能只看单方）
- 禁止线性外推（"N场未胜"不能直接推本场）
- 历史主场统治力需阵容折扣（缺 2+ 核心→主场加权从 +3% 降至 +1%）

### 4. 融合与注单构建

- 默认 60/40；核心球员突发伤停或战意明确分化 → 50/50
- **单方向总仓位 ≤60%**（禁止 ALL-IN）
- **保留纯模型高 EV**：纯模型 EV>+10% 的注单融合方案必须保留≥50% 仓位
- **O2.5 vs O2.75**：融合 O2.5 概率>60% 且 O2.75 赔率>1.75 时优先 O2.75
- **双强对攻禁小球**：确认双 4-3-3 对攻 → 拒绝一切 U2.5 / U3.0
- **总投注 = ¥50**；A 方案：1-2 注核心 ¥30-40 + 可选 ¥10-20 博冷/角球
- **深度负 EV 标红**：EV<-30% 标"🚨庄家抽水重灾区"
- **比分矩阵 Top3 必含**：若有正 EV 须纳入

### 5. 角球专项（v5 必选）

- 曼城（Doku/Savinho）+ 阿森纳（Saka/Martinelli）双边路强队 + 冠军争夺 → +1.5 修正
- 例外：控球 <40% → -2~3 修正
- 填角球专项分析表（近5场均值 + 对抗度 + 冠军修正 → 本场预期 → 盘口 EV）

### 6. 目录结构

```
football-betting/
├── analyses/
│   └── mancity-vs-arsenal-20260419.md    # [NEW] 赛前分析产出，11大模块完整结构
├── config/
│   └── analysis-template.md              # [REF] 参照模板
├── scripts/
│   ├── predict_single.py                 # [USE] 纯模型预测（加 --xgb）
│   └── odds_api.py                       # [USE] 赔率实拉
└── .workbuddy/memory/
    ├── MEMORY.md                         # [REF] 经验教训 & 系统性问题
    └── 2026-04-19.md                     # [APPEND] 今日简短备忘
```

## 关键约束

- 一场一文件，禁止合并
- 赔率禁止脑补，所有 EV 依赖的赔率必须标注来源与时间
- 不做复盘（赛后才做）、不修改代码、不做其他场次

## Agent Extensions

### Skill

- **football-betting-analyst**
- 用途：主导本场赛前分析，按 v5 三段式规范 + 11 大模块输出到 `analyses/mancity-vs-arsenal-20260419.md`
- 预期产出：完整 Markdown 文件（纯模型 + 纯脑算 + 融合方案 + 六项补充分析 + 角球专项 + 纯模型假设结算）+ 对话摘要投注表