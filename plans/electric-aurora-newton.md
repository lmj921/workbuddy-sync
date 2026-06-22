# 分析计划：申花 vs 深圳新鹏城 (中超第14轮, 2026-05-24)

## 目标
为明天的中超比赛生成完整三段式赛前分析文件 `analyses/shenhua-vs-shenzhen-20260524.md`

## 执行步骤

### Step 1: 运行预测模型
```bash
python3 scripts/predict_single.py \
  --model-dir models/CHN \
  --home "Shanghai Shenhua" --away "Shenzhen Xinpengcheng" \
  --bankroll 750 --json
```
- 获取 λ_home/λ_away、Elo修正、校准概率、比分矩阵
- 注意: XGB 未激活(CHN CSV格式缺列)，仅 Poisson+Elo+Isotonic

### Step 2: 获取实时赔率
- 用 WebSearch 搜索明天申花vs深圳的赔率（500彩票网/竞彩/澳门盘）
- 覆盖: 胜平负、让球、大小球、BTTS
- 记忆规则: 赔率必须实拉禁止脑补

### Step 3: 伤停情报收集
- WebSearch 搜索申花最新伤病更新（上轮7-8人缺阵是否恢复？）
- WebSearch 搜索深圳新鹏城阵容情况
- 伤停须双向评估+2次验证(E规则)

### Step 4: 双方近况整理
- 申花: 近5场战绩、主场表现、核心数据（上轮vs武汉赛果?）
- 深圳: 近5场战绩、客场表现、外援情况
- 关注联赛积分榜位置、保级/争冠动力

### Step 5: 撰写三段式分析
按照标准模板:
1. **Part 1 纯模型输出**: λ值、概率矩阵、比分矩阵、模型诊断
2. **Part 2 脑算分析**: 近况、伤停、战术、概率评估、核心逻辑
3. **Part 3 融合投注方案**: 60/40融合、EV计算、E规则检验、最终注单(≤3注)

### Step 6: 赛前核查清单
- E69: 注单≤3
- E70: raw_prob检查
- E71: Kelly>2%
- E80: 伤病雪崩评估
- 实盘赔率确认提醒

## 关键文件
- 输出: `analyses/shenhua-vs-shenzhen-20260524.md`
- 模型: `models/CHN/` (poisson_params.json, elo_ratings.json, calibrator.pkl)
- 脚本: `scripts/predict_single.py`
- 参考: `analyses/shenhua-vs-wuhan-20260520.md` (最近一场申花分析)

## Bankroll 档位
- ¥750 (喜欢球队-申花)

## 注意事项
- Elo 滞后性: 1750.8 可能已不准确（近期连败）
- 深圳 Elo 仅 1457.8，Poisson客场攻击因子0.670极低
- E80 伤病雪崩: 需确认申花伤兵是否回归
- 中超特规: 点球溢价+0.3 | 弱主λ修正 | 反击λ+0.2~0.3
