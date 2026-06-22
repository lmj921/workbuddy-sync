# 中超足球分析工作流理解计划

## 探索成果总结

### 1. predict_single.py CLI 接口
**完整命令格式**：
```bash
python3 scripts/predict_single.py \
  --csv data/CHN.csv \
  --home "上海海港" --away "天津津门虎" \
  --model-dir models/CHN \
  --home-odds 1.95 --draw-odds 3.50 --away-odds 4.20 \
  --over-odds 1.85 --under-odds 2.00 \
  --btts-yes-odds 1.70 --btts-no-odds 2.15 \
  --ah-line -0.5 --ah-home-odds 1.95 --ah-away-odds 1.95 \
  --xgb --xgb-blend 0.6 \
  --json --bankroll 100
```

**核心参数**：
- `--csv`: 数据源 (中超用 CHN.csv)
- `--home/--away`: 球队名称（需与CSV匹配）
- `--model-dir`: 预训练模型目录（models/CHN）
- 赔率参数：home/draw/away/over/under/btts-yes/btts-no/ah-line/ah-home/ah-away
- 初盘参数：home-open-odds/draw-open-odds/away-open-odds/over-open-odds/ah-line-open
- `--xgb`: 启用XGBoost 73因子融合
- `--json`: JSON输出格式
- `--bankroll`: 投注本金（默认100）

### 2. 中超模型文件结构
**位置**: `/Users/a1_builder/WorkBuddy/football-betting/models/CHN/`

**文件清单**：
- `poisson_params.json` - 攻防因子系数（45支球队）
- `elo_ratings.json` - Elo评分系统
- `calibrator.pkl` - 概率校准器（IsotonicRegression）
- `meta.json` - 元数据
  - 训练时间：2026-04-17
  - n_teams_poisson: 45队
  - n_teams_elo: 45队
  - 校准市场：home_win/draw/away_win/over_2_5/under_2_5

### 3. 分析文件markdown模板
**标准章节结构**（从shenhua-vs-haigang-20260411.md提取）：

```
# [队伍A] vs [队伍B] | [赛事类型]

> **赛事信息**: 日期/时间/场地
> 分析时间：YYYY-MM-DD HH:MM | 分析师：Football Betting Analyst vX

---

## 🔄 临场更新

### 🌦️ 天气情况
[天气表格 + 影响评估]

### 👥 预测首发阵容
[两队首发阵容表 + 关键变量]

### 📊 盘口最新变化
[初盘/即时盘变化表 + 解读]

### ⚡ 临场关键变量总结
[变量表格 + 对方案影响]

---

## 📊 核心数据摘要

### 两队赛季战绩
[战绩表：战胜数/积分/进/失/净胜球]

### 近期状态详情
[轮次表：对手/比分/亮点]

### 阵容&伤停情况
[球员伤停状态表]

### 历史交锋
[近5场对阵记录表]

### 盘口&赔率数据
[亚盘变化 + 大小球 + 四维解读]

---

## 🎯 概率评估

### 权重体系应用
[因子权重表：xG/主客场/近期战绩/历史交锋/均值回归/心理因素等]

### 胜平负概率
[我的评估 vs Pinnacle隐含 vs 偏差]

### 让球盘评估
[赢盘/走水/输盘概率]

### 大小球评估
[预期总进球 + O/U概率]

### BTTS评估
[BTTS Yes/No概率 + 依据]

---

## 💰 投注方案

### 方案逻辑一致性检查
[检查核心注之间的逻辑完整性]

### 🟢 核心注 (30-60%仓位)
### 🟡 价值注 (20-40%仓位)
### 🔴 博冷注 (5-15%仓位)

每注包含：
- 投注项 + 赔率范围
- 资金占比
-凯利建议
- 置信度星级
- 逻辑依据
- 风险点

### 资金分配汇总
[表格汇总所有注单]

### 场景分析
[比分场景 → 结算结果表]

---

## ⚠️ 风险评估

### 最大不确定性
[列举3-5个最关键风险]

### 临场调整清单
[赛前检查项 - checkbox]

### 复盘教训
[从历史比赛吸取的具体教训]

---

## 📌 最终建议

- **如果只买一注** → [推荐项]
- **如果买两注** → [推荐组合]
- **如果全方案** → [按比例执行]

---

## 📋 复盘数据（赛后填写）

[比分/各注单结果/ROI/经验总结]

---

> ⚠️ 免责声明：本分析仅供参考...
```

### 4. 最近中超分析案例 - 海港/天津相关

**海港案例文件**：
- `/Users/a1_builder/WorkBuddy/football-betting/analyses/shenhua-vs-haigang-20260411.md` - 申花vs海港（R5）
  - 关键发现：近5场德比BTTS 100%命中，场均3.6球
  - 核心注：BTTS Yes (30%) + 申花不败 (25%)
  - 临场调整：让-克劳德回归→海港防守强化→降低直胜仓位

- `/Users/a1_builder/WorkBuddy/football-betting/analyses/guoan-vs-haigang-20260510.md` - 国安vs海港（R11）
  - 数据驱动：海港外援严重缺阵（仅维塔尔），EV最高的是U2.5和BTTS No
  - 脑算修正：4v1外援碾压 + 穆帅5后卫体系 → U2.5微调上升

- `/Users/a1_builder/WorkBuddy/football-betting/analyses/tianjin-vs-shenhua-20260405.md` - 天津vs申花
  - 存在但未详细查看

**赔率脚本工具**：
- `/Users/a1_builder/WorkBuddy/football-betting/scripts/odds_api.py`
  - 通过 the-odds-api.com 获取40+家博彩公司赔率
  - 支持中超：`--league csl` 或 `--league 中超`
  - 输出格式兼容 predict_single.py

### 5. 工作流程完整链路

```
数据输入 (CSV) 
    ↓
predict_single.py 加载模型 (models/CHN/)
    ├─ 泊松模型 (poisson_params.json)
    ├─ Elo评分 (elo_ratings.json)
    └─ 概率校准 (calibrator.pkl)
    ↓
纯模型输出 (概率矩阵)
    ├─ λ_home/λ_away (泊松参数)
    ├─ home_win/draw/away_win (胜平负)
    ├─ over_2_5/under_2_5 (大小球)
    └─ BTTS yes/no (双方进球)
    ↓
融合因子处理
    ├─ XGBoost 73因子 (可选 --xgb)
    ├─ 赔率输入 (手动或自动拉取)
    └─ 伤停/天气信息 (可选参数)
    ↓
投注方案生成
    ├─ EV计算 (期望值)
    ├─ Kelly分数 (仓位管理)
    └─ 分层分配 (核心注/价值注/博冷)
    ↓
Markdown报告生成
    └─ 三部分结构：纯模型 + 投注方案 + 诊断信息
```

## 后续问题需澄清

1. **中超特殊性**：predict_single.py 中有特殊的 CSL 弱主 λ 熔断规则（v5.7c）和 Elo 大失衡简化规则，这些是否应该在报告中强调？

2. **赔率来源**：实际分析中使用的赔率是从 odds_api.py 自动拉取，还是手动输入的历史赔率数据？

3. **天气/伤停数据**：这些信息如何获取？是人工查阅还是有自动化渠道？

