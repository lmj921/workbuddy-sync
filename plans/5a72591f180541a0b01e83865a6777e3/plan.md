## 用户需求

1. 港股圆桌周报有2个自动化任务，删掉一个
2. 保留的任务不要推送企业微信（删除 Step 7 企微推送）
3. 海天味业上周已卖掉，从周报标的列表中移除

## 产品概述

对港股圆桌周报自动化任务进行精简：删除重复任务、取消企微推送、移除已清仓标的

## 核心功能

- 删除 `hk-weekly-roundtable` 自动化任务，保留 `automation-6`
- 修改 automation-6 的 prompt：移除 Step 7（企微推送）、移除海天味业(hk03288)相关内容
- 更新 MEMORY.md：移除海天味业持仓记录、更新自动化配置表
- 更新 automation-6/memory.md

## 实现方案

### 需要修改的内容

**1. 删除重复自动化任务**

- 删除 `hk-weekly-roundtable` 自动化任务（通过 automation_update 工具，mode=delete）
- 保留 `automation-6`（港股圆桌周报）

**2. 修改 automation-6 的 prompt**

- 移除 **Step 7：企微推送摘要** 整个步骤
- 移除关注标的中的 `海天味业 hk03288`
- 移除专家-标的映射表中的 `海天味业 | 文仔+坤仔+钊仔` 行
- 更新 Step 1 中的关注标的列表为5只：腾讯、哔哩哔哩、招商证券、泡泡玛特、小米

**3. 更新 MEMORY.md**

- 移除 `## 海天味业 (03288.HK)` 整个章节
- 自动化配置表：删除 `hk-weekly-roundtable` 行，将 `automation-6` 行的推送改为 `❌ 无推送`
- 港股持仓汇总：移除海天味业相关内容
- westock-partner 集成：专家映射中移除 `海天→文仔+坤仔+钊仔`

**4. 更新 automation-6/memory.md**

- 记录海天味业已移除、企微推送已取消

### 文件变更清单

```
/Users/a1_builder/WorkBuddy/stock-analysis/
├── .codebuddy/automations/automation-6/memory.md   # [MODIFY] 更新执行记录，标注海天移除+推送取消
├── .workbuddy/memory/MEMORY.md                     # [MODIFY] 移除海天味业章节、更新自动化配置表、更新专家映射
```

### 自动化任务操作

- [DELETE] hk-weekly-roundtable 任务
- [UPDATE] automation-6 prompt：移除 Step 7 + 移除海天味业