## 用户需求

分析 2026-04-19 英超 **阿斯顿维拉 vs 桑德兰** 一场比赛，给出**¥50 预算**下的**保守稳健型**投注方案（2-3 注、聚焦核心正 EV 市场）。

## 核心产出

- **赛前分析文件**: `analyses/aston-villa-vs-sunderland-20260419.md`（一场一文件，禁止合并）
- **方案风格**: 保守稳健，单注 ≤ ¥20，总仓位 ≤ ¥50；禁止博冷；聚焦 EV ≥ 5% 的核心市场
- **赔率来源**: 必须通过 `scripts/odds_api.py` 实拉（禁止脑补），不足处用 Web Search 交叉验证
- **模型**: `python3 scripts/predict_single.py --model-dir models/E0 --xgb --bankroll 50 --json`，XGB 必开

## 11 大必选模块（对齐 v5.3 规范）

1. 纯模型（概率/λ/EV/Kelly/比分矩阵/亚盘/Elo）
2. 纯脑算（阵容/战意/战术/主客场/盘口）
3. 融合方案（60/40，含角球）
4. xG 深度
5. 命中矩阵
6. 注单一致性检查
7. 临场调整
8. 同类比赛对比（复用场次 #3、#17 桑德兰经验）
9. 经验教训检查（v5/v5.2/v5.3 规则逐条核验）
10. 角球专项分析（近 5 场均值 + 对抗度 + 德比修正 → 本场预期 → EV）
11. 纯模型方案假设结算

## 关键约束（MEMORY 硬规则）

- 单方向仓位 ≤ 60%，保留 ≥ 30% 反向对冲空间
- 融合方案必须保留纯模型 EV ≥ 15% 注单至少 50% 仓位
- 脑算对单一市场修正 ≤ ±15%
- 投注方案必须至少含 Top3 比分矩阵中一注
- 角球有正 EV 则必须纳入
- Isotonic Draw shift > 0.20 时 draw 市场额外 -30% 仓位
- XGB Draw EV > +50% 视为幻觉过滤
- 赛前伤停 2 小时内核实（Sports Mole / Football Faithful / 官方）

## 特殊性

- 桑德兰非鱼腩：场次 #3（纽卡 1-2 桑）+ 场次 #17（桑 1-0 热刺）两次验证客场/主场都能打硬仗，对阵维拉需重估胜负概率
- ¥50 小本金：Kelly 仓位按 50 bankroll 重算，2-3 注聚焦，禁止广撒网

## 工作方式

非代码任务：基于现有分析流水线产出一份完整的**赛前分析 markdown 文件** + 终端展示的**核心投注方案**。

## 数据与工具链（全部复用项目已有能力）

| 能力 | 工具/路径 | 用法 |
| --- | --- | --- |
| 实时赔率 | `scripts/odds_api.py` | `--league epl --search "Aston Villa" --json` |
| 模型预测 | `scripts/predict_single.py` | `--model-dir models/E0 --home "Aston Villa" --away "Sunderland" --xgb --bankroll 50 --json` |
| 英超历史 | `data/E0.csv` | 近 H2H / 主客场分路 |
| xG 高级数据 | `data/understat/EPL_2025.json` | xG / npxG / ppda / xpts |
| 桑德兰最近战绩 | `analyses/newcastle-vs-sunderland-*.md` + `analyses/sunderland-vs-tottenham-*.md` | 同对手同侧经验 |
| 伤停 | Web Search（Sports Mole / Football Faithful / 官方推特） | 赛前 2 小时核实 |
| 规范模板 | `config/analysis-template.md` | 11 模块完整骨架 |
| 记忆硬规则 | `.workbuddy/memory/MEMORY.md` | v5/v5.2/v5.3 逐条核验 |


## 执行流程（严格按序）

1. **数据采集层**

- 调用 odds_api 拉 1X2 + AH + O/U + BTTS + 角球 O/U + 比分；多家博彩交叉验证（至少 Pinnacle + Bet365）
- 跑 `predict_single.py --xgb` 得到 λ_home / λ_away / 1X2 概率 / AH cover / O/U / BTTS / Top5 比分 / Kelly 建议（bankroll=50）
- Web Search 获取双方最新伤停、近 5 场战绩、维拉主场分路、桑德兰客场分路

2. **三段式分析层**

- Part 1 纯模型：直接采用 predict_single 输出，列 1X2/AH/O/U/BTTS/Top5 比分/λ/EV/Kelly 表
- Part 2 纯脑算：阵容（伤停双向评估）/ 战意（保级/欧战位）/ 战术（阵型对攻度）/ 主客场（维拉主场分路）/ 盘口（初盘→实时变化）
- Part 3 融合：60/40 权重，每市场单独融合，每项修正 ≤ ±15%；纯模型 EV ≥ 15% 强制保留 ≥ 50% 仓位

3. **角球专项**（独立模块）

- 近 5 场角球均值（维拉主场 + 桑德兰客场）→ 对抗度修正 → 本场预期 → 对比盘口算 EV → 决定是否下注

4. **v5.3 规则自检清单**（逐条对照）

- 进球荒持续性？崩盘叙事？年轻中卫摆铁桶？O2.5 vs O2.75 赔率差？XGB Draw 幻觉？Draw shift > 0.20？

5. **投注方案层**（¥50 保守版）

- 2-3 注，单注 ≤ ¥20，总仓位 ≤ ¥50
- 单方向 ≤ 60%（即主胜类注不超过 ¥30）
- 必含 Top3 比分中一注 或 角球正 EV 注
- EV < -30% 触发风险提示但不下注

6. **输出层**

- 写入 `analyses/aston-villa-vs-sunderland-20260419.md`
- 终端精简版（核心方案 + 关键理由 + 风险提示）
- 更新 `.workbuddy/memory/2026-04-19.md` 追加记录

## 关键注意点（避坑）

- **赔率 100% 实拉**，任何 "~X.XX" 估计值都禁止（2026-04-15 BTTS 脑补教训）
- **XGB 必开**（`--xgb`），否则只跑 MVP 子集（2026-04-18 教训）
- **伤停双向评估**：不能只看桑德兰客场伤停，必须同时看维拉主力状态
- **历史对桑德兰的判断需校准**：场次 #3 #17 证明其非鱼腩，不可按低估赔率线性外推
- **Isotonic Draw 偏高**：若 draw shift > 0.20，融合后 draw 仓位再 -30%
- **handicap_prob 已修**（2026-04-18），但仍要 assert 两侧 cover ≈ 1.0
- **角球极端回缩例外**：若一方控球预期 < 40%，角球修正 -2 ~ -3（海港/马竞三次验证）

## 输出文件

- `analyses/aston-villa-vs-sunderland-20260419.md`（一场一文件，11 模块完整）
- 更新 `.workbuddy/memory/2026-04-19.md`（追加本场分析条目）

## Agent Extensions

### Skill

- **football-betting-analyst**
- Purpose: 统筹赛前分析全流程（xG 深度 / 盘口价值 / Kelly 仓位 / 多层分层 / 复盘追踪），严格按 v5.3 规范产出 11 模块报告
- Expected outcome: 一份完整的 `analyses/aston-villa-vs-sunderland-20260419.md`，包含纯模型/纯脑算/融合三段 + 2-3 注保守方案 + 风险提示