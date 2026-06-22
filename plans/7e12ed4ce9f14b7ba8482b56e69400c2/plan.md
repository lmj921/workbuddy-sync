## 用户需求

分析今晚（2026-04-18）4场英超比赛，验证本周刚调整的模型（models/E0/，04-17训练）效果：

1. 利兹联 vs 狼队
2. 纽卡斯尔 vs 伯恩茅斯
3. 热刺 vs 布莱顿
4. 切尔西 vs 曼联

## 核心交付

- 每场独立 v5 完整分析（11模块+角球+四方对比），¥100 bankroll
- 一场一文件，禁止合并（MEMORY.md硬规则）
- 模型效果验证维度：本周新模型 vs 历史基线对比、校准后概率 vs 隐含概率差值、纯模型方案假设结算 vs 融合方案 ROI 差
- 4场跑完后输出汇总与串关评估（不提前承诺串关）

## 必选产出项（每场）

- Part 1 纯模型（概率/λ/EV/Kelly/比分矩阵/亚盘/Elo 诊断）
- Part 2 纯脑算（阵容/战意/战术/主客场/盘口）
- Part 3 融合方案（含角球市场强制评估）
- 补充 A xG 深度
- 补充 B 命中矩阵
- 补充 C 注单一致性检查
- 补充 D 临场调整清单
- 补充 E 同类比赛对比（从 analyses/ 中找最近相似场）
- 补充 F 经验教训检查（核对 MEMORY.md）
- 角球专项 + 控球<40%修正
- 纯模型假设结算 vs 融合方案 ROI 对比

## 风控约束（近期状态）

- 4/16~4/17 连续 2 场全灭，累计 ROI 仅 +3.7%，需仓位保守
- 新模型未实盘验证，建议单场总仓位 ≤ 6%
- 单方向总仓位 ≤ 60%、脑算单市场修正 ≤ ±15%、高EV(≥15%)纯模型注保留 ≥50% 仓位
- 投注方案必须包含 Top3 比分中一个比分注

## 技术方案

### 执行架构

沿用项目既有三段式工作流（config/analysis-template.md v5），所有4场严格复用同一流程，不引入新脚本、不改动模型权重文件。

```
赔率获取 → predict_single.py(纯模型JSON) → 脑算增量 → 融合方案 → Markdown输出
```

### 关键脚本与数据

- 预测: `scripts/predict_single.py --model-dir models/E0 --json`
- 赔率: `scripts/odds_api.py`（实拉，禁脑补）+ Web 搜索交叉验证
- 数据: `data/E0.csv`（刚刷新，含训练集到 2026-04-17）
- 模板: `config/analysis-template.md` 11模块
- 模型诊断: 读 `models/E0/meta.json` + `poisson_params.json` + `elo_ratings.json`，确认本周调整的具体影响（校准偏移、Elo更新幅度、攻防因子变化）

### 队名映射（football-data.co.uk 标准）

| 中文 | 映射值 |
| --- | --- |
| 利兹联/狼队 | Leeds / Wolves |
| 纽卡斯尔/伯恩茅斯 | Newcastle / Bournemouth |
| 热刺/布莱顿 | Tottenham / Brighton |
| 切尔西/曼联 | Chelsea / Man United |


### 市场覆盖（每场）

- 1x2（主胜/平/客胜）
- 大小球 O/U 2.5
- BTTS
- 亚盘 AH（取主流盘口）
- 角球 O/U（总角球 + 主/客单边）
- 正确比分（至少 Top3 之一入选）

### 模型效果验证维度（本周调整看点）

1. 每场对比"纯模型注单假设结算 ROI" vs "融合方案 ROI"
2. 校准偏移（home_win / over_2_5 校准前后差值）
3. Elo 差与盘口隐含优势的一致性
4. 4场汇总后输出新模型命中倾向诊断（偏主/偏客/偏小/偏大）

### 文件输出规范

一场一文件，命名 `{home}-vs-{away}-20260418.md`，放在 `analyses/`：

- analyses/leeds-vs-wolves-20260418.md
- analyses/newcastle-vs-bournemouth-20260418.md
- analyses/tottenham-vs-brighton-20260418.md
- analyses/chelsea-vs-manutd-20260418.md
- analyses/epl-4matches-summary-20260418.md（汇总+串关评估+新模型效果验证）

### 风控执行规则（强约束）

- 单场总仓位 ≤ 6%（4场并行，总仓位 ≤ 24%）
- 脑算单市场修正幅度 ≤ ±15%
- 高 EV（≥15%）纯模型注单至少保留 50% 仓位
- 单方向总仓位（全部主胜/全部大球等）≤ 60%
- 每场角球市场必选评估，控球劣势方 < 40% 触发 -2~3 修正
- 伤停必须双向评估，不能只列一方

## 目录变更

```
football-betting/
├── analyses/
│   ├── leeds-vs-wolves-20260418.md             # [NEW] 利兹 vs 狼 v5完整分析
│   ├── newcastle-vs-bournemouth-20260418.md    # [NEW] 纽卡 vs 伯恩茅斯 v5完整分析
│   ├── tottenham-vs-brighton-20260418.md       # [NEW] 热刺 vs 布莱顿 v5完整分析
│   ├── chelsea-vs-manutd-20260418.md           # [NEW] 切尔西 vs 曼联 v5完整分析
│   └── epl-4matches-summary-20260418.md        # [NEW] 4场汇总+串关评估+新模型效果诊断
└── .workbuddy/memory/
    └── 2026-04-18.md                           # [NEW/UPDATE] 当日记忆：新模型首轮实战效果
```

## Agent Extensions

### Skill

- **football-betting-analyst**
- Purpose: 加载项目已安装的足球博彩分析专家 skill，强制落地 v5 11模块规范、凯利仓位、角球必选、一场一文件等硬规则
- Expected outcome: 每场分析严格按 config/analysis-template.md 结构输出，零模块遗漏，风控约束全部体现

### SubAgent

- **code-explorer**
- Purpose: 在补充分析 E（同类比赛对比）阶段跨 analyses/ 目录（34+文件）检索结构最相似的历史场次，为每场比赛匹配对标案例
- Expected outcome: 每场找到 1 个最接近的历史分析，提取赛果与借鉴点