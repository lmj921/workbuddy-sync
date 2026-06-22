# TAPD 催单提醒 — 配置与扩展指南

## 快速上手

### 1. 新增项目

```bash
# 复制模板
cp config/_template.yaml config/你的项目名.yaml

# 编辑配置
# 填入 workspace_id、oauth_token、robot_key 等
```

### 2. 运行催单

```bash
# 进入工作区目录
cd /Users/a1_builder/WorkBuddy/Claw

# 正式执行
python ~/.workbuddy/skills/tapd-reminder/scripts/tapd_reminder.py \
  --config ~/.workbuddy/skills/tapd-reminder/config/maple.yaml

# 预演
python ~/.workbuddy/skills/tapd-reminder/scripts/tapd_reminder.py \
  --config ~/.workbuddy/skills/tapd-reminder/config/maple.yaml --dry-run

# 测试（全发给 PM）
python ~/.workbuddy/skills/tapd-reminder/scripts/tapd_reminder.py \
  --config ~/.workbuddy/skills/tapd-reminder/config/maple.yaml --test

# 只催 Bug
python ~/.workbuddy/skills/tapd-reminder/scripts/tapd_reminder.py \
  --config ~/.workbuddy/skills/tapd-reminder/config/maple.yaml --type bug
```

## 新增工作项类型（Bug / Task）

在项目配置的 `rules` 数组中追加即可：

```yaml
rules:
  - type: story
    # ... 已有配置 ...

  - type: bug                    # 新增 Bug 催单
    name_keyword: ""             # 不过滤标题
    skip_statuses:
      - "closed"
      - "rejected"
    status_map:
      new: "新建"
      in_progress: "处理中"
      resolved: "已解决"
      closed: "已关闭"
      rejected: "已拒绝"
    message_template:
      title: "🐛 {project_name} Bug 催单提醒"
      footer: "📌 请尽快修复超期 Bug"
```

## 配置字段参考

| 字段 | 必填 | 说明 |
|------|------|------|
| `project.name` | ✅ | 项目显示名称 |
| `project.workspace_id` | ✅ | TAPD 项目 ID |
| `tapd.mcp_url` | ❌ | MCP 地址，有默认值 |
| `tapd.oauth_token` | ✅ | TAPD 认证 Token |
| `tapd.username` | ✅ | TAPD 用户名 |
| `wechat.robot_key` | ✅ | 企微机器人 Key |
| `wechat.pm_id` | ✅ | PM 企微 ID |
| `rules[].type` | ✅ | story / bug / task |
| `rules[].name_keyword` | ❌ | 标题模糊匹配关键词 |
| `rules[].skip_statuses` | ❌ | 不催单的状态列表 |
| `rules[].status_map` | ❌ | 状态 ID → 中文映射 |
| `rules[].message_template` | ❌ | 自定义消息模板 |
| `log.dir` | ❌ | 日志目录，默认 tapd_reminder_log |

## 注意事项

- **敏感信息**：`oauth_token` 和 `robot_key` 是敏感信息，不要提交到公开仓库
- **企微限频**：Webhook 有频率限制，脚本内置 5 秒间隔 + 自动重试
- **状态 ID**：不同项目的自定义状态 ID 不同，需要在 TAPD 后台查看
- **Bug 的处理人字段**：Bug 使用 `current_owner`，Story/Task 使用 `owner`，脚本已自动处理
