# Task 4.1 + 4.2 — 因子管理工程化 Plan

> 创建：2026-04-27
> 预估：3 天（1.5d + 1.5d）
> 前置：已有 `src/factor/registry.py`（集合级注册）+ `scripts/factor_ab_test.py`（单模型版 AB）+ 两份 `ab_rdagent_*.py` 重复脚本

---

## 1. 现状梳理（Phase 1 探索结论）

### 1.1 因子代码分布（绝对路径 + 行号）

| 文件 | 内容 | 关键位置 |
|------|------|---------|
| `/Users/a1_builder/WorkBuddy/stock_trader/src/factor/alpha101.py` | WQ101 因子 62~79 个 | `get_wq101_features()` |
| `/Users/a1_builder/WorkBuddy/stock_trader/src/factor/alternative.py` | 资金流代理 16 个 | L24 `get_moneyflow_proxy_factors()` / L165 `get_factor_set()` |
| `/Users/a1_builder/WorkBuddy/stock_trader/src/factor/hk_specific.py` | 港股专属 12 个 | L17 `get_hk_specific_factors()` |
| `/Users/a1_builder/WorkBuddy/stock_trader/src/factor/hk_full_v2_handler.py` | **4 个 Handler 类** | L21 `HKFullV2` / L97 `Alpha158MoneyflowV2` / L164 `USRDAgentV1` / L297 `HKRDAgentV1` |
| `/Users/a1_builder/WorkBuddy/stock_trader/src/factor/rdagent_bridge.py` | RDA parquet 加载 | （USRDAgentV1 依赖）|
| `/Users/a1_builder/WorkBuddy/stock_trader/src/factor/registry.py` | **集合级**注册中心 | L23 `FactorRegistry` / L30 `_register_builtin` 9 个集合 |
| `/Users/a1_builder/WorkBuddy/stock_trader/src/factor/evaluator.py` | IC/IR/分组回测评估器 | - |
| `/Users/a1_builder/WorkBuddy/stock_trader/config/factors.yaml` | 集合启用配置 | 10 个 entry，active=`alpha158` |

### 1.2 当前"因子声明"方式

每个因子 = `(Qlib 表达式字符串, name 字符串)`，存在**模块级 Python 函数**里返回 `(fields, names)` 两个等长 list。**没有** category / market / version / ic_mean / ir / author / description 元数据。

### 1.3 AB 脚本重复度

| 脚本 | 行数 | 模型 | 用途 |
|------|------|------|------|
| `scripts/factor_ab_test.py` | 202 | **LGB only** | Task 2.4 港股 2 集合对比 |
| `scripts/ab_rdagent_v1.py` | 320 | **LGB+CatBoost 集成** | 美股 RDA AB |
| `scripts/ab_rdagent_hk_v1.py` | 334 | **LGB+CatBoost 集成** | 港股 RDA AB |
| `scripts/ab_fundamental.py` | 221 | - | 老的基本面 AB |

`ab_rdagent_v1.py` vs `ab_rdagent_hk_v1.py` **~90% 重复**（只有 TOPK/N_DROP/INSTRUMENTS/HANDLERS dict 不同 + 港股多一个 `--filtered` 开关）。

`factor_ab_test.py` 已经是 click 单模型通用版，但用的是自建 daily_return 而非 Qlib 标准回测，且只跑 LGB，**和生产不一致**。

### 1.4 CLI 入口

`scripts/cli.py` 是 click group，现有子命令：`fetch` / `fetch-fundamental` / `train` / `signal` / `trade` / `status` / `stock` / `backtest` / `paper-trade` / `pending-orders`。添加新子命令是标准 `@main.command()` 装饰器。

---

## 2. 设计决策

### 2.1 Task 4.1 — 因子注册中心

**定位**：**单因子级**的元数据注册（当前 registry 是集合级，保留不动，上层增量）。

**数据模型**：`FactorMeta` dataclass
```python
@dataclass
class FactorMeta:
    name: str                          # e.g. "OBV_RATIO_5"
    expression: str                    # Qlib 表达式 或 "PARQUET:<col>" / "FUNC:<module.func>"
    category: str                      # alpha158 / wq101 / moneyflow / hk_specific / rdagent / fundamental
    markets: list[str]                 # ["hk"] / ["us"] / ["hk","us"]
    version: str = "1.0"
    author: str = "joker"
    description: str = ""
    ic_mean: float | None = None       # 评估后回填
    ir: float | None = None
    source_file: str = ""              # 定位原文件
    enabled: bool = True
```

**存储**：启动时一次性扫描+注册，存在内存 dict；**评估后**通过 `registry.update_metric(name, ic=0.03, ir=0.8)` 回填到 `config/factors_meta.yaml`（新增，作为持久化 overlay）。

**装饰器**：`@register_factor(meta=FactorMeta(...))` 可选接入，对现有函数级因子**不强制改**，用 **adapter** 一次性把现有 `get_*_factors()` 的结果包装成 FactorMeta 批量注册。

**CLI**：新增 `scripts/cli.py` 子命令 `factor`：
```bash
python scripts/cli.py factor list [--category moneyflow] [--market hk] [--min-ic 0.02]
python scripts/cli.py factor info OBV_RATIO_5
python scripts/cli.py factor eval <name> -m hk              # 单因子跑 evaluator 并回填 IC/IR
python scripts/cli.py factor history <name>                 # 版本历史（暂用 git log on meta yaml）
```

**保底原则**：
- **不修改** 现有 `HKFullV2/USRDAgentV1` 等 Handler（工程化 = 加层，不改生产）
- 现有 `FactorRegistry`（集合级）作为"bundle"，`FactorMeta`（单因子）作为"atom"，两者共存
- 现有 `config/factors.yaml`（集合配置）保留，新增 `config/factors_meta.yaml`（单因子元数据 overlay）

### 2.2 Task 4.2 — 统一 AB CLI

**新脚本**：`scripts/factor_backtest.py`（**新写**，替换 `factor_ab_test.py` / `ab_rdagent_v1.py` / `ab_rdagent_hk_v1.py` 三个）

**命令设计**：
```bash
python scripts/cli.py factor ab \
  -m hk \
  --baseline HKFullV2 \
  --candidate HKRDAgentV1 \
  --seeds 42,2024,7777 \
  --model ensemble \         # lgb / catboost / ensemble (default)
  --topk 15 --n-drop 3 \     # 默认读 strategy.yaml
  [--rdagent-parquet <path>] # 可选传给 HKRDAgentV1
```

**市场默认参数**（从 `config/strategy.yaml` 读）：
- hk: TopK=15, N_Drop=3
- us: TopK=10, N_Drop=2
- hk train/valid/test 窗口 从 `config/strategy.yaml` 读
- us: train=2020-01~2024-06 / valid=2024-07~2025-06 / test=2025-07~今天-1（从 qlib 日历取）

**模型参数**：封装 `src/backtest/ab_runner.py`，提供 `build_dataset()` / `train_ensemble()` / `qlib_backtest()` 三层，直接复用 `ab_rdagent_v1.py` 验证过的 PortfolioMetrics 流程（含 `_cal_benchmark` monkey patch）。

**输出**：JSON + HTML（Plotly 累计净值曲线），落到 `logs/analysis/factor_ab_{market}_{ts}.{json,html}`。

**安全门槛**：沿用 `factor_ab_test.py` 的 `ratio >= 0.95` 判定。

### 2.3 Handler 注册

在 `src/backtest/ab_runner.py` 内维护一个 `HANDLER_MAP`（从 `hk_full_v2_handler.py` 导入 4 个），**不重构现有 Handler**。未来新 Handler 自己加一行即可。

---

## 3. 实施步骤（落地顺序）

### Day 1（Task 4.1 上）
1. `src/factor/meta.py`：`FactorMeta` dataclass + `@register_factor` 装饰器
2. `src/factor/registry.py`：**增加**单因子注册方法 `FactorRegistry.register_atom(meta)` / `list_atoms()` / `find_atom(name)`，不动现有集合级逻辑
3. `src/factor/_auto_register.py`：扫描 `get_moneyflow_proxy_factors` / `get_hk_specific_factors` / `get_wq101_features` / `Alpha158DL`，批量生成 FactorMeta 注册
4. `config/factors_meta.yaml`：持久化 overlay 文件（IC/IR 回填用）

### Day 1（下）—— Task 4.1 CLI
5. `scripts/cli.py` 新增 `factor` 子命令 group（list / info / eval / history）
6. `factor eval` 调用现有 `src/factor/evaluator.py`，结果写回 `config/factors_meta.yaml`

### Day 2（Task 4.2 核心）
7. `src/backtest/ab_runner.py`：抽取 `ab_rdagent_v1.py` 的 `build_dataset` / `train_and_backtest`，参数化 market/TOPK/N_DROP/handler_class
8. `scripts/factor_backtest.py`：新的统一入口，接 `ab_runner`
9. `scripts/cli.py` 新增 `factor ab` 子命令（薄壳，调 `factor_backtest.py`）

### Day 3（验证 + 收尾）
10. **对照测试**：用新 CLI 跑 `HKFullV2 vs HKFullV2`（baseline 自比）+ `Alpha158MoneyflowV2 vs USRDAgentV1`，确认和 `ab_rdagent_v1.py` 历史结果一致（Sharpe 差 < 0.02）
11. 归档老 AB 脚本到 `scripts/legacy/`：`git mv scripts/ab_rdagent_v1.py scripts/ab_rdagent_hk_v1.py scripts/factor_ab_test.py scripts/ab_fundamental.py scripts/legacy/`，保留可追溯不阻碍新代码
12. 更新 `docs/ROADMAP_v0.2.md` Task 4.1/4.2 勾选
13. 更新 `MEMORY.md` 与今日日记

---

## 4. 不做的（明确范围）

- ❌ 不改 `HKFullV2` / `USRDAgentV1` 等 4 个 Handler 类
- ❌ 不改 `config/factors.yaml`（集合级配置保留）
- ❌ 不做 Task 4.3 衰减监控（下阶段）
- ❌ 不做因子依赖图（Task 4.1 描述里的，简化掉）
- ❌ `factor history` 子命令用 `git log config/factors_meta.yaml` 一行搞定，不做复杂版本 DB

## 5. 关键风险

| 风险 | 缓解 |
|------|------|
| 新 AB 结果和旧脚本不一致 | Day 3 Step 10 做对照测试，Sharpe 差 < 0.02 才算通过 |
| `_cal_benchmark` monkey patch 副作用 | 复用 `ab_rdagent_v1.py` 既有实现，不重写 |
| FactorMeta 与现有集合级 registry 冲突 | 单因子和集合级分离（atom vs bundle），同一 registry 两套方法 |
| Qlib 日历取 test 末日踩坑 | 复用 `ab_rdagent_v1.py` L163-165 `end_time >= cal[-1]` 降级逻辑 |

## 6. 验收标准

- [ ] `python scripts/cli.py factor list -m hk` 能列出 265+ 个港股因子，带 category/IC 列
- [ ] `python scripts/cli.py factor info OBV_RATIO_5` 输出元数据
- [ ] `python scripts/cli.py factor ab -m hk --baseline HKFullV2 --candidate HKFullV2` 两组 Sharpe 差异 < 0.02（自比，集成模式）
- [ ] `python scripts/cli.py factor ab -m us --baseline Alpha158MoneyflowV2 --candidate USRDAgentV1 --seeds 42,2024,7777 --model ensemble` 结果和历史 `scripts/legacy/ab_rdagent_v1.py` JSON 对齐（Sharpe 差 < 0.02）
- [ ] `logs/analysis/factor_ab_*.html` 有 Plotly 累计净值对比图
- [ ] 新增/修改文件总量 < 1500 行，不删旧 Handler
- [ ] `scripts/legacy/` 目录下老 AB 脚本可用（仅作为历史对照）

## 7. 用户决策确认（2026-04-27）

1. **FactorMeta 接入**：Adapter 自动扫描现有 120+ 存量因子（一次性批量注册），**不改**原函数定义
2. **AB 默认模型**：LGB+CatBoost 集成（和生产对齐），支持 `--model lgb|catboost|ensemble` 切换
3. **老 AB 脚本**：归档到 `scripts/legacy/`（`git mv`，不删）
4. **factor history**：用 `git log on config/factors_meta.yaml`，不做独立版本表
