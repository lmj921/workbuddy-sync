# Global Memory

> 跨 workspace 的长期记忆，所有 workspace 共享。
> 最后更新：2026-04-19

---

## 用户画像

- **昵称**：Joker
- **角色**：工作室 PM 负责人
- **偏好**：简洁高效、中文沟通
- **时区**：Asia/Shanghai (GMT+8)
- **系统**：macOS

## 工作项目

| 项目 | 类型 | 状态 |
|------|------|------|
| PCHG | 搜撤微恐类 repo 游戏，团队 ~50 人 | Pre-Alpha |
| Maple端游 | 搜撤射击游戏 | — |
| Maplemobile | Maple 手游版本 | — |
| ProZ | 项目 3 | — |
| XYMini | 微信小游戏，对标生存33 | — |

---

## 投资持仓（截至 2026-03-19）

### RBLX (Roblox Corporation)
- **持仓**：40 股 @ 均价 $77（分四笔：$92、$82、$72、$62 各 10 股）
- **3/19 股价**：~$58，浮亏约 $760（-24.7%）
- **分析建议**：HOLD + 分批加仓
  - 第一批：$55-58 买 5 股
  - 第二批：$50 附近买 10 股
  - 第三批：技术面确认反转后加 5-10 股
  - 硬止损：$42
  - 基本面止损：Q1 DAU <30% 或预订量负增长则清仓
- **关注催化**：Q1 财报（5 月初）、50 日均线企稳

### CRCL (Circle Internet Group)
- **持仓**：20 股 @ $104（成本 $2,080）
- **3/24 股价**：$101.17，浮亏 -$56.60（-2.7%）— CLARITY Act 暴跌 -20.11%
- **分析建议**：HOLD — 等法案明朗
  - 核心业务（USDC mint/redeem）未受损
  - 收益禁令仅影响新产品线
  - 回调加仓区：$90-95
  - 止损线：$70
- **关注催化**：CLARITY Act 参议院表决（4 月）、Q1 财报（5 月）、Fed 利率决议

### ARKK (ARK Innovation ETF) — 跟踪中
- **未持仓**，仅做 Cathie Wood 操作跟踪
- **自动化日报**：3/9~3/25 持续生成，存放于 `~/WorkBuddy/arkk-tracker/`
- **最新状态（3/24）**：$69.00（-2.71%），CLARITY Act 稳定币禁令恐慌
- **ARK 近期动向**：逆势抄底 CRCL 116,123股（~$11.7M），卖出6只中小仓位回收弹药

---

## 完成过的任务

### 2026-03-13
- **ARKK 每日跟踪系统搭建** — 浏览器自动化抓取 ARK 官网+腾讯财经，生成日报+Excel
- **加班餐费报销** — 从 5 份发票 PDF 提取信息填入 Excel 报销表（策划/服务器/客户端/美术/PM运营），人均 50 元餐标，超额按预算填

### 2026-03-17
- **巴萨盘口分析** — 巴塞罗那 2025-26 赛季全部比赛（~40 场）盘口走势 HTML 报告 + Excel 导出
  - 存放于 `~/WorkBuddy/20260317114135/`

### 2026-03-19
- **RBLX 投资分析** — 完整 5 阶段多角色辩论分析，结论 HOLD+分批加仓
- **CRCL 投资分析** — 完整 5 阶段多角色辩论分析，结论 HOLD+分档止盈
  - 存放于 `~/WorkBuddy/stock-analysis/`

### 2026-03-20
- Onboarding 完成（IDENTITY.md + USER.md）
- 确认企微不支持私聊其他人（WorkBuddy 是机器人角色）

### 2026-03-21
- 足球博彩分析系统搭建：Skill + 复盘追踪器 + 盘口分析工具增强
  - Skill: `~/.workbuddy/skills/football-betting-analyst/SKILL.md`
  - 复盘器: `~/WorkBuddy/football-betting/betting-tracker.html`
  - 增强: `~/WorkBuddy/20260317114135/` 新增 value-engine.js + 价值分析/盘口变化 Tab
- **布莱顿 vs 利物浦** 完整投注分析 + 实战验证
  - 核心注 ✅ Brighton +0.25 @2.00（用户实际下注 50 元，净赚 +50）
  - 踩坑：500.com 盘口数据不准，改用 football-data.co.uk 重做
- **TAPD 催单系统搭建**（Maple 项目）
  - 脚本: `~/WorkBuddy/Claw/maple_story_reminder.py`
  - Skill: `~/.workbuddy/skills/tapd-reminder/`
  - 定时任务：周一-六 16:00 + 20:00
  - 踩坑：企微 Webhook 频率限制 45009 → 5s 间隔 + 指数退避重试
- **ARKK** 补生成 3/20 日报（三巫日）+ Week 12 完整周报
- **RBLX/CRCL 定时分析** 调整为周日 10:00 + 企微推送

### 2026-03-22
- **WorkBuddy Vault** GitHub 仓库搭建 — 整理 41 个文件到 Obsidian Vault，push 到 github.com/lmj921/workbuddy_vault
  - 存放于 `~/WorkBuddy/workbuddy_vault/`
  - iOS 同步方案：Working Copy + Obsidian
- **XYMini 开发方案** — Multi-Agent 架构设计 + 《生存33天》深度竞品拆解
  - 核心循环：搜打撤（6.5min），6层数值递进，付费金字塔
  - 开发架构：WorkBuddy 任务管理 + CodeBuddy Agent Teams 编码 + Skills 知识库
  - 存放于 `~/WorkBuddy/20260321162425/`
- **富勒姆 vs 伯恩利** 投注分析+复盘 — 核心方向错误（伯恩利+0.75），总计 -1.2%
  - 教训：历史交锋样本<10 不可靠；心理因素难以量化；进球类投注更稳定
- **纽卡斯尔 vs 桑德兰** 投注分析+临场更新+复盘 — 5注命中4注，+120.7% ROI
  - 用户实际下注 75 元，全赢（+42.5 元主注）
  - 关键：逆向思维（93% 公众押主胜→翻车），临场托纳利缺阵触发方案升级
- **热刺 vs 诺丁汉森林** 赛前分析 — 看好森林不败+大球
- **RBLX 每周投资分析** — 周报 HOLD，等 $52-54 加仓

### 2026-03-23
- **加班餐报销目录重构** — 从扁平结构改为按日期分文件夹 + Excel 追踪列
  - 已有 3/14 数据（5组58人2861.6元），新增 3/21 两条（服务器+PM运营策划）
  - 存放于 `~/WorkBuddy/A1周六加班餐报销/`
- **ARKK Week 12 周报修订** — 补充 3/20 三巫日交易数据，操作总额 $1.6M→$25.0M
  - FIG 新建仓 $6.4M（ATH 跌-83%），卖出 TER/CRCL/BLSH 共 $14.0M
  - 叙事翻转：静默观察→蛰伏四日→周五雷霆换仓

### 2026-03-24
- **港美股 AI 量化交易系统搭建** — Qlib + Futu OpenAPI，完整项目骨架 + 首次数据拉取
  - 架构：src/{data,model,signal,trader,risk} + YAML config + CLI
  - 港股 Futu 10/10 成功（14815条），美股 Futu 受限→yfinance 10/10 成功（15630条）
  - Qlib 0.9.7 无 dump_bin→自写二进制转换
  - 存放于 `~/WorkBuddy/stock_trader/`
- **XYMini 新工程创建与资源迁移** — 从老工程迁移 341 个美术资源到 survival-demo
  - Unity 2021.3.45f2c1 + 2D URP 模板，5 个核心 Skills 落地
  - 存放于 `~/Documents/survival-demo/survival_unity/`
- **加班餐报销 3/21 补齐** — 客户端+美术发票入库（4/4 完成）
- **ARKK 日报** — 3/23 报告日，$70.92 (+2.56%)

### 2026-03-25
- **Futu 自选股发现+重组** — 发现自选股 272 只可作为量化训练池（10-15x 扩展）
  - 设计 12 行业 + 7 策略 = 19 个分组方案
  - 构建 regroup_watchlist.py（--plan/--execute），23 项操作全部完成
  - 存放于 `~/WorkBuddy/stock_trader/scripts/`
- **CRCL 暴跌分析** — CLARITY Act 稳定币收益禁令引发 -20.11%
  - 三重原因：政策泄露 + Tether 审计通过 + 技术面超买
  - 判断：预期修正式暴跌，核心业务未受损，HOLD
  - 存放于 `~/WorkBuddy/stock-analysis/CRCL-weekly/`
- **泡泡玛特 (9992.HK) 投资分析** — 年报日暴跌 -22.51%，完整 5 阶段分析
  - 营收 +185%/净利 +309%，但 LABUBU 单 IP 依赖 38.1%
  - 结论：HOLD/等企稳后分批建仓 HK$155-170
  - westock-data skill 首次验证，8/9 端点可用
  - 存放于 `~/WorkBuddy/stock-analysis/`
- **ARKK 日报** — 3/24 报告日，$69.00 (-2.71%)，ARK 逆势抄底 CRCL $11.7M
- **球队盘口数据更新** — 新增 6 场比赛（含西甲 SP1 新数据源）

### 2026-03-26
- **推送方式定型** — 企微 Webhook + chatid=jokerlu 私聊推送（经历3次迭代：直接POST→Claw→chatid私聊）
  - 三个自动化任务（rblx-3、rblx、crcl）prompt 全部更新
  - 首次验证 chatid 私聊推送成功（errcode:0）
- **港股日报自动化创建** — automation-4，泡泡玛特+腾讯控股，周一至周五 18:00
  - 数据源：westock-data skill，输出 HTML + 企微推送
  - 存放于 `~/WorkBuddy/stock-analysis/HK-daily/`
- **量化系统标的池清理** — 231→205（移除 26 只问题标的：次新<120天+杠杆ETF+美股薄数据）
- **量化系统路线图** — `docs/ROADMAP.md`，5 Phase 17 子任务
- **StockManager 标的管理器** — CLI add/remove/list + 自动同步 3 个配置文件
- **因子分析 Task 1.1** — Alpha158 因子评估，结论：保持原始 158 因子（激进剪枝破坏协同）
- **ARKK 日报** — 3/25 报告日，$69.90 (+1.30%)，ARK 1买13卖大扫除
- **盘口跟踪系统迁移** — 从 `20260317114135/` 迁入 `football-betting/handicap-tracker/`
- **意大利 vs 北爱尔兰** — 完整分析+盘口变化+自我纠错+赔率横向对比
  - 用户实际下注 ¥80（3注），重仓"意大利零封"方向
  - 关键发现：净胜1球@3.35 负EV vs 净胜2球@3.90 正EV

### 2026-03-27
- **MiniMax vs WorkBuddy Skills 对比** — MiniMax 5 Skills vs WB 306+；最大差距是 shader-dev（WB 零覆盖），Office 差距不大
  - 报告：`~/WorkBuddy/Claw/minimax-vs-workbuddy-skills-comparison.md`
- **海天味业(03288.HK)投资分析** — 100股打新持仓，年报日SELL建议（RSI 84.7 + 南向净卖 + 小仓位）
  - 报告：`~/WorkBuddy/stock-analysis/HK03288-haitian-analysis-20260327.html`
- **港股日报** — 泡泡玛特 HK$149.60(-0.73%)暴跌后企稳 + 腾讯 HK$493.40(-0.44%)缩量整理
- **量化系统 Task 1.4 基本面因子** — 15因子接入，276/300覆盖(92%)
  - A/B实验：美股 Sharpe +2.5%(2.28→2.34)，港股 -7.6%(1.22→1.12)
  - 结论：美股用 FundamentalAlpha158，港股保持 Alpha158
- **ARKK 日报** — 3/26 报告日，$67.39(-3.59%)，ARK 1买15卖（3日累计49笔卖出，史上最密集）
- **意大利复盘** — 用户3注全中+¥88.7(ROI +110.9%)，AI原方案-8.5u；累计用户战绩4场+¥156.2(ROI +67.9%)
- **盘口-大小球三角关系分析** — EPL+Serie A+La Liga+CSL 3725场统计
  - 核心发现：盘口每深0.5球→进球+0.2球,大球率+5%；三角共振信号(让球中水+大球中低水)→上盘49.6%+大球62.8%
- **GitHub Trending 分析** — 黄仁勋五层模型分类，93%热门项目在L5应用层

### 2026-03-28
- **量化系统 Task 1.5.1 Regime Filter** — 市场状态过滤器，保守 Regime 推荐 Sharpe 2.02±0.37
  - 存放于 `~/WorkBuddy/stock_trader/src/signal/regime_filter.py`
- **量化系统 Task 1.5.2 多模型集成** — LGB+CatBoost 等权集成 Sharpe=2.45±0.31（+3.6%，方差降40%）
  - 关键：CatBoost 默认参数拉低集成→Optuna 30 trials 优化后集成显著优于单模型
  - 存放于 `~/WorkBuddy/stock_trader/scripts/us_ensemble.py`
- **量化系统 Task 1.5.3 动态风控** — DynamicRiskManager ~350行，参数校准（97%→82%触发率）
  - 美股: Sharpe -0.23→+1.09; 港股: 0%触发（不干预健康策略）
  - 存放于 `~/WorkBuddy/stock_trader/src/risk/manager.py`
- **Claude Code Game Studios 分析** — 48 Agent 游戏开发工作室评估，2D独立游戏适用度 7/10
  - 设计流程+代码能力强，但不生成美术资产；建议 Placeholder-first 开发
  - 存放于 `~/WorkBuddy/Claw/Claude-Code-Game-Studios-分析报告.md`
- **ARKK 日报** — 3/27 报告日，$64.63(-4.10%)，ARK 首次零买入+6卖，创新低
- **美股持仓日报** — RBLX $52.31(-2.86%) 进入加仓区 | CRCL $93.66(-4.69%) 周跌-26% | 组合 -$1112.50(-21.51%)

### 2026-03-29
- **量化系统 Task 2.1-2.3 模拟盘闭环** — executor.py 重构（258→480+行），实时报价+调仓+执行引擎
  - 港股 Dry-Run 通过：15笔BUY，849K HKD，零报错
  - 存放于 `~/WorkBuddy/stock_trader/src/trader/executor.py`
- **量化系统 Task 3.3 持仓相关性** — CorrelationChecker ~200行，发现3对强相关（ETF重叠/同系公司/同质大行）
  - 踩坑：高维 dropna 数据不足→改用 corr(min_periods=30)
- **量化系统 Task 2.4 美股实时行情** — USQuoteFetcher 三源降级（腾讯+Finnhub+Futu），7只全成功
  - 存放于 `~/WorkBuddy/stock_trader/src/trader/us_quote.py`
- **量化系统 Task 1.5.4 标的池分层** — PoolManager core/satellite/explore 三层（60%/30%/10%）
  - 存放于 `~/WorkBuddy/stock_trader/src/signal/pool_manager.py`
- **量化系统 Task 5.1 滚动训练** — rolling_train.py ~400行，安全门槛（Sharpe<阈值保留旧模型）
  - 港股 ensemble=1.480>0.8 ✅ | 美股 ensemble=0.786<1.5 保留旧模型 ✅
- **量化系统 Task 5.4 Streamlit Dashboard** — ~600行，4页（概览/信号/风控/模型）+ 股票名称显示增强
- **v0.2 Roadmap 制定+因子挖掘调研** — 13+框架调研，RD-Agent Conda 模式为首选
  - 用户4项决策确认：分析师因子延后、RD-Agent、LLM预算按需、资金流先做A/港股
  - 存放于 `~/WorkBuddy/stock_trader/docs/ROADMAP_v0.2.md`
- **CRCL 周报** — 周跌-25.7%（CLARITY Act），HOLD

### 2026-03-30
- **量化系统 Task 0.3 Daemon Mode** — APScheduler 守护进程，HK/US 全自动调度（开盘/盘中检查/收盘/月度训练），PID 防重复+健康检查+补跑+后台 fork
  - 存放于 `~/WorkBuddy/stock_trader/scripts/daemon.py`
- **美股 Dry-Run 6 Bug 修复** — HOLD 格式不匹配、跨午夜 weekday、卖出无序、字段缺失、BRK 代码错误
- **Logs 目录重整** — 从扁平 40+ 文件重构为 7 子目录（state/trade/events/reports/model/analysis/daemon），更新 8 个源文件路径
- **因子评估框架 Task 1.1-1.4** — FactorEvaluator（IC/IR/换手/分组/单调性/LS Sharpe）+ 相关性分析 + CLI，Plotly 暗色 HTML 报告
  - 存放于 `~/WorkBuddy/stock_trader/src/factor/evaluator.py`
- **WQ101 因子库 Task 2.1** — 79 个 WQ101 因子（7 大类），$vwap 替代方案，港股评估 0/79 严格通过但 10+ 具有 ML 特征价值
  - 存放于 `~/WorkBuddy/stock_trader/src/factor/alpha101.py`
- **Dashboard 增强** — 系统运行状态（daemon PID/运行时长）+ 操作日志页（事件时间线）+ 快速命令
- **操作手册 v1.1** — 新增系统启停速查 + venv 绝对路径 + daemon 后台模式
- **CRCL 加仓分析** — 盘前+3%死猫弹跳，三重不确定性 → 不加仓，维持 HOLD
- **加班餐报销 3/28** — 4 张发票录入，合计 2525 元

### 2026-03-31
- **量化系统 Dashboard 5+3 Bug 修复** — Top5排名错误、持仓盈亏无颜色、缺开盘价/日涨跌、股票名称缺失、港股12点缺检查、总资产占位值、红涨绿跌全局统一、标的池数量解析错误
  - 红涨绿跌：st.metric 默认绿涨红跌→MutationObserver JS 注入全局翻转
  - 存放于 `~/WorkBuddy/stock_trader/`
- **标的池 Dashboard 页面** — 新建"🏷️ 标的池"页面（统计/搜索/分层Tab/饼图/双市场对比），Score列从信号CSV获取
- **全量预测 Score 系统** — `daily_scores.py` 独立于交易流程，全标的池模型预测（HK 125只/US 129只，每市场~20s），daemon 开盘前15min调度
- **Daemon 清空重启** — 虚拟持仓/熔断器/止损/事件/日报全部清空，PID 78983 DRY-RUN 模式
- **波黑vs意大利投注分析** — 世预赛附加赛，意大利方向+复合盘口，Joker 实际下注 ¥90（3注：意大利赢&U3.5 @1.98 / HT和FT意大利 @4.00 / 净胜1球 @3.30）
- **英格兰vs日本投注分析** — 友谊赛，大球为主（温布利场均3.2球），4注方案¥125（未下注）
- **盘口变化追踪** — 波黑vs意大利赛前6h：全线升盘1-3档（机构坚定看意大利大胜），Polymarket 81% vs 博彩~70-75%存在恐慌溢价
- **football-betting-analyst Skill 升级** — 新增 Phase 1.5A（初盘vs即时盘对比/四维解读法）+ Phase 1.5B（Polymarket走势分析/三层对比法）
- **football-betting 目录整理** — 20+文件归入6子目录，github_trending迁出到独立workspace
- **量化投注工程化方案** — 五层架构设计（Data→Features→Model→Decision→Output），双泊松+XGBoost+凯利公式
- **因子体系v2** — 从25个扩展至72因子（8大类20子类），3tier权重分层，3期落地计划
- **Polymarket+GitHub预测模型调研** — sports-betting(681⭐)最佳回测框架，Elo+隐含概率是最重要特征
- **美股持仓日报** — RBLX $51.91(-0.76%)/CRCL $89.91(-4.00%)，组合 -$1166(-22.54%)
- **港股日报** — 泡泡玛特 HK$143.60(-3.43%)连跌7日 / 腾讯 HK$484.00(+0.50%)止跌回升
- **GitHub Trending W14 周报** — 手动执行+配置验证，superpowers 重回#1
- **WorkBuddy 命令审批调研** — 桌面版无 permissions 配置，建议 CLI 版或 requires_approval:false

### 2026-04-01
- **足球投注量化系统骨架搭建** — ROADMAP.md（4阶段）+ CLAUDE.md（项目配置）+ QUICKSTART.md（开发指南）+ src/骨架 + requirements.txt
  - Phase 1 MVP: Elo+泊松+EV（3-5天），Phase 2: 72因子+XGBoost（5-7天）
  - 存放于 `~/WorkBuddy/football-betting/`
- **中超亚盘数据源纠正** — football-data.co.uk 中超CSV无亚盘字段，弃用欧赔反推方案，改用 OddsHarvester 爬取 OddsPortal 真实亚盘
- **美股持仓日报** — RBLX $56.56(+8.96%)/CRCL $95.41(+6.12%)，大盘年内最佳日，组合浮亏收窄至-$925(-17.88%)
- **Claude Code Agent Teams 指南** — iTerm2 分屏模式配置步骤

### 2026-04-02
- **量化系统 Daemon 3 Bug 修复** — 持仓表缺买入时间、操作日志查看不便、**关键：Dry-Run 每天重复买入**（Futu 空仓→全 BUY，改用 VirtualPortfolio fallback）
- **量化系统 v0.2 Phase 2 因子** — 16 个资金流因子（OBV/MFI/大单/散户反指/VWAP偏离/聪明钱等）+ 12 个港股专属因子（换手率冲击/Spread代理/尾盘漂移/跳空缺口等）
- **因子 AB 回测** — HKFullV2(265因子) vs Alpha158(158因子): Sharpe +122%（1.571 vs 0.708），3 seed 全部 B>A
- **生产模型训练部署** — HK HKFullV2 Ensemble Sharpe 1.056 / US Alpha158MoneyflowV2 Sharpe 2.936，4 个新模型文件部署
- **Score 不变大 Bug 修复** — DataFetcher 类不存在（silent fail）+ end_test 日期硬编码（卡在 3/24），HK 160只全覆盖恢复
- **全面 Code Review 18 问题** — 3 Critical（handler映射/日期硬编码/rolling_train同步）+ 5 Medium + Score 历史追踪功能
- **港股多维度选股扫描** — 5 维度交叉筛选 8 只标的（长飞光纤/吉利/赣锋锂业/比亚迪/康方/京东/零跑/舜宇）
- **港股日报扩展** — 小米(1810.HK)加入跟踪，3列布局，取消企微推送
- **恒安国际(01044.HK)投资分析** — BUY，5-8%仓位分2笔，PE 11.56/股息5.45%/毛利率33.8%
- **腾讯控股(00700.HK)投资分析** — BUY，8-12%仓位分2笔，PE 17.93/混元3.0+AI催化/北水持续增持
- **选股自动化 automation-5** — 港美股每日17:00扫描，多信号交叉筛选
- **football-betting Git 配置** — GitHub 仓库 + QUICKSTART + .gitignore 完善
- **ARKK 日报** — 4/1 报告日，$68.40(+1.20%)，连续第2日零操作

### 2026-04-03
- **Futu OpenAPI 实盘持仓拉取** — 发现完整持仓10+1只，此前仅手动跟踪5只。腾讯1997股(核心仓)，新发现LULU/HOOD/FIG/赛力斯/京东工业/招商证券/哔哩哔哩
  - 存放于 `~/WorkBuddy/stock-analysis/positions_snapshot.json`
- **港股日报扩容** — 3只→5只，新增B站(9626.HK)和招商证券(6099.HK)，增加股息率维度
- **美股持仓日报** — RBLX $60.11(+4.30%)/CRCL $90.26(-0.53%)，组合浮亏-$834.50(-16.13%)
- **港股日报** — Good Friday+清明休市4天，泡泡玛特连跌10日，小米创52周新低
- **港美股每日选股扫描** — 港股8只(吉利4维度领衔)/美股7只(LLY/NKE/CEG等)
- **投注系统 Phase 5 设计** — 从量化基础设施转向"分析师赛前报告"，8大模块+100u本金制
- **ARKK 日报** — Good Friday 休市跳过

### 2026-04-04
- **量化系统 RD-Agent 环境搭建** — macOS 3 处核心 patch（PATH/Docker→Conda/Embedding encoding_format），SiliconFlow DeepSeek-V3 + bge-m3 后端，首次 3 轮自动因子发现（momentum/mean_reversion/volume_momentum 5 因子）
  - 存放于 `~/WorkBuddy/stock_trader/`
- **曼城vs利物浦足总杯赛前分析** — 100u方案 + T-1h 临场更新（ManCity ML 1.95→1.80 EV转负→移除，BTTS No 2.42 EV+27%→升级核心注）
  - 用户实际下注 ¥70：ManCity净胜1球 @4.00 + ManCity赢&小3.5 @3.20(EV+44%🔥)
  - 存放于 `~/WorkBuddy/football-betting/analyses/`
- **马竞vs巴萨赛前分析** — xG合计4.10→大球方向，巴萨48%胜率 vs 市场44%→EV+5.6%
- **美股持仓日报** — RBLX $60.11(+4.30%)/CRCL $90.26(-0.53%)，ZachXBT 指控 Circle $4.2亿+合规漏洞
- **ARKK Week 14 周报** — ARKK +6.08%，OpenAI $24M 首次建仓（历史性），RBLX 进入前10
- **Maple TAPD 催单** — 31 条超期 Story，19 人，送达率 74%→68%（5-6 人持续失败需手动跟进）

### 2026-04-05
- **RD-Agent 结果分析+三重Bug修复** — 13轮IC全部相同（新因子未纳入），根因：read_exp_res.py越界+conf未注入+FilterCol硬编码。首次修复方案错误（移除PortAnaRecord→破坏feedback）→回滚→真正根因off-by-one in backtest/utils.py→IC +66%（0.0147→0.0244）
  - 存放于 `~/WorkBuddy/stock_trader/`
- **RD-Agent 50轮搜索+LLM引导修复** — Loop 15卡住（源码引导LLM生成sklearn因子30-60min/个），根因factor_proposal.py L41→patch-6（prompt约束+看门狗+超时），重跑正常
- **stock_trader Git初始化** — 77文件初始提交，README+.gitignore，远程 stock_trader_qlib.git
- **马竞vs巴萨复盘** — 用户¥50巴萨-0.25 @0.99→巴萨2-1全赢+¥49.50
- **天津vs申花赛前分析（中超首战）** — 首发颠覆预判（铁桶阵→433三前锋），方案全面重写
  - 用户下注¥95（3注），79%押申花赢方向
- **RBLX 周报** — $60.11 周涨+15.80%，RSI接近超买，MA200关键阻力

### 2026-04-06
- **RD-Agent 50轮稳定性工程** — 5次崩溃/5次修复（patch-10~10f），ARG_MAX/MultiIndex/LLM Schema/Embedding Batch/因子中毒五种独立失败模式
  - patch-10: 最小化 env（不继承 os.environ），env 稳定 1,033B ✅
  - patch-10c: MultiIndex 3→2 层校验
  - patch-10d: LLM RuntimeError→SkipLoopError + 5连续失败看门狗
  - patch-10e: embedding 按 batch_size=50 切分
  - patch-10f: 常数因子毒物检测（std<1e-8 或 nan>0.95 → 剔除）
  - 22 轮 checkpoint 保存，SOTA IC=0.0178
  - 存放于 `~/WorkBuddy/stock_trader/`
- **天津vs申花复盘** — 2-3（半场1-1），用户3注中1注，¥95→-¥11.50（ROI -12.1%），累计8场+¥124.20（ROI +28.9%）
  - 教训：双433对攻→小球注直接弃；中超点球溢价+0.3球；阵型对攻度应为大小球首要因子

---

## 工具与经验

### ARKK 自动化
- 数据源：ARK 官网（持仓+交易）、腾讯财经（行情+新闻）
- 输出：daily/ 日报 + weekly/ 周报 + arkk_records.xlsx
- 自动化路径：`~/WorkBuddy/arkk-tracker/.codebuddy/automations/arkk/`

### 报销流程
- 工具链：pdf skill（发票提取）+ xlsx skill（填表）
- 餐标规则：人均 50 元，超出按预算填
- 费用垫付人需用户手动补填

### 踩坑经验
- **插件生态区分**：clawhub/skills 和 openclaw 是不同生态系统，同名包不是同一个东西。安装前必须先看 GitHub README 确认正确的 CLI 工具
- **ARKK 数据延迟**：ARK 官网交易数据有时当天不发布（如 3/17），自动化报告需处理缺失数据，标记 "待补充" 而非报错
- **Memory 架构**：分散在各 workspace 的记忆无法跨会话/跨 workspace 共享 → 必须有全局 MEMORY.md 作为单一信源
- **WorkBuddy 企微能力边界**：机器人角色，不能主动私聊其他人，只能被动响应用户消息
- **博彩数据源可靠性**：中文博彩聚合站（500.com 等）盘口数据严重不准（如 +1.5 实际为 +0.75），football-data.co.uk (Bet365 Asian Handicap) 是英足权威源
- **企微 Webhook 频率限制**：批量发送触发 45009 限频 → 消息间隔 5s + 指数退避重试（5s→10s→20s，最多 3 次）
- **MCP 响应清洗**：TAPD MCP 返回的 text 末尾带 `[TAPD-REQUEST-ID: xxx]`，必须 regex 去掉再 json.loads
- **跨赛事状态不延续**：球员 CL 进球不预示 PL 进球（Szoboszlai 案例），投注时只看同赛事近况
- **小样本历史交锋陷阱**：n<10 的历史交锋不可靠（Fulham vs Burnley "客场3胜/近4场"仅4场8年→实际3-1主胜），n<10 权重应降至 5% 以下
- **逆向思维在极端公众倾向时价值巨大**：93% 押纽卡主胜时反向押桑德兰 → 4/5 命中 +120.7% ROI，关键是要有基本面支撑（双中场核心缺阵）
- **临场信息必须更新方案**：赛前90分钟确认首发后，必须更新投注方案（纽卡-桑德兰：托纳利缺阵确认→方案升级→全赢）
- **延迟数据可能翻转叙事**：ARKK 周报初版显示 $1.6M 操作（静默），3/20 数据延迟到来后变成 $25.0M（雷霆换仓）。自动化报告应标记"初稿"并内建修订检查周期
- **Futu OpenAPI 美股受限**：Futu 港股免费行情好用，但美股权限受限（即使账户开通），需 yfinance 作为 fallback；数据管道设计需多数据源降级链
- **Qlib 版本功能缺失**：Qlib 0.9.7 无 dump_bin 脚本（文档/教程可能引用老版本功能），依赖框架工具前必须 `pip show` 确认版本并实测功能存在性
- **老工程迁移陷阱**：从老 Unity 工程迁移资源时，Spine Examples 和第三方模型包（如 Ark-Models）可能占 1000+ 文件，必须排除；只迁移实际使用的美术资源
- **Futu API 分组操作限制**：不支持创建/删除分组（只能在客户端操作），FX/外汇品种不支持分组操作。批量操作需先 --plan 预览再 --execute
- **Futu 客户端命名规范**：创建分组时会吃掉特殊字符（&等）周围的空格，脚本中必须用实际存储名（如 `AI&云计算` 而非 `AI & 云计算`）
- **westock-data MCP 能力边界**：`technical all` 查询会超时→必须按单指标查询（macd/kdj/rsi 等）；港股 rating 评级不可用，仅盈利预测可查
- **因子剪枝陷阱**：Alpha158 因子间存在协同效应，激进剪枝（>50%因子）会导致 Sharpe 暴降（1.93→1.41，-27%）；保守剪枝仅带来微弱改善（1.77，-8%）。结论：不如保持原始组合
- **glob 模型匹配歧义**：get_latest_model 的 glob 会匹配到 filtered 版本模型文件，必须加 filtered 参数区分原始 vs 过滤后模型
- **因子对比需独立 dataset**：compare 两组因子（158 vs 过滤后）时必须分别构建两套 dataset，共用一个 dataset 会导致列数不匹配
- **博彩赔率横向对比**：同一市场（净胜X球等）相邻选项赔率差<1.0但概率差>5%时，热门选项几乎必定负EV — 庄家系统性压低热门赔率
- **分析报告自我矛盾审计**：输出推荐列表前须检查是否包含自己曾标记为高风险/负EV的选项（意大利案例：HT/FT注与自身复盘经验矛盾）
- **Qlib 表达式语法**：`$` 后不能跟 `{}`（如 `${pe_ttm}` 或 `$(pe_ttm)` 都报 SyntaxError），必须直接写 `$pe_ttm`
- **yfinance 港股基本面数据**：大量缺失，仅有 `ticker.info` 快照值（非历史序列），作为因子引入反而增加噪声降低 Sharpe
- **因子效果是市场特定的**：同一因子集美股 Sharpe +2.5%、港股 -7.6%，数据质量决定因子价值，不能跨市场统一部署
- **不同联赛数据格式差异**：中超CSV无亚盘/大小球字段，需从欧赔反推隐含盘口；跨联赛统计分析需考虑数据来源差异
- **TopkDropoutStrategy 操作排名非分数**：Qlib 的 TopkDropoutStrategy 看的是排名（rank），不是原始预测分数——高排名=好，与分数符号无关
- **DatasetH vs TSDatasetH**：LightGBM/CatBoost 用 DatasetH，TSDatasetH 仅适用于时序模型（LSTM等）；混用会报错
- **Qlib instruments 参数简写**：传 `"us"` 或 `"hk"` 简称，不能传完整路径如 `"data/qlib/instruments/us.txt"`
- **CatBoost 默认参数不可信赖用于集成**：CatBoost 默认参数 Sharpe=1.59 远低于调优后 2.00；默认参数集成反而比单模型差(-17.5%)，必须先 Optuna 优化再集成
- **风控参数初始值过激陷阱**：动态风控初始参数触发率 97%（本质上始终激活=无alpha），校准后保守参数才达到理想效果（熊市82%/牛市0%）
- **ARKK 数据源时效性**：cathiesark.com 数据更新可能延迟数天，arktradetiming.com 和 arkfunds.io 是更可靠的实时交易数据源
- **高维 DataFrame dropna 陷阱**：161列 DataFrame 用 dropna().corr() 几乎删光所有行（任一列NaN就删行），必须用 pairwise `corr(min_periods=30)` 替代
- **FutuOpenD 进程≠可用**：进程 PID 存在+端口监听 ≠ API 可用，GUI 需要登录后 API 才真正开放。自动化脚本应做三层健康检查（进程→端口→API调用）
- **滚动训练安全门槛**：自动部署新模型前必须有 Sharpe 门槛检查——美股集成 Sharpe 0.786<1.5 时正确保留旧模型，防止劣化部署
- **技术调研需二次深挖**：首次调研 RD-Agent 判定"5个macOS致命坑"→二次深挖发现 Conda 模式完全绕过 Docker + 社区 PR #1261 已修复 M4 兼容。初始"不可用"结论是错的
- **跨系统 ID 格式必须归一化**：Qlib 用 `usaapl` 格式，Futu 用 `US.AAPL`——直接比较永远不等，导致所有持仓股被误判为 BUY 信号+卖出候选永远匹配不到。边界处统一格式
- **跨午夜交易时段判断**：美股 21:35~04:05 北京时间跨午夜，周五过零点 weekday()=5(周六)→所有盘中检查被跳过。需专门的 is_trading_session() 函数，hour<6 时检查前一天
- **Qlib bin 数据字段因市场而异**：港股无 $vwap 字段，11 个 WQ101 因子静默返回空 DataFrame。因子库必须声明依赖字段并提供 fallback（Typical Price 替代 VWAP）
- **Qlib handler.fetch() 列结构**：返回扁平 columns 而非 feature/label 分组；label 列名是原始表达式而非 'LABEL0'。必须用 col_set='feature'/'label' 分开取
- **venv 路径必须写死**：用户终端未激活 venv 时 `python` 指向系统 Python（无项目依赖），所有文档/Dashboard/CLI 命令应使用 `.venv/bin/python` 绝对路径
- **手动执行需交易时段守卫**：auto_trade.py 只有交易日检查没有交易时段检查，18:31 盘后仍执行生成无效订单。每个执行入口都要同时检查 day + hours
- **Dashboard 数据溯源三坑**：(1) 排名列从CSV导入的是分层内排名，不是显示排名→重新编号；(2) 总资产取自占位值1M→改为实时持仓计算；(3) YAML压缩格式行数≠标的数→regex拆分计数。教训：Dashboard每个指标都要追溯到数据源验证语义正确性
- **Streamlit 红涨绿跌覆盖**：st.metric 硬编码绿正红负，无原生配置项→两层修复：关键指标改 custom HTML、全局注入 MutationObserver JS 持续翻转 delta 颜色。中国市场Dashboard必须第一天就做
- **Daemon 重启漏跑任务**：daemon 21:28 启动但 daily_scores 21:20 已过期（misfire_grace_time=300s<480s延迟）→任务静默跳过。关键调度应设更大 grace_time 或加 startup catch-up 逻辑
- **Polymarket 恐慌溢价**：淘汰赛场景 Polymarket 概率比博彩隐含高 6-11%（波黑vs意大利：81% vs 70-75%），不是信息优势而是情绪溢价，不可直接用于EV计算
- **中超CSV无亚盘字段**：football-data.co.uk 的中超CSV只有欧赔，不含 AHh 等亚盘字段。不要从欧赔反推（不准），用 OddsHarvester 爬 OddsPortal 获取真实亚盘数据
- **LLM Agent 项目骨架先行**：Claude Code 等 LLM 编码 Agent 开始前，先准备 CLAUDE.md + QUICKSTART.md + 目录骨架 + requirements.txt，投入1小时可节省10倍返工时间
- **Dry-Run 幽灵状态陷阱**：dry-run 模式从 Broker API 读持仓（永远为空）→每天所有股票被判为 BUY 而非 HOLD。修复：dry-run 必须有本地状态 fallback（VirtualPortfolio），且跨周期持久化
- **静默类引用失败**：daemon 中 try/except 包裹的任务引用不存在的 DataFetcher 类→静默跳过→数据停滞 6 天。Stale data 比 missing data 更危险（输出看起来正常但是旧的）。daemon 启动时验证所有 import
- **Qlib 表达式不支持一元负号**：`-$volume` 报 `bad operand type for unary -` → 必须写 `(0 - $volume)`。QlibDataLoader config 是 `(fields_list, names_list)` 二元 tuple，不是 list of tuples
- **AKShare 南向资金爬取太慢**：akshare `stock_hsgt_hist_em()` 单次调用需 6 分钟+，不适合 daemon 定时任务。改用纯 OHLCV 表达式因子（OBV/MFI/大单代理）绕过
- **实盘持仓必须 API 验证**：手动记忆的持仓覆盖不到50%（5只→实际11只），Futu API 是唯一可信源。API均价含佣金摊入，与手动记录有微小差异属正常
- **日报扩容多层同步**：报告从N只扩至N+M只时，automation prompt/HTML模板/对比维度/数据查询四层必须全部更新，漏一层则输出残缺
- **节假日日历多市场差异**：同一假期（复活节）HK休4天、US休1天；自动化需按市场独立维护假日日历，skip时记录原因+复牌日期
- **RD-Agent macOS 三处必改**：(1) env.py 加 `/opt/homebrew/bin` 到 PATH；(2) generate_data_folder 用 `conda run` 替代 QTDockerEnv；(3) SiliconFlow Embedding 必须传 `encoding_format="float"` 不接受 None
- **RD-Agent conf_baseline.yaml 默认值全错**：默认 csi300 + SH000300 benchmark + 2008~2020 时间段，港美股用户必须全部覆盖。benchmark=null 在 Qlib 也报错，需用 placeholder 标的
- **Qlib bin 数据时间范围陷阱**：上次 fetch_and_convert 若 start 设近期日期（如 3/25），bin 数据只有几天，RD-Agent 因子发现需要 2020+ 完整历史才有意义，必须全量重拉
- **投注赔率 T-1h 必须刷新**：ManCity ML 赔率 6h 内从 1.95→1.80（EV 从正变负），BTTS No 2.42 成为全场最佳 EV+27%。永远不要在开赛前 2h+ 锁定投注方案
- **催单送达失败是人级别的不是随机的**：TAPD催单同一批人连续两轮都失败（5→6人），重试无效，需要手动跟进或备用渠道
- **首次修复方案可能是错的**：RD-Agent Qlib修复时，第一次直觉性修复（移除PortAnaRecord）解决了IndexError但破坏了feedback读取。真正根因在完全不同的模块（backtest/utils.py off-by-one）。修复第三方代码前必须保存pristine状态，验证ALL downstream后再确认
- **LLM Agent框架源码藏有隐式prompt**：RD-Agent factor_proposal.py L41在15轮后引导LLM "try machine learning-based factors"→生成sklearn因子卡死流程。使用任何LLM Agent前必须审查嵌入式prompt模板
- **自主循环必须有外部看门狗**：RD-Agent 50轮搜索在Loop 15被单个sklearn因子（30-60min）冻结。框架内置timeout可能不生效，外部watchdog脚本（独立进程定期kill）是唯一可靠安全网
- **首发阵容可颠覆全部赛前分析**：天津vs申花预判铁桶阵防守→实际4-3-3四外援进攻。阵型变化不是"权重调整"而是"范式转换"，需要全面重写方案而非微调
- **os.environ 继承在循环中导致 ARG_MAX 崩溃**：RD-Agent subprocess 每轮继承全 env，PATH 被重复 prepend（+1.7KB/轮），Loop 13-14 超过 macOS 1MB 限制。修复：只传 ~12 个必要变量，不继承 os.environ
- **LLM 输出 schema 违规是必然事件**：50 轮 Agent 循环中 DeepSeek-V3 在 Loop 22 返回 int 字段为 dict。RuntimeError 不在 skip 列表→进程崩溃。所有 LLM 调用必须 try-catch + 转为 skip event
- **embedding API batch 限制与数据增长冲突**：SiliconFlow ≤64 batch，因子库从 <64 增长到 65+ 后 413 错误。迭代系统中任何 API 调用都应从 day one 做分批
- **ML 因子库常数毒物检测**：SOTA 中混入 std=NaN 的常数因子→LightGBM IC 从 0.018 退化到 0。concat 前必须检查 std>1e-8 和 nan_ratio<0.95
- **中超点球溢价+0.3球**：中超VAR+点球率高，大小球预期需上调0.3球。双方433对攻时小球注应直接放弃
- **watchdog 超时必须校准**：RD-Agent 3×10 搜索中 watchdog TIMEOUT=180s 太短（Qlib backtest 5-10min/步），误杀健康进程导致 3 batch 全失败。规则：timeout = 3× 最大步骤时长，ML管道最少 10min
- **批量脚本 CLI 参数映射必须验证**：batch_search.sh 用了 evolving_n 以为是循环控制，实际是 --loop-n 控制。结果：10轮变29轮无限跑。Wrapper 脚本必须读框架 argparse 源码确认参数名
- **macOS grep 不支持 -oP**：macOS BSD grep 无 Perl regex 支持，-oP 静默失败返回空。永远用 -oE（ERE），或 `brew install grep` 后用 ggrep
- **数据管道脚本可静默覆盖历史数据**：market_switch.sh 调用 dump_to_qlib_bin 会用当前 CSV 全量覆盖 bin 文件。CSV 只有 7 天时，bin 从多年→7天，RD-Agent IC 全 NaN。必须先备份+验证 CSV 行数再 dump
- **Symlink 隐藏数据依赖**：~/.qlib/qlib_data/cn_data 是 symlink 到项目 bin 目录，market_switch 破坏 bin = 同时破坏 RD-Agent 训练数据。ML 管道需要数据隔离，symlink 是反模式
- **Dry-run 计算函数内部 re-fetch 返回空**：calculate_rebalance() 内部调 get_positions() 在 dry-run 下永远空→SELL 信号全被跳过。所有读取 broker 状态的函数必须接受 positions_override 注入
- **fetch_all_watchlist 的 --force 必要性**：check_existing 只检查文件是否存在，不检查行数。已损坏的 3 行 CSV "存在"→被跳过。--force 是重建损坏数据的唯一方式

### 2026-04-07
- **RD-Agent 3×10 港股因子搜索** — 首轮全失败（watchdog误杀+CLI参数错误），修正后17:20重启
  - 修正 batch_search.sh --loop-n / watchdog TIMEOUT 180→1800
  - 踩坑：macOS grep -oP 不可用
- **港股日报** — 休市（4/3-4/7 Easter+清明），4/2 数据展示
  - 五股跟踪（泡泡玛特/腾讯/小米/B站/招商证券），小米创52周新低

### 2026-04-08
- **Dry-run "只买不卖" Bug 修复** — calculate_rebalance 内部 re-fetch positions 在 dry-run 下返回空→SELL 全被跳过
  - 修复：positions_override 参数 + vp.update_prices() + vp 作用域修复
  - 存放于 `~/WorkBuddy/stock_trader/`
- **数据架构踩坑：market_switch 覆盖 bin** — 脚本用 7 天 CSV 覆盖了多年 bin 数据，导致 RD-Agent IC 全 NaN、因子 42% NaN
  - 根因：CSV 被截断(只有3-7天) + market_switch 无验证无备份直接覆盖
  - 修复流程：备份(CSV 308 files/BIN 39M) → fetch --force → 重建 bin → 验证
  - 关键发现：~/.qlib/qlib_data/cn_data 是 symlink 到项目 bin，零隔离
  - 存放于 `~/WorkBuddy/stock_trader/`
- **港股日报** — 大涨日（恒指+3.09%/恒科+5.22%），B站MACD金叉确认，招证金叉延续
- **美股持仓日报** — RBLX $57.50(+0.52%)菲律宾禁令解除 / CRCL $94.12(+2.14%)
- **每日选股扫描** — 美团(4维)+阿里(4维)+CRCL(3维)+LULU(3维) 领衔
- **巴萨vs马竞欧冠分析** — 第9场分析（第6场同对阵），策略收敛模板确立
- **ARKK 日报** — $68.76(-0.06%)，cathiesark 数据延迟，ARK 4/6 买入 TSLA ~$1066万

### 2026-04-09
- **每日选股扫描** — westock-tool 全天 MCP 限频100%失败，切换 finance-data API（limit_list_ths+top_list+broker_recommend），A股涨停/龙虎榜/券商金股维度更丰富
  - 港股持仓：腾讯508.5(+0.1%)、B站186.5(-1.27%)、招证13.29(-2.78%)
  - 美股持仓：RBLX $55.43(-3.6%)、CRCL $94.44(+0.34%)、LULU $158.86(+3.38%)
  - A股新发现：光迅科技（CPO龙头）首板+机构2.46亿、巨人网络（4月券商金股S级）
- **Daemon 排查** — 旧 PID 32802 运行158h后 step_trade 卡12h（BlockingScheduler 独占），kill 后新 PID 2108 正常
- **欧冠复盘** — 巴萨0-2马竞（5注0中-¥95）+ PSG 2-0利物浦（5注4中+¥125），合计+¥30（ROI +15.8%）
  - 教训：UCL淘汰赛谨慎效应系统性存在，深让盘需反向对冲；互补投注策略验证成功
- **新因子提案** — 亚盘连红/连黑/走水反转因子（均值回归子因子，待开发）

#### 4/9 新踩坑经验
- **MCP 工具限频不可控**：westock-tool 全天100%限频无任何预警。关键流程必须有 primary-backup 降级链且备选方案预先验证
- **Daemon 活死人状态**：PID存活≠任务执行。健康检查必须包含'最近成功执行时间'，watchdog 检测 staleness 而非 aliveness
- **UCL 淘汰赛谨慎效应**：深让盘(>=1球)在淘汰赛系统性高风险，红牌等极端事件对让球方破坏性极大。双场日用互补策略做默认风控
- **用户直觉是因子假设源**：亚盘连红/连黑反转假设来自用户领域经验，比纯数据挖掘更有方向性

### 2026-04-10
- **FMPFetcher 双 Bug 修复** — (1) `code.replace('.','').lower()` 产生 `usaaapl`（多a），改用 `futu_code_to_qlib()`；(2) CSV fallback 在 try 块内被 except 吞掉，提到外部
  - AAPL 验证：503交易日，12/15因子有效率>50%
  - 存放于 `~/WorkBuddy/stock_trader/`
- **港股日报** — 恒指+0.55%，招商证券+3.84%⭐领跑（放量MACD金叉），腾讯/B站MACD金叉
- **小米首次建仓** — 200股@HK$31.2（用户自主操作），4/10收盘30.90，浮亏-0.96%
- **ARKK 日报** — $68.92(-2.05%)，ARK 买入 WGS ~$45万/卖出 ROKU ~$160万
  - 踩坑：financecharts 限流 + Yahoo 429 + ARK XLS 损坏，三源同日失效，eastmoney+腾讯API兜底
- **申花vs海港上海德比赛前分析** — 第12场分析，BTTS 100%(近5德比)，申花让0.25→0.5升盘，5注方案
  - 教训应用：天津复盘经验（拉唐状态/谢鹏飞替补/中超点球溢价+0.3球）

#### 4/10 新踩坑经验
- **格式转换链是隐形Bug工厂**：`code.replace('.','').lower()` 对 `US.AAPL` 产生 `usaaapl`（多一个a）。每个 .replace()/.lower() 都是潜在腐败点，必须用已知输入→已知输出断言测试
- **Fallback 路径不能在 try 块内**：yfinance 异常后 except 直接 return None，fallback 永远不执行。Fallback 必须在 try/except 块外部
- **同质数据源连锁失效**：financecharts+Yahoo+ARK XLS 三个美国源同日连锁失效（共享反爬生态）。金融数据需4+源覆盖，至少2源来自不同生态系统（中美混合）
- **新建仓需全链路更新**：小米从 watch→hold，持仓快照/日报模板/自动化/风控/MEMORY 五层都需更新，漏一层产生数据不一致

### 2026-04-11
- **RD-Agent 美股数据修复** — yfinance 429→97% NaN，切换 Twelve Data API 重拉 140 只美股完整历史（2016-2026）
- **🚨 LOOK-AHEAD BIAS 发现** — `shift(-5)` 泄漏未来数据，IC 从 0.001 飙到 0.39（年化1101%），Batch 3 Loop 2-6 全部无效
  - patch-11: MLflow file_store 空 metric 文件容错
  - patch-12: prompts.yaml 强制因子代码数据清洗
  - 需要 patch-13: 禁止 shift(-N) N<0
- **港股因子提取 v4 重做** — 修复因子名配对串扰 + ANSI 转义，102 个有效因子
- **美股 Batch 2 新窗口 3 轮验证** — patch-11/12 生效，NaN=0，IC 稳定
- **申花vs海港临场更新** — 让-克劳德回归4外援全出→方案调整（直胜降→不败升），用户¥100（3注全含申花方向）
- **利物浦vs富勒姆赛前分析** — 大球+BTTS+利物浦主胜方向
- **用户三串一** — ¥10 综合赔率5.92（小3球+布莱顿客胜+富勒姆+0.75），第三腿逆向AI
- **ARKK Week 15 周报** — $69.29 周涨+1.06%，AI叙事芯片→垂直应用（AMD清仓→PLTR/HOOD）
- **Maple 催单** — 37 条超期 21 人，送达率 71%（6人失败需手动跟进）

### 2026-04-12
- **投注系统四大模型升级方案** — BTTS重构(P0)/xG波动(P0)/亚盘反转因子(P1)/射手策略(P2)，预计10h
- **单场预测 CLI + 模型持久化** — predict_single.py + refresh_data.py + 三段式模板(模型/脑算/融合)，E0/SP1/I1 预训练模型
- **🐛 校准器 Bug 修复** — Isotonic Regression 阶梯压缩→混合校准(50/50)，回测 17 场 ROI+42.5%
- **三场英超 V1→V2 重建** — V1 合并文件被退回，V2 独立文件+9模块+6补充维度+盘口追踪+伤停修正
  - 水晶宫 2-1 纽卡（80+90+4点球逆转）: BTTS No ❌ / 桑德兰 1-0 热刺（H2H 21场不胜终结）: 主胜 ✅
- **sentiment-news-analyzer + trading-decision-integrator Skill 构建** — 双 Skill + RBLX E2E 测试(3.5/10偏空) + 5 个自动化任务全部集成
- **美股 RD-Agent Batch 3 重跑确认** — patch-13 生效，IC 正常(0.000~0.008)，look-ahead=0
- **美股 Batch 4-5 完成(30轮总计)** — best IC=0.0135，13 个因子，NaN=0，LLM 失败=0
- **Task 3.4 因子评估** — 发现 mixed-market 数据(302只=162HK+140US)，确认 IC 有效(instruments filter)，修复 market_switch.sh
- **Batch 6 启动** — 修复后首次运行，纯美股 144只×17列 ✅
- **每日选股扫描完整版** — A股/港股/美股全覆盖，Top5: 天能动力/FCX/孚日/科达/AMZN

#### 4/12 新踩坑经验
- **LLM 因子 look-ahead bias 是系统性威胁**：LLM 不理解因果时序，自然会生成 `shift(-N)` 泄漏未来数据的因子。IC 异常跳涨(>5x)必须触发自动审查，年化>200%几乎必然是数据泄露
- **毒因子进入 SOTA 后污染全链**：一旦含 look-ahead bias 的因子成为 SOTA，后续所有迭代都在被污染基线上进化，结果全部无效。SOTA 更新前必须保存 clean checkpoint
- **回测短窗口(<12月)+极端指标(IR>10)≈不可靠**：9个月窗口 IC=0.41/IR=15 是幻觉。最低12月测试窗口，IR>5自动怀疑
- **日志解析脚本天然脆弱**：因子名-代码位置配对+ANSI转义干扰→v4重写。应优先要求ML管道输出结构化JSON
- **Isotonic Regression 小样本阶梯压缩**：309场训练集下 Isotonic 校准器将不同比赛映射到相同概率值（如 H=48.1%/D=29.0%/A=26.0%），看起来合理但实际是量化噪声。<1000 样本用混合校准（50%原始+50%Isotonic）
- **首版分析合并多场=必被退回**：将 3 场比赛合并到一个文件 + 省略维度 → 用户全部退回重做。每场独立文件 + 9 模块完整模板是底线标准，V1 返工 = 2x 总成本
- **ML 管道 "skip if exists" 对可变数据危险**：RD-Agent 检查 data_folder 存在就跳过复制，导致混合市场数据（162HK+140US）污染工作目录。可变数据必须 overwrite+validate，不能 skip
- **补时进球摧毁小球注单**：水晶宫 80 分钟 0-1 → 90+4 点球 → 2-1，BTTS No/U2.5 在 79 分钟时全赢 → 最终全灭。小球注需 Kelly 减码 15-20% + 正确比分微对冲
- **市场 switch 必须原子化更新所有数据副本**：market_switch.sh 只更新 template h5 未更新 working copy，导致因子在混合宇宙上计算截面排名。switch 脚本须更新 ALL 副本 + 断言 instrument count
- **连续零进球不等于不会进球**：利兹4场0球但对手防线都是中上水平；面对曼联赛季最弱后防（马奎尔停赛+德利赫特伤缺），线性外推"继续0球"是错误的。必须对比当前对手 vs 连续期对手的防守质量
- **伤停评估必须双向**：分析只看一方伤停（利兹缺谁）而忽略对方伤停（曼联后防双缺）→遗漏BTTS机会。每场分析必须有双列伤停影响矩阵
- **用户v2修正是最高价值学习信号**：曼联vs利兹v2修正：一致性评分71%→86%，揭示3个系统性盲点（线性外推/单向伤停/遗漏角球市场）。用户修正命中率>90%，每次修正应抽象为通用规则
- **数据质量投资有指数级回报**：RD-Agent Batch 6 修复后（纯144美股×17列含基本面）产出27因子，是Batch 4-5合计(13)的3倍。同框架同LLM，唯一区别是数据质量

### 2026-04-13
- **3场英超复盘(4/12赛果)** — 水晶宫2-1纽卡(AI -¥9/用户-¥50) + 桑德兰1-0热刺(AI +¥4.31/用户+¥46.25) + 切尔西0-3曼城(AI +¥2.04/用户+¥24.50)
  - 累计18场：~¥855投入，+¥156.95（ROI ~18.4%），用户持续跑赢AI
- **曼联vs利兹赛前分析** — 主胜64.2%，庄家精确定价(主胜1.55 EV~0%)。V1被用户修正：增BTTS Yes核心注(¥10)+角球市场(¥13)，删2-0比分(与BTTS矛盾)。一致性71%→86%
  - 用户实际下注¥75：BTTS+Mbeumo @2.44 / 曼联赢&BTTS @3.00(+14%EV) / O9.5角球 @1.85(+7%EV)
- **RD-Agent Batch 6 完成** — 3h完成10轮，best IC=0.0098(Loop 8)，SOTA突破4次。27个因子：估值(4)+质量(4)+动量(6)+量价(7)+复合(6)
- **westock-partner 三任务集成完成** — A:港股日报简评 + B:每日选股快评 + C:港股圆桌周报(新建)。小米圆桌分析(4位专家)
- **港股持仓日报** — 恒指-0.90%，组合总浮盈+151.3%，腾讯-2.87%拖累，B站+1.36%唯一收红
- **每日选股扫描** — 精选7只：华工科技BUY(78)/荣昌生物BUY(75)/东山精密WATCH/中际旭创WATCH/招商证券WATCH→BUY(68)/中国移动WATCH/LULU WATCH
- **GitHub Trending W16** — Agent框架军备竞赛，端侧AI推理首入榜，金融AI升级基础模型层

### 2026-04-14
- **RD-Agent 因子集成到生产管道** — rdagent_bridge.py 执行51脚本(48成功)→USRDAgentV1(301因子=253Qlib+48RD-Agent)，AB回测 **Sharpe +80%**(1.49→2.68)🔥，年化+107%(23.1%→47.9%)
  - 3个集成Bug修复：NestedDataLoader缺module_path、MultiIndex未排序、object列crash
  - ⚠️ 3 seed σ=0，需要数据扰动验证鲁棒性
- **投注模型全系统诊断+7优化方向** — P0:多赛季合并(309→1069场)、P1:Dixon-Coles、P2:v2特征激活(16→35因子)、P3-P4:校准/Elo。5 Phase Roadmap 19h
- **角球模型+xG/PPDA评估** — 3200场角球数据可建独立泊松模型，PPDA已爬未接入是角球预测的关键上游
- **欧冠数据新增** — CL 2324(125场)+CL 2425(189场)+合并494场，场均3.34球>联赛2.7
- **曼联1-2利兹复盘** — AI 6注3中-¥5.85，v2修正版限亏¥37+（v1估-¥43→实际-¥5.85）。角球O9.5第2次验证命中(15角球)。累计19场ROI~+13.8%
- **方法论 v3→v4 升级** — 分析模板新增角球专项分析+纯模型方案假设结算
- **马竞vs巴萨欧冠QF次回合分析** — 排除Sky247(比分错误)，模型马竞44% vs 市场25.6%→EV+45%🔥
- **B站vs小米换仓圆桌** — 4:2建议不急卖B站(盈利拐点+MACD金叉)，小米用增量资金分批接
- **每日选股扫描** — 神火(Q1+217.7%/PE 9.2)/沪电(涨停)/中际旭创/润泽/新易盛
- **加班餐报销 4/11** — 3张发票（服务器+客户端+美术），合计¥1964

#### 4/14 新踩坑经验
- **NestedDataLoader 需显式 module_path**：QlibDataLoader 在 NestedDataLoader 内部初始化时，缺少 module_path 参数会静默失败。集成第三方 Loader 必须传完整参数
- **Parquet MultiIndex 必须 sort_index()**：未排序的 MultiIndex 在 Qlib 的 loc/xs 操作中触发 UnsortedIndexError。写入 parquet 前 sort_index() 应该是标准流程
- **因子列 object 类型会炸 normalizer**：RD-Agent 生成的因子可能包含 None 值导致列类型为 object。RobustZScoreNorm 的 np.nanmedian 不接受 object → 必须在桥接层强制 float64
- **σ=0 across seeds ≠ 鲁棒性验证**：LGB/CatBoost 确定性训练+相同数据→3 seed 完全一致是预期行为，不是鲁棒性证据。真正的验证需要数据扰动（bootstrap/时间窗口偏移）
- **训练数据闲置是最大浪费**：投注模型用309场训练但3赛季1069场可用，35个可算特征只激活16个。先最大化已有资源利用，再考虑模型升级
- **数据源比分错误→全局黑名单**：Sky247 欧冠首回合比分写错→排除。错误范围不可知的源不能部分信任
- **赔率禁止估算/记忆**：BTTS Yes 脑记 1.55 但实际 1.34-1.40，EV 从正翻负。The Odds API 已接入，所有分析必须 `--auto-odds` 拉实时赔率，严禁估计
- **UCL淘汰赛必须事实预检**：V1分析3个致命事实错误（比分错、球员已转会、结果标TBC），根因是知识陈旧。欧冠分析必须先 web search 验证首回合比分+当前阵容+伤停
- **极端控球差异压制角球-3~-4**：马竞29%控球→6角球 vs 模型预测10.5。控球<35%时角球修正系数从-2~3上调到-3~4
- **复盘不得自吹未下注的预测**：声称"比分1-2精确命中🔥"但实际无比分注、标注"未记录投注"但用户曾给过数据→被用户抓住2个审计错误→方法论v5强制四方对比+禁止废话
- **Dixon-Coles rho 因联赛而异**：EPL ρ=-0.1741(强修正)、La Liga ρ=-0.0392(弱)、Serie A ρ=+0.0345(异常正值)。不可跨联赛使用统一rho
- **数据源URL会变需动态发现**：football-data.co.uk 封锁了 /new-data/ 和 /data/ 路径，正确为 /mmz4281/2526/{CODE}.csv。自动化脚本禁止硬编码URL
- **Stake.com IP封锁**：HK/CN IP 被 Stake.com 全面封锁（403 ip-blocked），含所有镜像。The Odds API 免费500次/月是可用替代

### 2026-04-15
- **Dixon-Coles修正+角球泊松模型** — Phase 2完成，EPL rho=-0.1741，角球模型支持德比/保级/PPDA修正
- **The Odds API 接入** — 67联赛+40博彩公司+实时赔率+Pinnacle提取，predict_single.py 对接 --auto-odds
- **赔率漂移因子 features_v2** — 7个新因子（1X2漂移+大球漂移+亚盘水位漂移+资金方向+Pinnacle margin），319/319非空
- **赔率快照对比系统** — --snapshot --tag + --snapshot-diff，追踪盘口变化
- **UCL QF2赛前分析v1→v2** — V1三致命事实错误被用户抓住，V2全部重写
- **马竞1-2巴萨复盘+方法论v5** — 角球O9.5惨败(6vs10.5)→控球修正参数+审计规范+四方对比
- **盘口数据更新** — football-data.co.uk URL重新发现，7球队数据更新至4/13
- **每日选股扫描** — 11只精选，A股Q1业绩催化（金海通+221%/东山+152%），NVDA 10连涨

### 2026-04-16
- **欧冠QF2双场复盘** — 阿森纳0-0葡体(AI -¥3/xG 0.93=赛季最低/角球O10.5精确命中11) + 拜仁4-3皇马(7球+2红牌史诗级)。用户二串一¥20→-¥20。累计22场+¥89.33(ROI +8.8%)
- **港股持仓日报** — 恒指+1.72%恒科+3.67%，五股全涨(小米+3.75%/腾讯+3.61%/B站+2.84%)，新增「搭子说两句」高手简评气泡+情绪评分条
- **美股持仓日报** — RBLX $59.79(+2.56%) MACD金叉，CRCL $105.52(+0.03%)利空出尽。⚠️ RBLX Q1财报日期确认为4/30(非此前记忆的5/7)
- **ARKK 日报** — $71.47(+3.53%)，无交易，cathiesark确认
- **每日选股扫描** — 11只精选，宁德BUY(80)/中际BUY(78)/AVGO(78)/比亚迪H(76)，创业板+3.17%创11年新高

#### 4/16 新踩坑经验
- **"被迫前压"≠有效进攻**：阿森纳总分领先→葡体被迫进攻→xG仅0.93(赛季最低)。aggregate trail导致的进攻是绝望式的，应打7折估算xG
- **非英超弱队UCL λ打5折**：Liga Portugal球队国内xG ~1.8 但UCL淘汰赛实际~0.5(折扣72%)。非TOP5联赛球队进UCL淘汰赛必须大幅折扣进球率
- **串关跨场一腿死全死**：角球O10.5✅(11角球精确命中)+O2.5❌(0球)=¥20全灭。跨场串关要求每腿>75%概率+低相关性，否则用单关+Kelly
- **催化日期必须API验证**：RBLX Q1财报日期记忆中5/7→实际4/30，差7天。期权/仓位时机可能因此错判。所有催化日期必须IR页面/API live验证
- **利空出尽信号识别**：CRCL从CLARITY Act暴跌-20%→Bernstein深度解读(针对分发商非发行人)→利好Circle→$105回稳。监管恐慌标题≠实际影响，要读法案原文

### 2026-04-17
- **🔥足球投注系统Phase 5全线突破** — xG/PPDA/xPTS数据管线修复(0%→97%)、全数据源接通(44→63→73因子)、XGBoost回测接入(Draw+63%)、Phase 5.1-5.5完成(英超-1.3%→+10.1%🔥🔥🔥)
  - 角球O10.5 ROI+25%独立alpha源确认
  - XGBoost按市场选择性激活：Under/Draw/Over用XGB，1X2用纯泊松
  - 新增球员xA(521人→20队)/红牌率/裁判偏向/半场进球率
- **中超全量数据系统搭建** — api-football(18统计/场)+CHN.csv(2848场)+45队Elo模型，免费版仅覆盖2022-2024
- **山东vs海港赛前分析** — 海港10+人伤缺(λ_away 1.83→1.08)，用户¥50(主胜@1.99+串关@2.97)
- **ARKK日报** — $77.34(-0.58%)，XLS CompDocError+Yahoo限流→eastmoney/tencent兜底
- **美股持仓日报** — RBLX $60.44(+1.09%)/CRCL $107.46(+1.84%)，组合浮亏-$649(-17.94%)
- **每日选股扫描** — 10只精选，中际旭创Q1+262%大超预期/荣昌生物获艾伯维6.5亿首付/源杰超茅台A股新股王

#### 4/17 新踩坑经验
- **特征代码存在≠特征数据接通**：features_v2有44因子的计算代码，但xG/PPDA/xPTS填充率0%，因为build_features_v2_from_csv()没加载Understat JSON。代码不报错+ML静默忽略NaN列=整个管线看起来正常实际40%因子无贡献。每次pipeline变更必须assert填充率
- **ML模型价值是市场特定的**：XGBoost改善Draw(+14pp)+Under(+4pp)但恶化HomeWin(-8pp)。全局部署ML→整体ROI降；按市场开关ML→英超从-1.3%到+10.1%。架构不是"最好的模型"而是"每个决策面最好的模型"
- **API免费版时间盲区**：api-football免费版覆盖中超2022-2024但不含2025+当前赛季。用历史数据开心搭完管线发现无法live使用。接入API前先检查时间覆盖范围
- **ARK XLS格式不稳定**：官方XLS下载成功但xlrd解析CompDocError。加上Yahoo限流+cathiesark延迟=三源同失。金融文件需多解析器fallback链(xlrd→openpyxl→pandas→web)

### 2026-04-18
- **英超4场赛前分析+双Bug修复** — 利兹/纽卡/热刺/切尔西四场v5分析。发现predict_single.py未激活XGB（main()不调用已写好的load函数），修复后+--xgb CLI。handicap_prob符号翻转Bug存活20+场分析首次被用户发现（+0.5罕见场景暴露），新增对称性不变量测试
  - XGB重跑：Draw +30pp、O2.5 +7~17pp
  - Isotonic Draw系统性偏高+32pp，与XGB双重叠加→Draw@4.23 EV+144%（虚假）
  - 用户下注¥150（5注），热刺O2.75@1.78 EV+16.2%为最佳注
- **量化系统Task 3.6港股基本面补齐** — AKShare替换Futu，ROE_AVG累计值Bug被pre-flight体检抓到→切ROE_YEARLY+手工年化ROA。151/161股成功，NaN 36-55%→7.6-24%
  - health_check_hk.py 新增7维度数据完整性体检
  - market_switch.sh v2重构：档案模式cp覆盖，秒级切换
- **🚨 Sharpe=2.68是数据artifact** — 修复bin后AB彻底反转：Alpha158MF 1.49→1.96(+31.7%)，USRDAgentV1 2.68→1.46(-45.4%)。根因：us.txt从139→144(加了usqqq benchmark)。恢复旧pool后RDA仍+9%正贡献
  - 港股RDA 4批40轮116因子=持续负贡献(-35.7%)，停止港股RDA投入
  - 美股保留USRDAgentV1(+5-10%)，港股用纯HKFullV2(Sharpe=1.74)
  - 美股基本面bin全NaN→重跑bin+h5+parquet修复，6/48退化因子恢复5个
- **ARKK日报** — 周六休市跳过

#### 4/18 新踩坑经验
- **代码存在≠运行时激活（双重验证日）**：predict_single.py的XGB函数写好了但main()没调用+handicap_prob存在20场但有sign bug。同一天两个独立实例证明：集成后必须跑e2e诊断确认所有模块"activated=True"
- **概率函数必须有数学不变量测试**：handicap_prob的point test（已知答案对）巧合通过了bug代码。加上cover_home+cover_away=1.0的对称性测试后立即抓到。一个不变量测试>十个点测试
- **Sharpe对标的池超级敏感**：us.txt加5只ETF(含benchmark)+延长17天test期→基线Sharpe +32%。AB结论从"+80%"翻转为"-25%"。恢复旧pool后真实值"+9%"。AB必须锁定pool fingerprint
- **RDA因子0%NaN≠有信息**：PE_Rank等6个因子fillna(0.5)→NaN=0%看起来健康但95%值=0.5常数。模型把它当噪声。零NaN的幻觉比真NaN更危险
- **基本面字段分三类**：ratio型(稳定)、YoY型(稳定)、absolute型(需年化)。AKShare ROE_AVG是累计值(Q1=5%/FY=21%)，直接用会让模型学到"Q1总是低"的假季节性信号
- **Benchmark禁止放入交易池**：usqqq加入trading pool后，QQQ本身参与了回测收益计算，导致Sharpe虚高。benchmark必须外置于instruments list

### 2026-04-19
- **5场批量复盘+10条新规则(v5.2+v5.3)** — 申花+利兹+纽卡+热刺+切尔西，累计28场ROI+3.4%。新规则：半场领先角球-2.5/弱队摆烂反转O2.5/XGB Draw幻觉过滤/崩盘叙事买对手胜/纯模型EV>+10%保留50%仓位等
- **XGB特征代理BUG-01修复** — predict_single.py只取主队最近一场→客队信息丢失。曼城vs阿森纳匹配到曼城vs诺丁汉森林→Draw 66%幻觉。修复为主客分头取+市场实时注入。Draw 66%→37%，Over 2.5新激活72.7%
- **初→终盘口变化规律挖掘(n=3229)** — "大热必死"是民间错觉(n=482,edge=+0.06%)。真陷阱：中档赔率+异常移动5-10%(n=426,edge=-4.54%,p=0.064)
- **market_alerts规则引擎上线** — 4条统计支撑的盘口异常检测规则编码到market_alerts.py，集成predict_single.py
- **sgodds.com初盘爬虫** — 填补The Odds API只有快照无初盘的数据缺口，支持1X2/亚盘/大小球/BTTS
- **3场新赛前分析** — 维拉vs桑德兰(U2.5 EV+23.6%)+埃弗顿vs利物浦(O2.5 EV+19.2%)+曼城vs阿森纳(修复后Arsenal胜EV+45.9%)
- **用户下注¥72** — 埃利O2.5@1.78¥30+角球O10.5@2.01¥12+维桑U2.5@1.85¥30
- **港股圆桌周报首次自动化(automation-6)** — 6只标的圆桌讨论，westock-data批量查询HK代码不支持需逐个查

#### 4/19 新踩坑经验
- **XGB单场代理必然失真**：任何基于"主队最近一场"的代理都丢失对战信息。修复：主客分头取(_home从主场历史/_away从客场历史)+市场类实时注入+H2H用NaN让XGB中位数填充
- **"大热必死"是民间错觉**：n=482场主胜<1.5的比赛，edge=+0.06%(p=1.0)，市场定价完全充分。真正的陷阱是中档赔率+异常移动(n=426,-4.54%,p=0.064)。不要脑补反买<1.5赔率
- **westock-data批量查询港股代码格式**：hk00700,hk09626格式批量查询返回空，需逐个查询。所有MCP工具的批量能力在自动化前必须先验证

### 2026-04-20
- **海港vs重庆中超R7赛前分析** — 海港9人伤病+重庆6轮不败→λ_home=0.444极低，U2.5 EV+43.8%。XGB因中超队名不匹配特征库静默跳过。用户¥40全重庆方向
- **水晶宫vs西汉姆EPL R33赛前分析** — HOME_COLD_TRAP触发(ML 2.20→2.61 +18.6%)，脑算反转纯模型方向。用户¥30(O2.5@1.86+WH+0.5@1.51)
- **港股日报手动补跑** — automation-4从4/17起连续4天未执行(静默失败)，手动补跑4/20日报。五股四涨一跌
- **GitHub Trending W17** — Agent自进化爆发+claude-mem记忆赛道+语音AI+金融AI

#### 4/20 新踩坑经验
- **自动化静默失败多日无告警**：automation-4从4/17到4/20连续4天未执行但无任何告警。自动化任务必须有 staleness 检测（最近成功执行时间 > 2x 预期间隔→告警）
- **中超XGB队名不匹配静默跳过**：CSL中文队名不在XGB特征库(英超/西甲/意甲英文名)，XGB返回None不报错。ML模型跳过必须记录原因，不能静默
- **market_alerts HOME_COLD_TRAP实战验证**：水晶宫主胜2.20→2.61(+18.6%)触发，机构明确看衰主胜，规则引擎首次EPL实战验证

### 2026-04-21
- **水晶宫vs西汉姆自动复盘** — 0-0闷平，AI融合-¥32.02(ROI-68.1%)💀，用户-¥14.90。Saar 81'进球被VAR吹(手球)。v5.5新规则2条：欧战疲劳+保级保守=U2.5优先/战意≠进攻
- **布莱顿vs切尔西赛前分析** — Chelsea 4连败+3-4首发缺，v5.5"战意≠进攻"完美匹配。U2.5@2.20+Brighton DNB@1.75+O10.5角球@2.11
- **伯恩利vs曼城赛前分析** — XGB O2.5 shift -21.4pp(源: Burnley vs Brighton/ManCity vs Chelsea)与脑算62%严重分歧→放弃大小球市场，AH Burnley+2.25为主注
- **美股持仓日报** — RBLX $61.83(+2.47%)浮亏-19.70% / CRCL $106.36(+0.42%)浮盈+0.20%。RBLX儿童安全和解+CRCL Drift诉讼+CLARITY Act妥协延迟
- **港股持仓日报** — 恒指26,361创反弹新高。泡泡+2.18%南向暴买+117万股 / B站-3.02%异环4/23公测 / 小米+0.25%前特斯拉厂长加盟
- **每日选股扫描** — 8只精选：东山精密(78)AI算力PCB+兆易创新(75)存储国替+中国移动(74)+巨子生物(72)

#### 4/21 新踩坑经验
- **欧战疲劳系统性压制进球**：双方均有欧战中周赛→combined lambda * 0.75。水晶宫vs西汉姆模型预测O2.5但实际0-0(xG~1.2)。欧战疲劳+保级/保级=U2.5优先信号
- **XGB源对手强度不匹配时shift不可信**：伯恩利vs曼城中XGB源为Brighton/Chelsea(中等对手)，与实际对手强度差距大。>20pp shift且源不可信→忽略该市场XGB
- **选股过滤器边界条件**：A股NetProfitGrowRate返回空、港股PE需放宽、美股MACD预设不支持。空结果≠无匹配，可能是过滤器错误。需渐进放宽策略
- **战意≠进攻(v5.5验证)**：保级/欧战资格球队往往更保守而非更进攻。高动机+防守能力=堡垒模式(U2.5)。首次实战验证成功

### 2026-04-22
- **海港1-2重庆复盘** — 用户+¥65.40(ROI+163.5%)🔥🔥🔥🔥，AI -¥0.09。用户选+0.5@2.07 vs AI选+0.75@1.82，line selection优势
- **布莱顿3-0切尔西复盘** — 用户+¥24.00(DNB ✅)，AI +¥3.92(DNB✅+角球✅+U2.5❌)。DNB+U2.5逻辑矛盾暴露
- **申花vs青岛赛前分析** — 主胜64%/U2.5优先/H2H五连零封。用户¥90（4注含角球¥50核心注）
- **累计战绩更新** — 34场/22场有记录, ~¥1532投入, +¥157.28(ROI +10.3%)
- **CRCL暴跌-9.72%** — 加密板块传染(COIN-7.41%/HOOD-5.31%)，用户明确不加仓$96。操作建议升级为价位表
- **美股持仓日报** — RBLX $61.26(-0.92%)浮亏-20.4% / CRCL $96.02(-9.72%)浮亏-9.54%。RBLX 4/25起财报冻结
- **港股持仓日报** — 恒指-1.22%，B站-5.75%暴跌（异环4/23公测）/ 泡泡南向+387万股暴买
- **每日选股扫描** — 精选11只，光模块主线爆发(中际/东山/新易盛/ASMPT/AVGO)
- **量化系统阶段收尾** — RDAgent Summary重写(美股+9.1%/港股负贡献)、MEMORY蒸馏9文件、清理~920MB、下阶段Task 4.1/4.2
- **ARKK日报** — $77.38(-2.45%)跑输大盘，cathiesark连续8天无交易更新

#### 4/22 新踩坑经验
- **用户亚盘选线持续跑赢AI**：海港1-2重庆，AI选重庆+0.75@1.82 vs 用户选+0.5@2.07，用户ROI+163.5%。方向一致时，用户的盘感在line selection上有结构性优势
- **加密板块传染性暴跌不要接飞刀**：CRCL-9.72%/COIN-7.41%/HOOD-5.31%同日暴跌，地缘+政策双重打击。板块性下跌当日不加仓，等2-3日缩量再评估
- **操作建议必须带价位**：用户明确要求日报给出具体买点卖点，不只是HOLD/BUY标签。每只持仓需4行操作表：加仓区/持有区/减仓区/止损位
- **cathiesark连续8天无更新**：交易数据停留在4/10，接近数据源失效阈值。14天无更新需切换到备选源

### 2026-04-23
- **football-betting v5.7 大迭代** — must_retain机制(高EV纯模型注强制保留)+XGB源质量审计+伤停CLI量化(6参数)+角球3新因子+规则冲突优先级金字塔(P0-P4)
  - 端到端验证通过（伯恩利vs曼城），284 tests passed
  - v5.7 must_retain回测：伯恩利U2.5 EV+17.6%被v5.6丢弃→v5.7保留→预估ROI+16%
- **申花2-0青岛复盘** — AI融合+¥94.15🔥(本季最佳)，用户4注全中+¥103.40(ROI+114.9%)
  - 累计战绩：24场/¥1652投入/+¥230.68(ROI+14.0%)
- **伯恩利0-1曼城复盘** — AI融合+¥0.14微利，纯模型+¥5.50。v5.6规则新增：XGB极端shift+弱队属性一致→50%仓位
- **港股持仓日报** — 恒指-0.95%，新增三花(30.00)+赛力斯(81.20)跟踪，组合8只
- **美股持仓日报** — RBLX $59.64(-2.64%)浮亏-22.55% / CRCL $104.36(+8.69%V型反弹)浮亏-1.69%
- **ARKK日报** — $79.30(+2.48%)，cathiesark 500错误(第13天无交易数据)，新浪MinKline失效，StockAnalysis.com升级为备选

#### 4/23 新踩坑经验
- **纯模型高EV注被脑算系统性丢弃**：设计缺陷，不是个案。must_retain机制是结构性修复——不是"永远听模型"而是"不可以悄悄丢弃"
- **双数据源同期失效**：cathiesark(500)+新浪(deprecated)同日失效。同生态数据源可能同时受限，需跨生态(中美混合)覆盖
- **规则冲突需治理框架**：20+条规则必然冲突，P0-P4优先级金字塔确保解决可追溯。一致性(P0)永远优先于模型信号(P1)

| Workspace | 用途 |
|-----------|------|
| `20260312212515` | 最早测试 |
| `20260313100121` | Python 项目 |
| `20260313204723` | ARKK 跟踪计划 |
| `20260313204751` | 加班餐费报销 |
| `20260317114135` | 巴萨盘口分析 + 价值引擎 |
| `20260317195416` | Unity 游戏资源 |
| `20260320102012` | 自我改进自动化 |
| `20260321162316` | 足球投注分析（纽卡/富勒姆/热刺等） |
| `20260321162425` | XYMini 开发方案 + 竞品拆解（已迁移至 survival-demo） |
| `20260322113041` | WorkBuddy Vault（Git 知识库归档） |
| `20260323102121` | 加班餐报销（重命名自 A1周六加班餐报销）|
| `A1周六加班餐报销/` | 加班餐报销目录（按日期分文件夹）|
| `Claw/` | TAPD 催单系统（Maple 项目） |
| `football-betting/` | 足球博彩分析（复盘追踪器、投注分析） |
| `arkk-tracker/` | ARKK 自动化日报（持续运行） |
| `stock-analysis/` | 个股投资分析（RBLX、CRCL） |
| `stock_trader/` | 港美股 AI 量化交易系统（Qlib + Futu） |
| `github_trending/` | GitHub Trending 周报自动化（每周一 09:00） |
