# -*- coding: utf-8 -*-
"""
TAPD 通用催单脚本
从 YAML 配置文件读取项目信息，拉取超期工作项（Story/Bug/Task），
通过企微 Webhook 通知处理人。

用法:
  python tapd_reminder.py --config CONFIG_PATH [--dry-run] [--test] [--type TYPE]

参数:
  --config  配置文件路径（必须）
  --dry-run 预演模式，只输出不发消息
  --test    测试模式，所有消息只发给 PM
  --type    只催指定类型（story/bug/task），不传则催全部已配置类型
"""

import argparse
import json
import os
import re
import requests
import sys
import time
import yaml
from datetime import datetime, date
from collections import defaultdict


# ============ 配置加载 ============


def load_config(config_path):
    """加载 YAML 配置文件"""
    if not os.path.isfile(config_path):
        print(f"❌ 配置文件不存在: {config_path}")
        sys.exit(1)

    with open(config_path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    # 校验必填字段
    required_keys = {
        "project.name": lambda c: c.get("project", {}).get("name"),
        "project.workspace_id": lambda c: c.get("project", {}).get("workspace_id"),
        "tapd.oauth_token": lambda c: c.get("tapd", {}).get("oauth_token"),
        "tapd.username": lambda c: c.get("tapd", {}).get("username"),
        "wechat.robot_key": lambda c: c.get("wechat", {}).get("robot_key"),
        "wechat.pm_id": lambda c: c.get("wechat", {}).get("pm_id"),
    }

    missing = [key for key, getter in required_keys.items() if not getter(config)]
    if missing:
        print(f"❌ 配置文件缺少必填字段: {', '.join(missing)}")
        sys.exit(1)

    return config


# ============ TAPD 数据拉取 ============


def build_tapd_headers(config):
    """构建 TAPD MCP 请求头"""
    tapd = config["tapd"]
    return {
        "OAUTH-TOKEN": tapd["oauth_token"],
        "X-USERNAME": tapd["username"],
        "X-Tools-Set": "lookup_tapd_tool,lookup_tool_param_schema,proxy_execute_tool",
        "X-Keep-Links": "true",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }


def get_tapd_tool_name(item_type):
    """根据工作项类型返回对应的 TAPD MCP 工具名"""
    tool_map = {
        "story": "stories_get",
        "bug": "bugs_get",
        "task": "tasks_get",
    }
    return tool_map.get(item_type)


def get_tapd_detail_url(workspace_id, item_type, item_id):
    """构建 TAPD 详情页 URL"""
    type_path = {
        "story": "story",
        "bug": "bugtrace",
        "task": "task",
    }
    path = type_path.get(item_type, item_type)
    return f"https://tapd.woa.com/tapd_fe/{workspace_id}/{path}/detail/{item_id}"


def get_due_field(item_type):
    """不同工作项类型的截止日期字段名"""
    # Story 和 Task 用 due，Bug 用 due
    return "due"


def get_owner_field(item_type):
    """不同工作项类型的处理人字段名"""
    owner_map = {
        "story": "owner",
        "bug": "current_owner",
        "task": "owner",
    }
    return owner_map.get(item_type, "owner")


def get_fields_for_type(item_type):
    """返回每种类型需要拉取的字段"""
    base_fields = "id,name,status,due,created"
    owner_field = get_owner_field(item_type)
    if owner_field != "owner" and owner_field not in base_fields:
        return f"{base_fields},{owner_field}"
    # 确保 owner 字段在列表中
    if "owner" not in base_fields and item_type in ("story", "task"):
        return f"{base_fields},owner"
    return base_fields if "owner" in base_fields else f"{base_fields},owner"


def fetch_items(config, rule):
    """
    通过 TAPD MCP 拉取指定类型的工作项（分页获取全量）
    """
    item_type = rule["type"]
    tool_name = get_tapd_tool_name(item_type)
    if not tool_name:
        print(f"  ❌ 不支持的工作项类型: {item_type}")
        return []

    tapd = config["tapd"]
    mcp_url = tapd.get("mcp_url", "http://mcp-idc.tapd.woa.com/mcp/")
    headers = build_tapd_headers(config)
    workspace_id = config["project"]["workspace_id"]

    all_items = []
    page = 1
    limit = 200

    while True:
        tool_args = {
            "workspace_id": workspace_id,
            "with_v_status": "1",
            "fields": get_fields_for_type(item_type),
            "limit": limit,
            "page": page,
        }

        # 如果有关键词筛选
        name_keyword = rule.get("name_keyword", "")
        if name_keyword:
            tool_args["name"] = name_keyword

        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/call",
            "params": {
                "name": "proxy_execute_tool",
                "arguments": {
                    "tool_name": tool_name,
                    "tool_args": tool_args,
                },
            },
        }

        try:
            resp = requests.post(mcp_url, json=payload, headers=headers, timeout=60)
            result = resp.json()

            if "result" in result and "content" in result["result"]:
                content = result["result"]["content"]
                if content and len(content) > 0:
                    raw_text = content[0].get("text", "{}")
                    # MCP 响应末尾可能带 [TAPD-REQUEST-ID: xxx]，去掉再解析
                    raw_text = re.sub(r'\s*\[TAPD-REQUEST-ID:.*?\]\s*$', '', raw_text)
                    data = json.loads(raw_text)
                    items = data.get("data", [])
                    all_items.extend(items)

                    total = data.get("count", 0)
                    print(f"  第 {page} 页: 获取 {len(items)} 条, 总计 {total} 条")

                    if len(all_items) >= total or len(items) < limit:
                        break
                    page += 1
                else:
                    break
            else:
                error_msg = result.get("error", {}).get("message", str(result))
                print(f"  MCP 响应异常: {error_msg}")
                break
        except Exception as e:
            print(f"  MCP 请求失败: {e}")
            break

    return all_items


# ============ 筛选逻辑 ============


def filter_overdue_items(items, rule):
    """
    筛选需要催单的工作项：
    1. 截止日期(due) ≤ 今天
    2. 状态不在跳过列表中
    """
    today = date.today()
    skip_statuses = set(rule.get("skip_statuses", []))
    status_map = rule.get("status_map", {})
    item_type = rule["type"]
    due_field = get_due_field(item_type)
    owner_field = get_owner_field(item_type)
    overdue = []

    for item in items:
        due_str = item.get(due_field, "")
        status = item.get("status", "")

        # 跳过指定状态
        if status in skip_statuses:
            continue

        # 跳过没有截止日期的
        if not due_str or due_str == "0000-00-00":
            continue

        try:
            due_date = datetime.strptime(due_str, "%Y-%m-%d").date()
        except ValueError:
            continue

        # 截止日期 ≤ 今天 → 需要催
        if due_date <= today:
            overdue_days = (today - due_date).days
            item["overdue_days"] = overdue_days
            item["due_date"] = due_date
            item["status_cn"] = status_map.get(status, status)
            item["_type"] = item_type
            item["_owner_field"] = owner_field
            overdue.append(item)

    return overdue


# ============ 企微通知 ============


def build_message_content(config, rule, owner_id, items):
    """构建催单消息内容"""
    project_name = config["project"]["name"]
    workspace_id = config["project"]["workspace_id"]
    item_type = rule["type"]
    type_cn = {"story": "Story", "bug": "Bug", "task": "Task"}.get(item_type, item_type)

    # 消息标题
    msg_template = rule.get("message_template", {})
    title = msg_template.get("title", f"⏰ {project_name} {type_cn} 催单提醒")
    title = title.replace("{project_name}", project_name).replace("{type}", type_cn)

    content = f'# <font color="#ff5656">{title}</font>\n'
    content += f'> <font color="comment">处理人:</font> {owner_id}\n'
    content += f'> 你有 **{len(items)}** 条 {type_cn} 已到/超过预计结束日期，请尽快处理：\n\n'

    for i, item in enumerate(items, 1):
        name = item.get("name", "未知")
        status_cn = item.get("status_cn", "未知")
        overdue_days = item.get("overdue_days", 0)
        due_str = item.get("due", "")
        item_id = item.get("id", "")
        detail_link = get_tapd_detail_url(workspace_id, item_type, item_id)

        if overdue_days == 0:
            overdue_text = "今天到期"
        else:
            overdue_text = f'<font color="warning">超期 {overdue_days} 天</font>'

        content += f'{i}. [{name}]({detail_link})\n'
        content += f'   状态: **{status_cn}** | 截止: {due_str} | {overdue_text}\n\n'

    # 页脚
    footer = msg_template.get("footer", "")
    if footer:
        content += f'\n---\n{footer}'

    content += f'\n_催单时间: {datetime.now().strftime("%Y-%m-%d %H:%M")}_'
    return content


def send_wechat_message(config, rule, owner_id, items, test_mode=False, max_retries=3):
    """
    给指定处理人发企微私聊催单消息，带重试机制。
    """
    wechat = config["wechat"]
    robot_key = wechat["robot_key"]
    pm_id = wechat["pm_id"]
    webhook_url = f"https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key={robot_key}&debug=1"

    content = build_message_content(config, rule, owner_id, items)

    # 测试模式：所有消息发给 PM 自己
    # 正式模式：催单消息只发给处理人本人（不再拉 PM 进对话）
    if test_mode:
        chatid = pm_id
    else:
        chatid = owner_id

    json_data = {
        "chatid": chatid,
        "msgtype": "markdown",
        "markdown": {
            "content": content,
            "at_short_name": True,
            "attachments": [{
                "callback_id": "tapd_reminder",
                "actions": [{
                    "name": "btn_ack",
                    "text": "收到，马上处理",
                    "type": "button",
                    "value": "ack",
                    "replace_text": "✅ 已确认",
                    "border_color": "#2EAB49",
                    "text_color": "#2EAB49"
                }]
            }]
        },
    }

    target = f"→ {pm_id}(测试)" if test_mode else f"→ {chatid}"
    last_error = None

    for attempt in range(1, max_retries + 1):
        try:
            resp = requests.post(webhook_url, json=json_data, timeout=10)
            result = resp.json()
            errcode = result.get("errcode", -1)

            if errcode == 0:
                print(f"  ✅ 已通知 {owner_id}（{len(items)} 条）{target}")
                return True
            elif errcode == 45009:
                wait = 5 * (2 ** (attempt - 1))
                print(f"  ⏳ {owner_id} 限频，{wait}s 后重试（{attempt}/{max_retries}）")
                time.sleep(wait)
                last_error = "限频(45009)"
            else:
                print(f"  ❌ 通知 {owner_id} 失败: {result}")
                return False
        except (requests.exceptions.Timeout, requests.exceptions.ConnectionError) as e:
            wait = 5 * (2 ** (attempt - 1))
            print(f"  ⏳ {owner_id} 网络异常({e.__class__.__name__})，{wait}s 后重试（{attempt}/{max_retries}）")
            time.sleep(wait)
            last_error = f"网络异常({e.__class__.__name__})"
        except Exception as e:
            print(f"  ❌ 通知 {owner_id} 异常: {e}")
            return False

    print(f"  ❌ 通知 {owner_id} 最终失败（重试 {max_retries} 次）: {last_error}")
    return False


def send_summary_to_pm(config, total, success, fail, failed_items):
    """执行完成后给 PM 发一条汇总消息"""
    wechat = config["wechat"]
    robot_key = wechat["robot_key"]
    pm_id = wechat["pm_id"]
    project_name = config["project"]["name"]
    workspace_id = config["project"]["workspace_id"]
    webhook_url = f"https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key={robot_key}&debug=1"

    if fail == 0:
        status_text = '<font color="info">全部成功 ✅</font>'
    else:
        status_text = '<font color="warning">部分失败 ⚠️</font>'

    content = f'# 📊 {project_name} 催单执行报告\n'
    content += f'> 时间: {datetime.now().strftime("%Y-%m-%d %H:%M")}\n\n'
    content += f'- 总通知人数: **{total}**\n'
    content += f'- 发送成功: **{success}**\n'
    content += f'- 发送失败: **{fail}**\n'
    content += f'- 状态: {status_text}\n'

    if failed_items:
        content += f'\n**未送达 → 请手动跟进：**\n'
        for owner, items in failed_items:
            content += f'\n👤 **{owner}**（{len(items)} 条）：\n'
            for item in items:
                item_id = item.get("id", "")
                name = item.get("name", "未知")
                status_cn = item.get("status_cn", "未知")
                item_type = item.get("_type", "story")
                detail_link = get_tapd_detail_url(workspace_id, item_type, item_id)
                content += f'- [{name}]({detail_link}) | {status_cn}\n'

    json_data = {
        "chatid": pm_id,
        "msgtype": "markdown",
        "markdown": {"content": content},
    }

    try:
        resp = requests.post(webhook_url, json=json_data, timeout=10)
        result = resp.json()
        if result.get("errcode") == 0:
            print(f"  ✅ 执行报告已发送给 PM")
        else:
            print(f"  ❌ 执行报告发送失败: {result}")
    except Exception as e:
        print(f"  ❌ 执行报告发送异常: {e}")


# ============ 日志 ============


def save_report_log(config, by_owner, total, success, fail, failed_items, all_overdue, test_mode=False):
    """
    保存执行报告为本地 Markdown 日志。
    每天一个文件（按日期命名），同一天多次执行追加到同一文件中。
    """
    log_config = config.get("log", {})
    log_dir_name = log_config.get("dir", "tapd_reminder_log")
    project_name = config["project"]["name"]
    workspace_id = config["project"]["workspace_id"]

    log_dir = os.path.join(os.getcwd(), log_dir_name)
    os.makedirs(log_dir, exist_ok=True)

    now = datetime.now()
    # 按天命名，同一天的多次执行合并到一个文件
    filename = now.strftime("%Y-%m-%d") + f"_{project_name}.md"
    filepath = os.path.join(log_dir, filename)

    mode_str = "测试模式" if test_mode else "正式执行"
    status_emoji = "✅ 全部成功" if fail == 0 else "⚠️ 部分失败"

    # 判断是否为当天第一次执行（文件不存在 → 写文件头）
    is_first_run = not os.path.isfile(filepath)

    lines = []

    if is_first_run:
        # 第一次执行：写文件头
        lines.extend([
            f"# {project_name} 催单执行报告 — {now.strftime('%Y-%m-%d')}",
            "",
        ])

    # 每次执行都追加一个带时间戳的 section
    run_label = now.strftime('%H:%M:%S')
    lines.extend([
        f"---",
        "",
        f"## 🕐 {run_label} 执行",
        "",
        f"- **时间**: {now.strftime('%Y-%m-%d %H:%M:%S')}",
        f"- **项目**: {project_name} (workspace: {workspace_id})",
        f"- **模式**: {mode_str}",
        f"- **超期工作项**: {len(all_overdue)} 条",
        f"- **涉及处理人**: {total} 人",
        f"- **发送成功**: {success}",
        f"- **发送失败**: {fail}",
        f"- **状态**: {status_emoji}",
        "",
    ])

    # 按类型统计
    type_counts = defaultdict(int)
    for item in all_overdue:
        type_counts[item.get("_type", "unknown")] += 1
    if type_counts:
        lines.append("### 按类型统计")
        lines.append("")
        for t, c in sorted(type_counts.items()):
            type_cn = {"story": "Story", "bug": "Bug", "task": "Task"}.get(t, t)
            lines.append(f"- {type_cn}: {c} 条")
        lines.append("")

    # 成功的处理人
    lines.append(f"### 已通知（{success} 人）")
    lines.append("")
    failed_owners = {fo for fo, _ in failed_items}
    for owner, items in sorted(by_owner.items()):
        if owner in failed_owners:
            continue
        lines.append(f"#### {owner}（{len(items)} 条）")
        lines.append("")
        lines.append("| # | 类型 | 工作项 | 状态 | 截止日期 | 超期 |")
        lines.append("|---|------|--------|------|----------|------|")
        for i, item in enumerate(items, 1):
            item_id = item.get("id", "")
            name = item.get("name", "未知")
            status_cn = item.get("status_cn", "未知")
            due_str = item.get("due", "")
            overdue_days = item.get("overdue_days", 0)
            item_type = item.get("_type", "story")
            type_cn = {"story": "Story", "bug": "Bug", "task": "Task"}.get(item_type, item_type)
            link = get_tapd_detail_url(workspace_id, item_type, item_id)
            overdue_text = "今天到期" if overdue_days == 0 else f"{overdue_days} 天"
            lines.append(f"| {i} | {type_cn} | [{name}]({link}) | {status_cn} | {due_str} | {overdue_text} |")
        lines.append("")

    # 失败的处理人
    if failed_items:
        lines.append(f"### ❌ 未送达（{fail} 人）— 需手动跟进")
        lines.append("")
        for owner, items in failed_items:
            lines.append(f"#### {owner}（{len(items)} 条）")
            lines.append("")
            lines.append("| # | 类型 | 工作项 | 状态 | 截止日期 | 超期 |")
            lines.append("|---|------|--------|------|----------|------|")
            for i, item in enumerate(items, 1):
                item_id = item.get("id", "")
                name = item.get("name", "未知")
                status_cn = item.get("status_cn", "未知")
                due_str = item.get("due", "")
                overdue_days = item.get("overdue_days", 0)
                item_type = item.get("_type", "story")
                type_cn = {"story": "Story", "bug": "Bug", "task": "Task"}.get(item_type, item_type)
                link = get_tapd_detail_url(workspace_id, item_type, item_id)
                overdue_text = "今天到期" if overdue_days == 0 else f"{overdue_days} 天"
                lines.append(f"| {i} | {type_cn} | [{name}]({link}) | {status_cn} | {due_str} | {overdue_text} |")
            lines.append("")

    # 追加写入（不覆盖已有内容）
    write_mode = "w" if is_first_run else "a"
    with open(filepath, write_mode, encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")

    run_order = "首次" if is_first_run else "追加"
    print(f"  📝 日志已保存（{run_order}）: {filepath}")
    return filepath


# ============ 主流程 ============


def run_rule(config, rule, dry_run=False, test_mode=False):
    """执行单条催单规则，返回 (by_owner, overdue_items)"""
    item_type = rule["type"]
    type_cn = {"story": "Story", "bug": "Bug", "task": "Task"}.get(item_type, item_type)
    project_name = config["project"]["name"]
    owner_field = get_owner_field(item_type)

    print(f"\n{'─' * 40}")
    print(f"📋 [{project_name}] 处理 {type_cn}...")

    # 拉数据
    print(f"\n📥 从 TAPD 拉取 {type_cn}...")
    items = fetch_items(config, rule)
    if not items:
        print(f"  未获取到任何 {type_cn}")
        return {}, []

    print(f"  共获取 {len(items)} 条 {type_cn}")

    # 筛选
    print(f"\n🔍 筛选超期 {type_cn}...")
    overdue = filter_overdue_items(items, rule)
    print(f"  共 {len(overdue)} 条需要催单")

    if not overdue:
        print(f"  🎉 没有需要催的 {type_cn}！")
        return {}, []

    # 按处理人分组
    by_owner = defaultdict(list)
    for item in overdue:
        owners_str = item.get(owner_field, "") or item.get("owner", "")
        owners = owners_str.strip(";").split(";")
        for owner in owners:
            owner = owner.strip()
            if owner:
                by_owner[owner].append(item)

    print(f"  涉及 {len(by_owner)} 个处理人")
    return dict(by_owner), overdue


def main():
    parser = argparse.ArgumentParser(description="TAPD 通用催单脚本")
    parser.add_argument("--config", required=True, help="配置文件路径")
    parser.add_argument("--dry-run", action="store_true", help="预演模式，不发消息")
    parser.add_argument("--test", action="store_true", help="测试模式，全发给 PM")
    parser.add_argument("--type", help="只催指定类型（story/bug/task）")
    args = parser.parse_args()

    config = load_config(args.config)
    project_name = config["project"]["name"]
    rules = config.get("rules", [])

    # 如果指定了类型，只执行对应的 rule
    if args.type:
        rules = [r for r in rules if r["type"] == args.type]
        if not rules:
            print(f"❌ 配置中没有类型为 '{args.type}' 的催单规则")
            sys.exit(1)

    mode_str = "预演(不发消息)" if args.dry_run else ("测试(全发给PM)" if args.test else "正式执行")

    print("=" * 50)
    print(f"TAPD 催单 — {project_name}")
    print(f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"模式: {mode_str}")
    print(f"规则: {len(rules)} 条 ({', '.join(r['type'] for r in rules)})")
    print("=" * 50)

    # 执行所有规则，合并结果
    all_by_owner = defaultdict(list)
    all_overdue = []

    for rule in rules:
        by_owner, overdue = run_rule(config, rule, dry_run=args.dry_run, test_mode=args.test)
        all_overdue.extend(overdue)
        for owner, items in by_owner.items():
            all_by_owner[owner].extend(items)

    if not all_overdue:
        print(f"\n🎉 {project_name} 没有需要催的单子，收工！")
        return

    # 发通知
    print(f"\n📨 发送企微催单通知...")
    if args.dry_run:
        print("  [预演模式] 以下是将要发送的催单：")
        for owner, items in sorted(all_by_owner.items()):
            print(f"\n  👤 {owner}（{len(items)} 条）：")
            for item in items:
                type_cn = {"story": "Story", "bug": "Bug", "task": "Task"}.get(item.get("_type", ""), "?")
                print(
                    f"     - [{type_cn}] {item['name']} | {item['status_cn']} | "
                    f"截止 {item['due']} | 超期 {item['overdue_days']} 天"
                )
    else:
        success = 0
        fail = 0
        failed_items = []

        # 按处理人发送（每个处理人一条消息，包含所有类型的超期项）
        # 需要按 rule 分组发送，因为消息模板不同
        # 策略：按 (owner, type) 发送
        owner_type_map = defaultdict(lambda: defaultdict(list))
        for owner, items in all_by_owner.items():
            for item in items:
                owner_type_map[owner][item["_type"]].append(item)

        owners_list = sorted(owner_type_map.items())
        rules_by_type = {r["type"]: r for r in config.get("rules", [])}

        for idx, (owner, type_items) in enumerate(owners_list):
            owner_success = True
            for item_type, items in type_items.items():
                rule = rules_by_type.get(item_type, rules[0])
                if not send_wechat_message(config, rule, owner, items, test_mode=args.test):
                    owner_success = False
                    failed_items.append((owner, items))
                # 间隔避免限频
                time.sleep(3)

            if owner_success:
                success += 1
            else:
                fail += 1

            # 人与人之间间隔
            if idx < len(owners_list) - 1:
                time.sleep(5)

        print(f"\n📊 发送结果: 成功 {success}, 失败 {fail}")

        # 给 PM 发执行汇总
        if success + fail > 0:
            time.sleep(5)
            send_summary_to_pm(
                config=config,
                total=len(owners_list),
                success=success,
                fail=fail,
                failed_items=failed_items,
            )

        # 保存本地日志
        save_report_log(
            config=config,
            by_owner=dict(all_by_owner),
            total=len(owners_list),
            success=success,
            fail=fail,
            failed_items=failed_items,
            all_overdue=all_overdue,
            test_mode=args.test,
        )

    print(f"\n✅ {project_name} 催单完成！")


if __name__ == "__main__":
    main()
