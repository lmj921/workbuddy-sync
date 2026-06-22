---
title: "TAPD A1分组统计"
description: "统计Maple项目A1分组的未完成需求和Bug，输出可视化分析报告"
agent_created: true
version: "1.0"
triggers:
  - "A1统计"
  - "A1分组统计"
  - "tapd统计"
  - "需求统计"
  - "bug统计"
  - "单子统计"
  - "跑统计"
  - "跑一次统计"
---

# TAPD A1分组统计 Skill

## 目的
统计Maple项目(workspace_id=20453876)中A1分组的未完成需求和Bug，按分组/人员/系统维度输出可视化分析报告。

## 前置条件
- TAPD MCP可用（通过 `mcp__tapd__proxy_execute_tool` 执行）
- A1成员名单存储在 `/Users/a1_builder/WorkBuddy/tapd_agent/.workbuddy/memory/MEMORY.md`

## 执行步骤

### Step 1: 查询未完成需求
调用 `stories_get`:
```json
{
  "tool_name": "stories_get",
  "tool_args": {
    "workspace_id": "20453876",
    "name": "LIKE<Maple_A1>",
    "status": "planning|developing",
    "with_v_status": "1",
    "fields": "id,name,status,owner,parent_id,begin,due,priority_label",
    "limit": 200
  }
}
```
- "未完成"定义: 仅 `planning`(规划中) 和 `developing`(实现中)
- 如果 count > 200，需翻页(page=2)

### Step 2: 查询A1成员的未关闭Bug
按分组分批查询（避免USER_OR超长）:

**客户端组(8人)**:
```json
{
  "tool_name": "bugs_get",
  "tool_args": {
    "workspace_id": "20453876",
    "status": "NOT_EQ<closed>",
    "current_owner": "USER_OR<arvinzhao|hugoyu|paradoxhe|oilyou|suiyuanpei|suijiwu|wisechen|liezhou>",
    "fields": "id,title,status,current_owner,created,priority_label",
    "limit": 200
  }
}
```

**服务器组(5人)**:
```json
{
  "tool_name": "bugs_get",
  "tool_args": {
    "workspace_id": "20453876",
    "status": "NOT_EQ<closed>",
    "current_owner": "USER_OR<jeffefang|externielin|jaykan|jianxingxu|jianmin>",
    "fields": "id,title,status,current_owner,created,priority_label",
    "limit": 200
  }
}
```

**美术组(完整24人，优先用 `bugs_count` 看积压量，避免 `bugs_get` 输出过大)**:
```json
{
  "tool_name": "bugs_count",
  "tool_args": {
    "workspace_id": "20453876",
    "status": "NOT_EQ<closed>",
    "current_owner": "USER_OR<morganzhu|minghaoye|lusisdzheng|tinklezhang|jiajunjjhe|baronbei|allanshen|sunwushi|xiaobingxue|ninafu|weikou|zpennxiao|xiangwwang|yafeizhang|nichohuang|ticanma|zirongsun|curryhrxu|wallezzhang|zakiazhou|alongzhao|howardwan|poshhuang|zhenhuahai>"
  }
}
```
如需看今日新增美术资源检查，再用 `bugs_get` 增加 `created": ">YYYY-MM-DD"` 和 `limit": 100`。

**策划组(重点人)**:
```json
{
  "tool_name": "bugs_get",
  "tool_args": {
    "workspace_id": "20453876",
    "status": "NOT_EQ<closed>",
    "current_owner": "USER_OR<lileozhang|trafalgarwu|jeffreysong|seanyxzhang>",
    "fields": "id,title,status,current_owner,created",
    "limit": 100
  }
}
```

### Step 3: 每日快报增量查询（用户说“今天的单子情况”时必做）

1. 先读取昨日工作日志 `/Users/a1_builder/WorkBuddy/tapd_agent/.workbuddy/memory/YYYY-MM-DD.md`，获取昨日未完成需求数和重点风险。
2. 当前未完成需求仍用 Step 1 查询，并额外用 `stories_count` 分别统计 `planning` / `developing`。
3. 今日新增Bug按 `created": ">YYYY-MM-DD"` 查询，至少分三批：客户端+服务器、策划重点人、完整美术组。注意美术资源检查可能很多，优先汇总数量和Top处理人。
4. 对比昨日：未完成需求净变化、新增/消失需求、状态变化(planning→developing)、due日期变化、今日新增功能Bug和资源检查。
5. Bug分组统计可用 `bugs_count`，但多人协作Bug会被多个分组重复计数，报告中必须注明“用于看人力负荷，不用于全局去重总数”。

### Step 4: 分析数据

对需求数据:
1. 区分父需求(无parent_id)和子需求(有parent_id)
2. 提取所有处理人，按人统计需求数
3. 识别超期需求(due < today且status != 完成状态)
4. 识别无处理人的需求
5. 按父需求维度聚合，列出主要进行中系统

对Bug数据:
1. 去重(多个查询可能有交叉)
2. 分类: AI CR / 美术资源检查 / 功能Bug（按标题关键词判断）
   - 含"AI CR"→ AI代码审查
   - 含"美术资源检查"→ 美术资源检查
   - 其他 → 功能Bug
3. 按处理人统计
4. 按分组汇总

### Step 5: 输出可视化报告

使用 `show_widget` 输出HTML可视化报告，包含:
- 4个指标卡: 未完成需求总数、规划中、实现中、未关闭Bug
- Bug按分组分布(客户端/美术/服务器/策划)
- Bug按人员分布柱状图(区分功能Bug vs AI CR/资源检查)
- 主要进行中系统列表(标注超期)
- 风险项总结

### Step 6: 标注风险

重点标注:
1. **超期需求**: due已过期但仍为planning/developing的父需求
2. **无处理人**: owner为空的子需求
3. **AI CR积压**: 单人超过5条AI CR未处理
4. **功能Bug积压**: 单人超过3条功能Bug

## A1分组信息

详见 MEMORY.md，核心分组:
- **策划(10人)**: averyliu, yiyangsun, careytseng, lydiachang, jeffreysong, seanyxzhang, tianyiqing, dorabdong, lileozhang, trafalgarwu
- **客户端(8人)**: arvinzhao, hugoyu, paradoxhe, oilyou, suiyuanpei, suijiwu, wisechen, liezhou
- **服务器(5人)**: jeffefang, externielin, jaykan, jianxingxu, jianmin
- **美术(24人)**: morganzhu, minghaoye, lusisdzheng, tinklezhang, jiajunjjhe, baronbei, allanshen, sunwushi, xiaobingxue, ninafu, weikou, zpennxiao, xiangwwang, yafeizhang, nichohuang, ticanma, zirongsun, curryhrxu, wallezzhang, zakiazhou, alongzhao, howardwan, poshhuang, zhenhuahai
- **运营(4人)**: morganyao, shirleyyao, lyonsun, shankshu

## 项目配置
- **workspace_id**: 20453876
- **需求标识**: 标题含 `【Maple_A1】`
- **Bug标识**: 处理人属于A1成员
- **未完成需求状态**: planning, developing
- **未关闭Bug**: status != closed

## 迭代记录
- v1.0 (2026-05-07): 初始版本，完成基本统计+可视化输出
