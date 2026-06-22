---
name: tapd-reminder
description: >
  TAPD 催单提醒工具。自动从 TAPD 拉取超期的 Story/Bug/Task，
  通过企微 Webhook 通知处理人。支持多项目、多工作项类型、可配置筛选规则。
  触发词：催单、提醒、tapd提醒、tapd催单、催一下、超期提醒、
  到期提醒、story催单、bug催单、task催单、发催单、跟进提醒、
  催进度、tapd reminder、overdue reminder。
---

# TAPD 催单提醒 Skill

你是一个 TAPD 项目管理催单助手。根据用户指令，从 TAPD 拉取超期工作项（Story/Bug/Task），
通过企微 Webhook 私聊通知对应处理人，并生成执行报告。

## 目录结构

```
tapd-reminder/
├── SKILL.md              # 本文件 — Skill 定义与工作流
├── scripts/
│   └── tapd_reminder.py  # 核心催单脚本（通用，不含项目配置）
├── config/
│   ├── _template.yaml    # 配置模板（新项目复制此文件）
│   └── maple.yaml        # Maple 项目配置（示例）
└── references/
    └── README.md         # 配置说明与扩展指南
```

## 配置文件格式

每个项目一个 YAML 配置文件，放在 `config/` 目录下。新增项目只需复制 `_template.yaml` 并修改。

### 配置文件字段说明

```yaml
# 项目基本信息
project:
  name: "项目显示名称"
  workspace_id: "TAPD 项目 ID"

# TAPD 连接配置
tapd:
  mcp_url: "http://mcp-idc.tapd.woa.com/mcp/"
  oauth_token: "你的 TAPD OAUTH-TOKEN"
  username: "你的 TAPD 用户名"

# 企微通知配置
wechat:
  robot_key: "企微机器人 Webhook Key"
  pm_id: "PM 的企微 ID（接收汇总报告 + 测试模式收件人）"

# 催单规则（可配置多个工作项类型）
rules:
  - type: story                    # 工作项类型: story / bug / task
    name_keyword: "maple_A1"       # 标题关键词（模糊匹配，留空则不过滤）
    skip_statuses:                 # 这些状态不催单
      - "status_5"                 # 待验收
      - "status_7"                 # 验收通过
      - "status_10"                # 无需测试
      - "resolved"                 # 已完成
      - "rejected"                 # 已拒绝
    status_map:                    # 状态 ID → 中文映射
      planning: "规划中"
      developing: "实现中"
      resolved: "已完成"
      rejected: "已拒绝"
      status_5: "待验收"
      status_7: "验收通过"
      status_8: "测试中"
      status_9: "挂起"
      status_10: "无需测试"
      status_12: "暂时无法测试"
    message_template:              # 消息模板（可选，有默认值）
      title: "⏰ {project_name} Story 催单提醒"
      footer: |
        📌 **状态操作说明：**
        > 1. 正在做的 → 请转到「**实现中**」
        > 2. 已完成的 → 请转到「**待验收**」并备注"无须测试"

# 日志配置
log:
  dir: "tapd_reminder_log"         # 日志保存目录（相对于工作区根目录）
  format: "{date}_{time}.md"       # 日志文件名格式
```

## 工作流程

### 用户说"催一下 XX 项目的单" 时

1. **确认项目** — 根据用户提到的项目名，在 `config/` 下找对应的 YAML 配置
2. **确认范围** — 默认催全部已配置的 rules（Story + Bug + ...），用户可指定只催某类
3. **确认模式** — 默认正式执行，用户可要求 `--dry-run`（预演）或 `--test`（全发给 PM）
4. **执行脚本** — 运行 `scripts/tapd_reminder.py --config config/xxx.yaml [--dry-run|--test]`
5. **报告结果** — 展示执行摘要（催了几人、几条、成功/失败）

### 新增项目时

1. 复制 `config/_template.yaml` 为 `config/新项目名.yaml`
2. 填入项目的 workspace_id、关键词、状态配置
3. 完成，即可使用

### 新增工作项类型时

在项目配置的 `rules` 数组中追加一个新的 rule 块即可。每个 rule 对应一种工作项类型（story/bug/task）。

## 脚本用法

```bash
# 正式执行（发给每个处理人）
python scripts/tapd_reminder.py --config config/maple.yaml

# 预演模式（只输出，不发消息）
python scripts/tapd_reminder.py --config config/maple.yaml --dry-run

# 测试模式（所有消息只发给 PM）
python scripts/tapd_reminder.py --config config/maple.yaml --test

# 只催 story
python scripts/tapd_reminder.py --config config/maple.yaml --type story

# 只催 bug
python scripts/tapd_reminder.py --config config/maple.yaml --type bug
```

## 注意事项

- 企微 Webhook 有频率限制，脚本内置 5 秒间隔 + 限频重试（指数退避）
- TAPD MCP 分页上限 200，脚本自动翻页获取全量数据
- 日志保存在工作区的 `tapd_reminder_log/` 目录，方便追溯
- 配置文件中的 `oauth_token` 属于敏感信息，请勿提交到公开仓库
