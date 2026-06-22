# v5.7 模型+Skill 迭代计划

## 修改范围总览

| 优先级 | 改动 | 涉及文件 | 类型 |
|--------|------|---------|------|
| P0-1 | XGB源场景质量评分 + 过拟合自动warning | `predict_single.py` | 模型 |
| P0-2 | 纯模型高EV注强制保留机制 | `predict_single.py` + `decision.py` | 模型 |
| P1-1 | 进球荒评估升级(-15%→-25%) | `SKILL.md` | Skill |
| P1-2 | 角球H2H优先规则 | `SKILL.md` | Skill |
| P1-3 | 角球因子补充(射正比/射门比) | `features_v2.py` + `xgboost_model.py` | 模型 |
| P1-4 | 伤停影响量化优化 | `features_v2.py` + `xgboost_model.py` + `SKILL.md` | 模型+Skill |
| P1-5 | DNB+U2.5逻辑矛盾自动检测 | `predict_single.py` | 模型 |
| P1-6 | 欧战疲劳+保级保守双因子 | `SKILL.md` | Skill |

---

## Part A：模型层改动（代码）

### A1. XGB源场景质量评分 [P0-1]

**文件**: `scripts/predict_single.py` → `_build_xgb_feature_row()` (L210-347)

**当前问题**: XGB用"最近一场"做特征代理，但不输出源场景的质量信息。导致脑算无法判断XGB信号是否可信（维拉4-3桑德兰、水晶宫0-0西汉姆都因此翻车）。

**改动**:

在 `_build_xgb_feature_row()` 返回的 `info` dict 中新增 `xgb_source_quality` 字段：

```python
# 在 info["home_feature_source"] 之后（约L260），新增：
home_src_row = features_df[home_mask].iloc[-1]
away_src_row = features_df[away_mask].iloc[-1] if away_last is not None else None

# 源场景质量评分
source_quality = {}

# 1. 源场景进球数
home_src_goals = int(home_src_row.get("FTHG", 0)) + int(home_src_row.get("FTAG", 0))
source_quality["home_source_total_goals"] = home_src_goals
source_quality["home_source_clean_sheet"] = int(home_src_row.get("FTAG", 0)) == 0

if away_src_row is not None:
    away_src_goals = int(away_src_row.get("FTHG", 0)) + int(away_src_row.get("FTAG", 0))
    source_quality["away_source_total_goals"] = away_src_goals
    source_quality["away_source_clean_sheet"] = int(away_src_row.get("FTHG", 0)) == 0

# 2. 过拟合风险标记
overfit_risk = False
overfit_reasons = []
if home_src_goals <= 2 and source_quality["home_source_clean_sheet"]:
    overfit_risk = True
    overfit_reasons.append(f"主队源场景仅{home_src_goals}球+零封=清洁球，U2.5信号可能虚高")
if away_src_row is not None and away_src_goals <= 1:
    overfit_risk = True
    overfit_reasons.append(f"客队源场景仅{away_src_goals}球，进攻能力信号可能失真")

source_quality["overfit_warning"] = overfit_risk
source_quality["overfit_reasons"] = overfit_reasons

info["xgb_source_quality"] = source_quality
```

然后在 `predict_single_match()` 的 diagnostics 输出中（约L594）把 `xgb_source_quality` 加入：

```python
"xgb_source_quality": xgb_match_info.get("xgb_source_quality") if xgb_match_info else None,
```

**测试验证**: 跑一场已知过拟合的比赛(如维拉vs桑德兰)确认warning正确触发。

---

### A2. 纯模型高EV注强制保留机制 [P0-2]

**文件**: `scripts/predict_single.py` → `predict_single_match()` (约L507-559)

**当前问题**: 纯模型的正EV注单在JSON中输出了，但**融合/脑算阶段没有任何机制强制保留**。切曼+伯曼两场的教训是纯模型EV>+10%的注单被完全丢弃。

**改动**: 在JSON输出的 `plan` 部分新增 `pure_model_recommended` 字段，在脑算时形成强制参照：

在 `predict_single_match()` 最终输出前（约L530-540之间），构建纯模型推荐列表：

```python
# 纯模型独立推荐（不经脑算，直接从calibrated_probs出）
pure_model_bets = []
if odds:
    pure_markets = {
        "home_win": calibrated_probs.get("home_win", 0),
        "draw": calibrated_probs.get("draw", 0),
        "away_win": calibrated_probs.get("away_win", 0),
        "over_2_5": calibrated_probs.get("over_2_5", 0),
        "under_2_5": calibrated_probs.get("under_2_5", 0),
    }
    odds_map = {
        "home_win": odds.get("home_win_odds"),
        "draw": odds.get("draw_odds"),
        "away_win": odds.get("away_win_odds"),
        "over_2_5": odds.get("over_2_5_odds"),
        "under_2_5": odds.get("under_2_5_odds"),
    }
    for mkt, prob in pure_markets.items():
        mkt_odds = odds_map.get(mkt)
        if mkt_odds and mkt_odds > 1:
            ev = prob * mkt_odds - 1.0
            if ev > 0.10:  # EV > +10% 的纯模型注
                pure_model_bets.append({
                    "market": mkt,
                    "model_prob": round(prob, 4),
                    "odds": mkt_odds,
                    "ev": round(ev, 4),
                    "must_retain": True,  # 标记：融合方案必须保留此注 ≥50% 仓位
                    "rule": "v5.3: 纯模型EV>+10%→融合保留≥50%仓位",
                })
```

输出到JSON `plan` 下的新字段：

```python
plan_output["pure_model_recommended"] = pure_model_bets
```

**Skill侧配合**: SKILL.md 新增规则——看到 `pure_model_recommended` 中有 `must_retain: true` 的注单时，融合方案**必须保留该注**，仓位不低于纯模型Kelly的50%。

---

### A3. 角球因子补充 [P1-3]

**文件**: `src/features_v2.py` → `_compute_tactical_from_csv()` (L593-625) 和 `_compute_attack_defense_from_csv()` (L632-678)
**文件**: `src/models/xgboost_model.py` → `TRAIN_FEATURES` (L35-101)

**当前问题**: 角球预测只有 `T09_corners_per90`（单纯的场均角球数），缺乏角球产出的驱动因子。埃弗顿vs利物浦案例(43.6%控球但仅1角球)说明控球率≠角球产出，需要射正比等辅助因子。

**改动1** - `features_v2.py` 新增3个角球相关因子：

在 `_compute_attack_defense_from_csv()` 中追加计算（已有shots/sot数据在team_history里）：

```python
# 新增角球因子
T10b_corners_for_per90 = []     # 己方角球/场
T10c_corners_against_per90 = [] # 对手角球/场
A09b_sot_ratio = []             # 射正/射门比（角球驱动因子）

# 在循环中追加：
if not recent:
    T10b_corners_for_per90.append(np.nan)
    T10c_corners_against_per90.append(np.nan)
    A09b_sot_ratio.append(np.nan)
else:
    corners_for = [r["corners_for"] for r in recent if not np.isnan(r.get("corners_for", np.nan))]
    corners_against = [r["corners_against"] for r in recent if not np.isnan(r.get("corners_against", np.nan))]
    shots = [r["shots"] for r in recent if not np.isnan(r["shots"])]
    sot = [r["shots_on_target"] for r in recent if not np.isnan(r["shots_on_target"])]
    
    T10b_corners_for_per90.append(np.mean(corners_for) if corners_for else np.nan)
    T10c_corners_against_per90.append(np.mean(corners_against) if corners_against else np.nan)
    A09b_sot_ratio.append(np.sum(sot) / np.sum(shots) if shots and sum(shots) > 0 else np.nan)
```

同时需要在 `_compute_tactical_from_csv()` 的 team_history 积累中追加 `corners_for` 和 `corners_against` 字段（当前只记了"corners"但不分己方/对方）。

**具体修改 `_compute_tactical_from_csv()`**：在team_history.append中：
```python
team_history.setdefault(team, []).append({
    ...existing fields...
    "corners_for": _safe_int(row.get(f"{prefix_h}C", np.nan)),      # 己方角球
    "corners_against": _safe_int(row.get(f"{prefix_a}C", np.nan)),  # 对方角球
})
```

**改动2** - `xgboost_model.py` 的 `TRAIN_FEATURES` 追加：

```python
# 角球驱动因子 (v5.7 新增)
"T10b_corners_for_per90",       # 己方场均角球
"T10c_corners_against_per90",   # 对方场均角球
"A09b_sot_ratio",               # 射正/射门比（角球产出驱动因子）
```

**测试**: 回测英超确认新因子不降低现有市场(O2.5/U2.5)的准确率，且角球相关预测有改善。

---

### A4. 伤停影响量化优化 [P1-4]

**文件**: `src/features_v2.py` → 新增 `_compute_injury_factors_from_cli()` 
**文件**: `src/models/xgboost_model.py` → `TRAIN_FEATURES` 追加
**文件**: `scripts/predict_single.py` → 新增CLI参数

**当前问题**: S01-S14全是NaN(占位符)。伤停影响完全靠脑算手动评估，导致"切尔西进球荒"(-15%不够要-25%)、"桑德兰缺3进攻=崩塌"(实际进3球)等误判。

**设计思路**: 不指望自动拉伤停数据（数据源不稳定），而是**通过CLI参数手动注入关键伤停信号**，转化为XGB可用的特征。

**改动1** - `predict_single.py` 新增CLI参数：

```python
parser.add_argument("--home-injured-attack", type=int, default=0,
                    help="主队缺席的进攻球员数(首发级别)")
parser.add_argument("--home-injured-defense", type=int, default=0,
                    help="主队缺席的防守球员数(首发级别)")
parser.add_argument("--away-injured-attack", type=int, default=0,
                    help="客队缺席的进攻球员数")
parser.add_argument("--away-injured-defense", type=int, default=0,
                    help="客队缺席的防守球员数")
parser.add_argument("--home-goal-drought", type=int, default=0,
                    help="主队连续不进球场次数")
parser.add_argument("--away-goal-drought", type=int, default=0,
                    help="客队连续不进球场次数")
```

**改动2** - 在 `_build_xgb_feature_row()` 的 `market_overrides` 扩展中注入：

```python
# 伤停因子注入（从CLI传入）
if injury_data:
    market_overrides["S13_goal_threat_missing"] = injury_data.get("home_injured_attack", 0)
    market_overrides["S14_defensive_anchor_missing"] = injury_data.get("home_injured_defense", 0)
    # ...away同理...
    
    # 进球荒因子
    drought_h = injury_data.get("home_goal_drought", 0)
    drought_a = injury_data.get("away_goal_drought", 0)
    if drought_h >= 3:
        market_overrides["S15_goal_drought_home"] = drought_h
    if drought_a >= 3:
        market_overrides["S15_goal_drought_away"] = drought_a
```

**改动3** - `xgboost_model.py` TRAIN_FEATURES 追加：

```python
# 伤停因子 (v5.7 新增，CLI手动注入)
"S13_goal_threat_missing",        # 缺席进攻球员数
"S14_defensive_anchor_missing",   # 缺席防守球员数
"S15_goal_drought_home",          # 主队连续不进球场次
"S15_goal_drought_away",          # 客队连续不进球场次
```

> 注意：由于历史CSV中没有伤停数据，这些特征在训练时全为NaN，XGB会自动处理(native missing)。但在预测时如果传入了具体值，XGB会利用该信号。这种"训练时NaN+预测时有值"的模式在XGBoost中是合法的（tree split会走missing branch或explicit branch）。

**改动4** - diagnostics输出中记录伤停输入：

```python
"injury_input": {
    "home_injured_attack": N,
    "home_injured_defense": N,
    "away_injured_attack": N,
    "away_injured_defense": N,
    "home_goal_drought": N,
    "away_goal_drought": N,
}
```

---

### A5. DNB+U2.5逻辑矛盾自动检测 [P1-5]

**文件**: `scripts/predict_single.py` → `predict_single_match()` 的 diagnostics 输出部分

**改动**: 在plan_output构建后（约L550），新增一致性检查：

```python
# 方案内部一致性检查
consistency_warnings = []
bet_markets = [b["market"] for b in plan_output.get("bets", [])]

# 检测1: DNB(看好某方胜) + U2.5 = 逻辑矛盾
has_home_dnb = any("home" in m and "dnb" in m.lower() for m in bet_markets)
has_away_dnb = any("away" in m and "dnb" in m.lower() for m in bet_markets)
has_u25 = "under_2_5" in bet_markets

if (has_home_dnb or has_away_dnb) and has_u25:
    consistency_warnings.append({
        "type": "DNB_U25_CONFLICT",
        "severity": "high",
        "message": "DNB(看好某方胜≥1球) + U2.5(总球≤2) = 仅1-0/2-0可行，概率极低",
        "suggestion": "考虑用BTTS No替代U2.5，或降低U2.5仓位",
    })

# 检测2: 看好A胜 + BTTS Yes + U2.5 = 三重矛盾
has_btts_yes = "btts_yes" in bet_markets
if has_u25 and has_btts_yes:
    consistency_warnings.append({
        "type": "U25_BTTS_CONFLICT", 
        "severity": "high",
        "message": "U2.5 + BTTS Yes = 仅1-1可行，概率约12-15%",
    })

diagnostics["consistency_warnings"] = consistency_warnings
```

> 注意：当前plan中的market是"home_win/over_2_5"等标准名，DNB不是标准市场。这个检测更适合在**Skill层**做（脑算出方案后自检）。代码层做标准市场间的矛盾检测(如U2.5+BTTS Yes)，Skill层做非标准市场(DNB)的逻辑检测。

---

## Part B：Skill层改动（SKILL.md）

**文件**: `/Users/a1_builder/.workbuddy/skills/football-betting-analyst/SKILL.md`

### B1. 进球荒评估升级 [P1-1]

在"经验积累"章节新增规则：

```markdown
- **进球荒评估升级 v5.7**（2026-04-23）：
  - 3-4连场不进球 → 进球概率 -15%（维持原规则）
  - **5+连场不进球 → 进球概率 -25%**（切尔西5连0验证）
  - **BTTS额外 -20%**（5+连场不进球方的BTTS Yes必须额外打折）
  - 进球荒是结构性崩溃信号，不是均值回归反弹信号
  - 脑算禁止对5+场进球荒做"触底反弹"修正（切曼案例教训）
```

### B2. 角球H2H优先规则 [P1-2]

在"经验积累"章节新增：

```markdown
- **角球预测H2H优先规则 v5.7**（2026-04-23）：
  - 当H2H近10场角球有**≥7次同方向**时（如7/10走小），**H2H权重 > 通用德比修正**
  - 埃弗顿vs利物浦案例：H2H 7/10走小 > 德比+1.5修正 → 实际7角球
  - 角球修正优先级：①H2H角球数据 ②射正/射门比(A09b) ③控球率推算 ④德比通用修正
  - 控球率→角球正相关(71%控球→11角球)，但控球率≠进球效率
  - 控球<40%→角球-2~3修正（维持原规则）；控球<35%→角球-3~4修正
```

### B3. 纯模型强制保留（Skill侧配合A2）

在"纯模型调用规范"章节新增：

```markdown
### 🚨 纯模型高EV注强制保留规则 v5.7

跑完 `predict_single.py --xgb --json` 后，检查JSON中的 `plan.pure_model_recommended` 字段：

1. 如果有 `must_retain: true` 的注单（纯模型EV>+10%）：
   - **融合方案必须保留该注**
   - **仓位不低于纯模型Kelly建议的50%**
   - 脑算可以调整方向但不能完全丢弃
   
2. 违反案例回顾：
   - 切尔西vs曼联：纯模型U2.5 EV+11.3% → 融合方案丢弃 → 纯模型+190% vs 融合-76%
   - 伯恩利vs曼城：纯模型U2.5 EV+17.6% → 融合放弃 → 纯模型+40% vs 融合+0.14%
   
3. 分析文件模板新增必填表格：
   | 纯模型推荐 | EV | 融合是否保留 | 保留仓位 | 丢弃理由（如果丢弃）|
```

### B4. XGB过拟合warning处理规则（Skill侧配合A1）

```markdown
### XGB源场景质量检查 v5.7

跑完模型后，检查 `diagnostics.xgb_source_quality`：

1. 如果 `overfit_warning: true`：
   - 该场XGB在U2.5/O2.5市场的shift **自动打5折**
   - 例：XGB shift = +15pp O2.5 → 实际只取+7.5pp
   - 在分析文件中标注 "⚠️ XGB过拟合风险: {overfit_reasons}"

2. 如果XGB极端移动(>20pp)：
   - 与弱队自身进攻属性一致（如Burnley主场进攻弱）→ 信任50%仓位（v5.6规则）
   - 与弱队自身属性不一致（如源场景对手不同）→ 仅30%仓位
   - `overfit_warning: true` 时 → 进一步降到20%仓位
```

### B5. 欧战疲劳+保级保守双因子 [P1-6]

```markdown
- **欧战疲劳+保级客队保守=U2.5优先信号 v5.7**（2026-04-23）：
  - 当满足：主队欧战后3天内+客队保级方→O2.5需 **-15~20%修正**
  - 水晶宫0-0西汉姆完美验证（欧战疲劳+保级保守→0球闷平）
  - 脑算禁止仅给-3%修正（本场教训）
  - 保级队客场优先保平策略（战意≠进攻输出）
```

### B6. 伤停评估优化（Skill侧配合A4）

```markdown
### 伤停评估量化框架 v5.7

调用模型时**必须传入伤停参数**：
```bash
--home-injured-attack 2 --away-injured-defense 1 --away-goal-drought 5
```

伤停评估原则：
1. **缺进攻球员≠零进球**：缺N个进攻球员→进球预期 **-10~15%×N**（不是-30%×N）
   - 维拉vs桑德兰教训：桑缺3进攻球员仍进3球（替补爆发）
2. **双向评估**：伤停必须同时评估对己方和对手的影响
   - 曼阿案例：只看阿森纳伤停6人，忽视曼城主场10场不败
3. **进球荒 > 伤停**：N+1场进球荒比伤停更可靠（结构性 vs 偶然性）
4. **赛前2小时最终确认**：强制执行（水晶宫Lacroix首发翻转了伤停叙事）
```

---

## 实施顺序

### 第1批（模型代码，约40分钟）
1. **A1**: `predict_single.py` 新增 `xgb_source_quality` (20行)
2. **A2**: `predict_single.py` 新增 `pure_model_recommended` (30行)
3. **A5**: `predict_single.py` 新增 `consistency_warnings` (25行)
4. 测试：跑一场英超确认JSON输出正确

### 第2批（特征工程，约30分钟）
5. **A3**: `features_v2.py` 新增3个角球因子(40行)
6. **A3**: `xgboost_model.py` TRAIN_FEATURES追加3个(3行)
7. **A4**: `predict_single.py` 新增伤停CLI参数(15行)
8. **A4**: `features_v2.py` + `xgboost_model.py` 伤停因子(20行)
9. 测试：跑 `pytest tests/` 确认不破坏现有测试

### 第3批（Skill更新，约20分钟）
10. **B1-B6**: `SKILL.md` 更新所有新规则
11. 验证：用一场实际比赛走完整流程确认新规则生效

### 验收标准
- [ ] JSON输出包含 `xgb_source_quality.overfit_warning`
- [ ] JSON输出包含 `plan.pure_model_recommended` (EV>10%的注单)
- [ ] JSON输出包含 `diagnostics.consistency_warnings`
- [ ] 新角球因子 `T10b/T10c/A09b` 在features中正确计算
- [ ] `--home-injured-attack` 等CLI参数能正确传入并体现在diagnostics
- [ ] SKILL.md包含v5.7所有6条新规则
- [ ] `pytest tests/` 全部通过（允许preexisting的5个失败）
