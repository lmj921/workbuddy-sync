## 用户需求

"更新一下，同时整理下工作目录，各种临时文件看看要不要清理下，上下文也要压缩下，目前token消耗有点大"

## 核心任务概览

基于上一轮的根因排查结论，对 stock_trader 项目做一次认知更新 + 工作目录整理 + 长期记忆压缩的综合收尾。四项决策已澄清：报告完整重写（A）、git_ignore_folder 保留 batch4/5/6（B）、日志/缓存目录不动（D）、>14 天 memory 日文件蒸馏后删除（A）。

## 核心功能

### 1. 报告纠偏

完整重写 `docs/Task_3.5_3.6_RDAgent_Summary.md`，用真实结论覆盖错误叙事：

- 美股 RDA 真实 alpha +9.1%（非 +80% 飞跃、非 -25% 退化）
- 港股 RDA 整体负贡献（结论不变，生产仍用纯 HKFullV2）
- 生产配置：美股 USRDAgentV1（Sharpe 1.4641）、港股 HKFullV2（Sharpe 1.7371）
- 附根因排查章节：记录 us.txt 标的池 139→144、历史延长、test 末延长如何污染 AB 基线

### 2. 工作目录整理（仅删机械垃圾，不碰认知依赖）

- 根目录：删除 `_update_fmp.py`、`Users/a1_builder/` 空壳、`scripts/fetch_all_watchlist.py.bak`
- `git_ignore_folder/` 删除 batch1/2/3 + 早期快照 + invalid workspace + 两个空 batch6 包（释放 ~920M），保留 batch4/5/6 及当前 workspace
- 保留 log/ logs/ pickle_cache/ 原样（用户明确选 D）
- **严禁删除** `data/qlib_data/bin/instruments/*.bak*`（AB 对照复现依赖）

### 3. 长期记忆压缩

- 扫读 9 个 >14 天日文件（2026-03-24 ~ 2026-04-03），按主题把跨 session 有价值的事实/决策/踩坑蒸馏进 MEMORY.md（去重、不累积个例）
- 删除 9 个原日文件，保留 2026-04-04 ~ 2026-04-18 共 11 个日文件
- 今日日志追加本次整理记录

### 4. 可验证性

每批删除前后用 `du -sh` 对账实际释放量；报告完成后人工复核核心数字；memory 蒸馏后 MEMORY.md 保持可读且无冗余。

## 任务性质

纯文档整理 + 文件系统清理 + 长期记忆蒸馏，不涉及代码改动、依赖变更或架构调整，因此无需选型技术栈，只定义执行规范。

## 执行规范

### 1. 文件删除安全规则

- **白名单思维**：删除前先 `ls -la` 核对路径和大小，避免误删
- **分批 rm**：根目录垃圾、git_ignore_folder 备份、老 memory 日文件三批独立执行，每批前后 `du -sh` 对账
- **bin/.bak 绝对保留**：`data/qlib_data/bin/instruments/us.txt.bak`、`us.txt.bak4`、`hk.txt.bak`、`all.txt.bak` 是 AB 对照实验复现依赖，本次任务不触碰
- **日志/缓存不动**：`log/`、`logs/`、`pickle_cache/`、`mlruns/`、`catboost_info/` 按用户决定 D 全部保留
- **密钥不动**：`.env`、`.env.rdagent` 本次不涉及
- **不执行 git add/commit**：用户未要求，避免 blast radius 扩散

### 2. 报告重写准则

- 覆盖式重写，不做增量补丁；旧版的"+80% 飞跃"、"RDA 负贡献（美股）"两个错误叙事必须消除
- 结构：概述 → 真实结论（美股/港股分述）→ 生产决策 → 根因排查（instruments 池变化时间线）→ 经验教训 → 附录（AB 对照数据表）
- 核心数字必须来自已锁定的 MEMORY.md 事实（Sharpe 1.3349 / 1.4563 / 1.9625 / 1.4641 / 1.7371 / 1.1178），不新造数据
- 日期口径：明确区分 4/14 旧 pool 测试 和 4/18 新 pool 复现

### 3. MEMORY.md 蒸馏准则

- 蒸馏原则：**跨 session 仍有用的**才写，重复的/单次个例的不写
- 主题分类建议（合并同主题而非按日期堆叠）：
- 项目约定与配置（数据路径、市场切换脚本、工作区边界）
- 数据层事实（bin 列数、handler 实际读取的字段、instruments 池结构）
- Qlib/RD-Agent 踩坑（parquet swap、FMP 免费版限制、bin dump 参数等）
- AB 验证方法论（先查"啥变了"再猜"因子退化"）
- 生产配置历史（各批次因子采用/淘汰决策）
- 蒸馏完成后 MEMORY.md 行数预计控制在 ~200 行内（当前 117 行，追加后不宜超过 250 行）
- 老日文件删除前先确认蒸馏 diff 已落地

### 4. Blast Radius 控制

- 本次不改任何 `.py` 源码、`.yaml` 配置
- 不触发 rebuild、retrain、backtest
- 不改动 `.gitignore`（现有规则已覆盖 Users/、_update_fmp.py、log/、logs/ 等）
- 所有删除命令在本地文件系统执行，不涉及远端

## 目录结构变更清单

```
stock_trader/
├── _update_fmp.py                                      # [DELETE] 15KB 临时脚本，已 gitignored
├── Users/a1_builder/                                   # [DELETE] 空壳目录
├── scripts/
│   └── fetch_all_watchlist.py.bak                      # [DELETE] 旧备份
├── git_ignore_folder/
│   ├── RD-Agent_backup_20260411_011454/                # [DELETE] 66M 早期快照
│   ├── RD-Agent_backup_batch1_20260411_102223/         # [DELETE] 72M
│   ├── RD-Agent_backup_batch2_20260411_152816/         # [DELETE] 447M
│   ├── RD-Agent_backup_batch3_20260411_160358/         # [DELETE] 147M
│   ├── RD-Agent_workspace_batch3_invalid_20260411_235927/  # [DELETE] 101M invalid
│   ├── RD-Agent_backup_batch6_20260412_204426/         # [DELETE] 12K 空包
│   ├── RD-Agent_backup_batch6_20260412_205954/         # [DELETE] 12K 空包
│   ├── RD-Agent_backup_batch4_20260412_111432/         # [KEEP] 399M 美股有效因子来源
│   ├── RD-Agent_backup_batch4_20260418_105930/         # [KEEP] 37M
│   ├── RD-Agent_backup_batch5_20260412_123258/         # [KEEP] 421M
│   ├── RD-Agent_backup_batch6_20260412_201355/         # [KEEP] 215M
│   ├── RD-Agent_workspace/                             # [KEEP] 172M 当前工作区
│   ├── RD-Agent_factor_data/                           # [KEEP] 13M
│   └── factor_implementation_source_data/              # [KEEP] 13M 激活数据
├── data/qlib_data/bin/instruments/
│   ├── us.txt.bak / us.txt.bak4 / hk.txt.bak / all.txt.bak  # [KEEP-CRITICAL] AB 复现依赖
├── docs/
│   └── Task_3.5_3.6_RDAgent_Summary.md                 # [REWRITE] 完整重写为真实结论+根因章节
├── .workbuddy/memory/
│   ├── 2026-03-24.md ~ 2026-04-03.md (9 个文件)        # [DELETE after 蒸馏]
│   ├── 2026-04-04.md ~ 2026-04-18.md (11 个文件)       # [KEEP]
│   ├── MEMORY.md                                       # [APPEND] 蒸馏 9 个老日文件的跨 session 要点
│   └── 2026-04-18.md                                   # [APPEND] 追加本次整理记录
```

## 执行顺序约束

1. 先做认知类（报告重写 + MEMORY.md 蒸馏），需要细读现有内容，防止误删有价值信息
2. 再做机械删除类（三批 rm），每批前 `du -sh` 预览，后 `du -sh` 对账
3. 最后补记今日 memory 日志（简短，3-5 行）
4. 不需要最终 `git status` 收尾（修改都在 gitignored 区域 + docs 文档，用户未要求 commit）