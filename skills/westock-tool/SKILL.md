---
name: westock-tool
description: 选股 / 选基工具——按条件、策略、标签、事件、排行从全市场批量筛选股票或 ETF。当用户问"找一只 / 哪些股票 / 帮我选 / 推荐 / 排行榜 / TOP / 筛选 / MACD金叉 / 央企股 / ST股 / 高股息ETF"时使用。提供 filter（自定义条件）、strategy（预置策略）、label（标签/ETF主题）、event（事件触发）、ranking（排行，支持在板块/标签/策略/事件结果内二次排序）等入口。本技能只做"批量筛选"；查单只标的详细数据用 westock-data。
---

# WeStock Tool

**作用**：五种选股 / 选基方式——条件（filter）、策略（strategy）、标签（label）、事件（event）、排行（ranking）。

**数据源**：腾讯自选股选股接口 | 条件选股：A股/港股/美股 | 策略/标签/事件/排行（股票）：仅 A股 | ETF：沪深 ETF（`--asset etf`）。

---

## 必读文档（按需取用）

- 📖 **[references/scenarios-guide.md](./references/scenarios-guide.md)** — **路由与场景速查**：路由与边界铁律（严禁事项 / 与 westock-data 边界 / 清单查询）、同义需求 → 命令对照表、价值/技术/资金/港美股/组合查询等 30+ 场景模板
- 📖 **[references/fields-guide.md](./references/fields-guide.md)** — 字段速查：行情/估值/财务/技术/ETF 全部字段（含沪深 vs 港美对照）
- 📖 **[references/ai_usage_guide.md](./references/ai_usage_guide.md)** — 完整命令语法、预设/策略/标签/事件清单、返回字段说明、数据更新频率
- 📖 **[references/etf-pools.md](./references/etf-pools.md)** — ETF 主题池 + 排行指标完整表
- 📖 **[references/ranking-indicators.md](./references/ranking-indicators.md)** — 排行指标 + `--min-<字段>` 对照表

---

## 核心铁律（路由必读）

1. **命中本 Skill 能力域时，禁止绕过**——不要用 HTTP 直连（curl/fetch）、通用网页搜索、其它选股 Skill/MCP、训练数据替代。**禁止手搓筛选**（先 westock-data 拉行情再 Python 排序过滤是反模式，本 Skill 的 `filter`/`ranking` 已直接支持）。
2. **"哪些 X 可以用"必须执行 `--list`**——`event/label/strategy/ranking --list`、`filter --list-presets`，**不要凭文档/记忆列举**（示例不全且会过时）。
3. **6 命令路由**——按用户表述形态选择：
   - 自定义条件（"PE<20且ROE>15"）→ `filter "<表达式>"`
   - 条件型预设（"低PE股 / 高股息股"）→ `filter --preset`
   - 策略信号（"MACD金叉 / 巴菲特策略"）→ `strategy`
   - 静态分类（"央企 / ST / 新股 / 破净"）→ `label`
   - 时间窗口事件（"近期解禁 / 回购 / 大宗交易"）→ `event`
   - 排序、TOP、最多/最少、"X 里的 Y 最高"→ `ranking`（含 `--within-label/strategy/event`、`--universe`）
4. **概念股 ≠ 选股**——"XX 概念股" 用 `westock-data search <关键词> --type sector`，不属本工具。

> ⚠️ 用 `--list` 取清单 + 读 [scenarios-guide.md](./references/scenarios-guide.md) 解决"用哪个命令"。

---

## 与 westock-data 边界（高频误判）

> 用户问"**哪些股票** XX"/"**最近 N 天** XX 的股票" → **westock-tool event**（股票池）；
> 问"**某只股票** XX 明细"/"**某天** XX 清单" → westock-data calendar/lhb/notice 等。

常见配对（左→westock-tool，右→不要走 westock-data）：限售解禁→`event shareunlock_next_90`、业绩预约→`event earnings_schedule`、近期回购→`event buyback`、大宗交易/龙虎榜池→`event block_past_30`/`longhu_statis_past_15`、董监高变动/增减持→`event manager_change`/`manager_sharechg`。

---

## 调用约定

- **执行**：`node <本SKILL.md所在目录>/scripts/index.js <命令> [参数]`（**禁止硬编码安装路径**）
- 环境：Node.js ≥ v18，已单文件打包，无需 `npm install`
- 下文 `westock-tool <命令>` 是逻辑命令名
- **通用参数**：`--raw`（严格 JSON 输出）、`--limit`/`--offset`（分页，复用上次输出末尾的 `next offset`）、`--start`/`--end`（区间，避免单日×N 次）

---

## 已知限制

- 市场：沪深 A股、港股、美股；**不支持北交所**
- 字段名：沪深 vs 港美不同（`PE_TTM` vs `PeTTM` 等），**切勿混用**——详见 [fields-guide.md](./references/fields-guide.md)
- PE/PB 负值必须排除：`PE_TTM > 0`
- 港股/美股加 `--market hk` / `--market us`
- 多条件 AND **必须**用 `intersect([...])`，不支持 `&`/`&&`/`AND`；OR 用 `union([...])`

---

## 高频命令速查（inline 示例）

> 完整语法见 [ai_usage_guide.md](./references/ai_usage_guide.md)。以下为最高频场景，**可直接复制执行**。

```bash
# 1. filter — 自定义条件 / 预设
westock-tool filter "intersect([PE_TTM > 0, PE_TTM < 20, ROETTM > 15])"
westock-tool filter "intersect([PE_TTM > 0, PE_TTM < 15, ROETTM > 15])" --orderby ROETTM --desc
westock-tool filter "intersect([PeTTM > 0, PeTTM < 10, DivTTM > 5])" --market hk
westock-tool filter --preset LowPE --limit 30
westock-tool filter --list-presets

# 2. strategy — 策略信号（仅输出 code/name）
westock-tool strategy --list
westock-tool strategy macd_golden --date 2026-04-10
westock-tool strategy high_dividend,pb_roe                       # 多策略并查
westock-tool strategy macd_golden --start 2026-04-01 --end 2026-04-10

# 3. label — 静态分类标签
westock-tool label --list [分组]
westock-tool label shareholder_central_state                     # 央企（中央国资委）
westock-tool label valuation_lowpb,fin_high_roettm               # 多标签并查

# 4. event — 时间窗口事件
westock-tool event --list [分组]
westock-tool event shareunlock_next_90
westock-tool event manager_change,manager_sharechg

# 5. ranking — 排行 / 范围限定二次排序
westock-tool ranking --list
westock-tool ranking CompScore --limit 10                                # 综合评分 TOP10
westock-tool ranking fin_valuation --limit 10                            # 估值排行
westock-tool ranking margin_chg_d                                        # 两融日加仓榜
westock-tool ranking CompScore --within-label shareholder_central_state  # 央企里评分最高
westock-tool ranking fin_valuation --within-strategy macd_golden         # MACD金叉中估值最低
westock-tool ranking CompScore --within-event shareunlock_next_90        # 解禁股评分排行
westock-tool ranking fin_valuation --universe 11010001                   # 板块内估值排行
westock-tool ranking margin_in_days --min-MtInDays 5                     # 两融连续扩大≥5天
westock-tool ranking CompScore --asc                                     # 升序（评分最低）

# 6. ETF 选基 — label / ranking 加 --asset etf
westock-tool label --asset etf --list                            # 全部主题池
westock-tool ranking --list --asset etf                          # 全部 ETF 指标
westock-tool label high_dividend --asset etf
westock-tool ranking size --asset etf --limit 20                 # 规模榜
westock-tool ranking valuation --asset etf --orderby PB --asc    # PB 最低
```

---

## 关键提醒

- **`filter --list-presets` ≠ `strategy --list`**：preset 是条件型（含阈值参数），strategy 是信号型。
- **filter --preset vs strategy**：preset 输出含指标列；strategy 仅输出 code/name。
- **"央企" vs "国企"**：央企（中央国资委）→ `shareholder_central_state`；地方国企/口语"国企"→ `shareholder_local_state`；全量央国企 → 两者并查。
- **ranking 阈值用 `--min-<字段>`，不要用 `--limit`**——"评分>70" → `--min-CompScore 70`（`--limit` 是结果条数）。
- **`--min-<字段>` 字段名 ≠ 指标代码**（如 `cap_main_5d` 对应 `--min-MainSum5d`），必须查 [ranking-indicators.md](./references/ranking-indicators.md)。
- **label vs event**：label = 静态分类；event = 动态时间窗口。
- **股票代码**：沪/科创 `sh600519`、深 `sz000001`、港 `hk00700`、美 `usAAPL`。

---

## 重要声明

> 1. 本技能仅提供客观市场数据筛选，不含主观分析、投资评级或交易建议。
> 2. 不构成证券投资咨询服务，结果不应作为投资决策唯一依据。
> 3. 数据可能存在延迟，以交易所官方为准。
> 4. 投资有风险，决策需谨慎。

**数据来源**：腾讯自选股数据接口
