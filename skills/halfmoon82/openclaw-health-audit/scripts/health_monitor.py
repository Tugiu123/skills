#!/usr/bin/env python3
"""
health_monitor.py — openclaw-health-audit skill
版本: 1.0.0 (2026-03-05)

用法:
  python3 health_monitor.py --report       # 生成报告，输出到 stdout（供 agent 发送 Telegram）
  python3 health_monitor.py --dry-run      # 同 --report，标注 [DRY RUN]
  python3 health_monitor.py --fix "1,3"   # 执行第 1、3 项问题的修复
  python3 health_monitor.py --fix all     # 执行全部修复
  python3 health_monitor.py --list-fixes   # 列出所有可执行的修复命令（不执行）
  python3 health_monitor.py --setup        # 运行安装向导生成 config.json

监控范围（由 config.json 控制）：
  A. System Prompt 体积漂移（Layer 1）
  B. Cron Job 合规性（Layer 2）
  C. 孤儿 Session 检测（Layer 2）
  D. Token 消耗趋势（Layer 3，参考）
  E. 缓存配置完整性（Layer 2，可选，需要 semantic-router M1/M3 补丁）
"""

import json
import os
import re
import sys
import time
import subprocess
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

# ─── 路径常量 ────────────────────────────────────────────────────────────────

SKILL_DIR = Path(__file__).parent.parent
CONFIG_FILE = SKILL_DIR / 'config' / 'config.json'
BASE = Path.home() / '.openclaw'
WORKSPACE = BASE / 'workspace'
AGENTS_DIR = BASE / 'agents'
CRON_JOBS = BASE / 'cron' / 'jobs.json'
SESSION_STATE = WORKSPACE / '.lib' / 'session_model_state.json'
REPORT_FILE = SKILL_DIR / 'health_report_latest.md'

# ─── 配置加载 ────────────────────────────────────────────────────────────────

def load_config() -> dict:
    if not CONFIG_FILE.exists():
        print(f"⚠️  配置文件不存在：{CONFIG_FILE}")
        print("请先运行安装向导：python3 scripts/audit_wizard.py")
        print("或手动复制 config/config.template.json 为 config/config.json 并调整阈值。")
        sys.exit(1)
    with open(CONFIG_FILE) as f:
        return json.load(f)

# ─── 数据结构 ────────────────────────────────────────────────────────────────

@dataclass
class Issue:
    idx: int
    category: str
    severity: str       # warn / alert
    title: str
    detail: str
    fix_cmd: Optional[str] = None
    fix_description: Optional[str] = None

# ─── 监控检查 ────────────────────────────────────────────────────────────────

def check_prompt_drift(cfg: dict) -> list[Issue]:
    """A: 检查主 workspace 和子代理 SOUL.md 体积漂移"""
    issues = []

    # 主 workspace 文件
    for filename, thresholds in cfg.get('prompt_files', {}).items():
        if filename.startswith('_'):
            continue
        path = WORKSPACE / filename
        if not path.exists():
            continue
        size = path.stat().st_size
        warn, alert = thresholds['warn'], thresholds['alert']
        if size > alert:
            sev = 'alert'
        elif size > warn:
            sev = 'warn'
        else:
            continue
        issues.append(Issue(
            idx=0, category='A', severity=sev,
            title=f'{filename} 体积漂移: {size // 1024}KB ({size}B)',
            detail=f'阈值: warn={warn // 1024}KB, alert={alert // 1024}KB\n'
                   f'原因: 可能有新内容被写入常驻 prompt\n'
                   f'建议: 将超出部分移至 memory/LESSONS/ 或对应 Skill 文件',
            fix_description=f'手动审查 {filename}，将非核心内容移至 memory/LESSONS/lessons.md',
        ))

    # 子代理 SOUL.md
    subagents = cfg.get('subagents', {}).get('list', [])
    soul_thresholds = cfg.get('subagent_soul', {'warn': 3072, 'alert': 4096})
    oversized = []
    for agent in subagents:
        soul_path = AGENTS_DIR / agent / 'workspace' / 'SOUL.md'
        if not soul_path.exists():
            continue
        size = soul_path.stat().st_size
        warn = soul_thresholds['warn']
        alert = soul_thresholds['alert']
        if size > alert:
            oversized.append((agent, size, 'alert'))
        elif size > warn:
            oversized.append((agent, size, 'warn'))

    if oversized:
        names = ', '.join(f'{a}({s}B)' for a, s, _ in oversized)
        max_sev = 'alert' if any(s == 'alert' for _, _, s in oversized) else 'warn'
        issues.append(Issue(
            idx=0, category='A', severity=max_sev,
            title=f'子代理 SOUL.md 超限: {len(oversized)} 个',
            detail=f'超限代理: {names}\n'
                   f'阈值: warn={soul_thresholds["warn"]}B, alert={soul_thresholds["alert"]}B\n'
                   f'建议: 删除 SOUL.md 中的模型配置表、历史教训等非核心内容',
            fix_description='删除各子代理 SOUL.md 中的 Model Fallback Order 表和历史教训',
        ))

    return issues


def check_cron_jobs(cfg: dict) -> list[Issue]:
    """B: 检查 Cron Job 合规性"""
    issues = []
    if not CRON_JOBS.exists():
        return issues

    with open(CRON_JOBS) as f:
        jobs_data = json.load(f)

    jobs = jobs_data if isinstance(jobs_data, list) else jobs_data.get('jobs', list(jobs_data.values()))
    expensive_models = set(cfg.get('expensive_models', {}).get('list', [
        'claude-opus', 'claude-opus-4', 'opus-4.6', 'opus-4-5'
    ]))

    violations = []
    for job in jobs:
        if job.get('status') == 'disabled':
            continue
        payload = job.get('payload', {})
        if payload.get('kind') != 'agentTurn':
            continue

        jid = job.get('id', 'unknown')
        name = job.get('name', jid)[:50]
        problems = []

        if job.get('sessionKey') is not None:
            problems.append('sessionKey 非 null（污染主会话）')
        if 'timeoutSeconds' not in payload:
            problems.append('缺少 timeoutSeconds（可能挂起）')
        model = payload.get('model', '')
        if any(em in model.lower() for em in expensive_models):
            problems.append(f'使用高成本模型: {model}')

        if problems:
            violations.append((jid, name, problems))

    if violations:
        detail_lines = [f'- [{jid[:8]}...] {name}: {", ".join(problems)}'
                        for jid, name, problems in violations]
        issues.append(Issue(
            idx=0, category='B', severity='alert' if len(violations) > 2 else 'warn',
            title=f'Cron Job 违规: {len(violations)} 个',
            detail='\n'.join(detail_lines) + '\n建议: 设置 sessionKey=null, timeoutSeconds≤120, 使用低成本模型',
            fix_description=f'修复 {len(violations)} 个违规 Job: sessionKey=null, timeoutSeconds=120',
        ))

    return issues


def check_orphan_sessions(cfg: dict) -> list[Issue]:
    """C: 检查孤儿 Session（超过 N 天无活动的 cron session）"""
    issues = []
    if not SESSION_STATE.exists():
        return issues

    stale_days = cfg.get('session_stale_days', 7)

    with open(SESSION_STATE) as f:
        sessions = json.load(f)

    now_ms = int(time.time() * 1000)
    stale_ms = stale_days * 24 * 3600 * 1000

    stale = []
    for key, state in sessions.items():
        ts = state.get('lastPatchedAt', state.get('updatedAt', 0))
        if ts and (now_ms - ts) > stale_ms:
            age_days = (now_ms - ts) / (24 * 3600 * 1000)
            stale.append((key, age_days))

    if stale:
        names = '\n'.join(f'- {k[:60]} ({d:.1f}天前)' for k, d in stale)
        issues.append(Issue(
            idx=0, category='C', severity='warn',
            title=f'过期 Session: {len(stale)} 个（>{stale_days}天无活动）',
            detail=names + f'\n建议: 从 session_model_state.json 清除这些 key',
            fix_description=f'清除 {len(stale)} 个过期 session key',
        ))

    return issues


def check_token_trend(cfg: dict) -> list[Issue]:
    """D: 检查 Token 消耗趋势"""
    issues = []
    thresholds = cfg.get('token_thresholds', {'warn': 30_000_000, 'alert': 60_000_000})

    try:
        result = subprocess.run(
            ['openclaw', 'gateway', 'usage-cost', '--json', '--days', '2'],
            capture_output=True, text=True, timeout=15
        )
        if result.returncode == 0:
            data = json.loads(result.stdout)
            daily = data.get('daily', [])
            for day_data in daily:
                date = day_data.get('date', '')
                total = day_data.get('totalTokens', 0)
                cost = day_data.get('totalCost', 0)
                if total > thresholds['alert']:
                    sev = 'alert'
                    icon = '🔴'
                elif total > thresholds['warn']:
                    sev = 'warn'
                    icon = '🟡'
                else:
                    continue
                issues.append(Issue(
                    idx=0, category='D', severity=sev,
                    title=f'{icon} Token 消耗异常 {date}: {total / 1_000_000:.1f}M tokens / ${cost:.2f}',
                    detail=f'阈值: warn={thresholds["warn"] // 1_000_000}M, alert={thresholds["alert"] // 1_000_000}M\n'
                           f'建议: 检查是否有失控的 cron job 或长会话未压缩',
                    fix_description='检查 cron job 模型配置，使用 /compact 压缩长会话',
                ))
    except Exception:
        pass

    return issues


def check_cache_config(cfg: dict) -> list[Issue]:
    """E: 检查 message-injector 缓存配置完整性（可选，需要 semantic-router M1/M3）"""
    issues = []
    cache_cfg = cfg.get('cache_config', {})

    injector_path_str = cache_cfg.get(
        'message_injector_path',
        '~/.openclaw/workspace/.openclaw/extensions/message-injector/index.ts'
    )
    injector_path = Path(injector_path_str).expanduser()

    if not injector_path.exists():
        return issues

    content = injector_path.read_text(encoding='utf-8')
    expected_ttl = cache_cfg.get('expected_ttl_ms', 1_800_000)
    bad_ttl = cache_cfg.get('bad_ttl_ms', 300_000)

    # E1: PATCH_CACHE_TTL 检查
    bad_ttl_patterns = [f'{bad_ttl}', '5 * 60 * 1000']
    found_bad = False
    found_line = ''
    for line in content.splitlines():
        if 'PATCH_CACHE_TTL' in line:
            for pat in bad_ttl_patterns:
                if pat in line:
                    found_bad = True
                    found_line = line.strip()
                    break
            break

    if found_bad:
        issues.append(Issue(
            idx=0, category='E', severity='alert',
            title='PATCH_CACHE_TTL 已回退至旧值（5 分钟）',
            detail=f'发现行: {found_line}\n'
                   f'期望: {expected_ttl // 60000} 分钟 ({expected_ttl}ms)\n'
                   f'影响: B 分支每 5 分钟触发不必要的 sessions.patch，LLM prompt cache 失效\n'
                   f'文件: {injector_path}',
            fix_description=f'手动编辑 message-injector/index.ts：将 PATCH_CACHE_TTL 改为 {expected_ttl // 60000} * 60 * 1000',
        ))

    # E2: extractDeclKey 函数存在性检查（M1）
    if cache_cfg.get('check_extract_decl_key', True):
        if 'function extractDeclKey(' not in content:
            issues.append(Issue(
                idx=0, category='E', severity='warn',
                title='M1 prependContext 稳定性机制缺失（extractDeclKey 未找到）',
                detail=f'未找到函数签名: function extractDeclKey(\n'
                       f'影响: 声明分数噪声（0.97/0.98）导致 user message 每次不同，对话 cache 无法命中\n'
                       f'文件: {injector_path}',
                fix_description='重新应用 M1 补丁：在 message-injector/index.ts 添加 extractDeclKey() 函数',
            ))

    return issues


# ─── 报告生成 ────────────────────────────────────────────────────────────────

def collect_all_issues(cfg: dict) -> list[Issue]:
    checks = cfg.get('checks', {})
    all_issues = []
    if checks.get('prompt_drift', True):
        all_issues.extend(check_prompt_drift(cfg))
    if checks.get('cron_jobs', True):
        all_issues.extend(check_cron_jobs(cfg))
    if checks.get('orphan_sessions', True):
        all_issues.extend(check_orphan_sessions(cfg))
    if checks.get('token_trend', True):
        all_issues.extend(check_token_trend(cfg))
    if checks.get('cache_config', False):
        all_issues.extend(check_cache_config(cfg))

    enabled_count = sum(1 for k, v in checks.items() if v)
    for i, issue in enumerate(all_issues, start=1):
        issue.idx = i

    return all_issues, enabled_count


def format_report(issues: list[Issue], enabled_count: int, dry_run: bool = False) -> str:
    now = datetime.now().strftime('%Y-%m-%d %H:%M')
    prefix = '[DRY RUN] ' if dry_run else ''

    ok_count = enabled_count - len(set(i.category for i in issues))
    alert_count = sum(1 for i in issues if i.severity == 'alert')
    warn_count = sum(1 for i in issues if i.severity == 'warn')

    lines = [f'{prefix}🔍 OpenClaw 健康报告 ({now})', '']

    if not issues:
        check_names = '、'.join(['Prompt 体积', 'Cron Job', 'Session', 'Token 趋势', '缓存配置'][:enabled_count])
        lines += [
            '✅ 全部正常，无需操作',
            '',
            f'监控范围：{check_names}',
        ]
        return '\n'.join(lines)

    status_parts = []
    if alert_count:
        status_parts.append(f'🔴 告警: {alert_count}')
    if warn_count:
        status_parts.append(f'🟡 警告: {warn_count}')
    if ok_count > 0:
        status_parts.append(f'✅ 正常类别: {ok_count}/{enabled_count}')
    lines.append(' | '.join(status_parts))
    lines.append('')
    lines.append('问题清单:')

    for issue in issues:
        sev_icon = '🔴' if issue.severity == 'alert' else '🟡'
        lines.append(f'\n{sev_icon} [{issue.idx}] [{issue.category}] {issue.title}')
        for detail_line in issue.detail.split('\n'):
            lines.append(f'   {detail_line}')
        if issue.fix_description:
            lines.append(f'   💊 修复: {issue.fix_description}')

    lines += [
        '',
        '─' * 40,
        '回复以下内容执行修复（发给主代理）:',
        f'• "health fix all" — 执行全部 ({len(issues)} 项)',
    ]
    if len(issues) > 1:
        idx_str = ' '.join(str(i.idx) for i in issues)
        lines.append(f'• "health fix {idx_str}" — 选择执行')
    lines.append('• "health skip" — 本次忽略')

    return '\n'.join(lines)


def execute_fix(issues: list[Issue], selected_indices: list[int], cfg: dict, dry_run: bool = False):
    selected = [i for i in issues if i.idx in selected_indices]
    if not selected:
        print('未找到匹配的问题编号')
        return

    for issue in selected:
        print(f'\n▶ 修复 [{issue.idx}] {issue.title}')
        if issue.category == 'B':
            if dry_run:
                print('  [DRY RUN] 将修复违规 Cron Job')
            else:
                _fix_cron_jobs(cfg)
        elif issue.category == 'C':
            if dry_run:
                print('  [DRY RUN] 将清理过期 Session')
            else:
                _fix_orphan_sessions(cfg)
        else:
            print(f'  ⚠️  需要手动处理: {issue.fix_description}')

    print('\n修复完成。建议重启 gateway: openclaw gateway restart')


def _fix_cron_jobs(cfg: dict):
    with open(CRON_JOBS) as f:
        jobs_data = json.load(f)

    jobs = jobs_data if isinstance(jobs_data, list) else jobs_data.get('jobs', list(jobs_data.values()))
    expensive_models = set(cfg.get('expensive_models', {}).get('list', ['claude-opus', 'opus-4.6']))
    fixed = 0

    for job in jobs:
        if job.get('status') == 'disabled':
            continue
        payload = job.get('payload', {})
        if payload.get('kind') != 'agentTurn':
            continue

        changed = False
        if job.get('sessionKey') is not None:
            job['sessionKey'] = None
            changed = True
        if 'timeoutSeconds' not in payload:
            payload['timeoutSeconds'] = 120
            changed = True
        model = payload.get('model', '')
        if any(em in model.lower() for em in expensive_models):
            payload['model'] = 'custom-llmapi-lovbrowser-com/google/gemini-2.5-flash'
            changed = True

        if changed:
            job['payload'] = payload
            fixed += 1

    with open(CRON_JOBS, 'w') as f:
        json.dump(jobs_data, f, indent=2, ensure_ascii=False)

    print(f'  ✅ 修复了 {fixed} 个 Cron Job')


def _fix_orphan_sessions(cfg: dict):
    stale_days = cfg.get('session_stale_days', 7)

    with open(SESSION_STATE) as f:
        sessions = json.load(f)

    now_ms = int(time.time() * 1000)
    stale_ms = stale_days * 24 * 3600 * 1000

    keys_to_remove = [
        k for k, v in sessions.items()
        if (ts := v.get('lastPatchedAt', v.get('updatedAt', 0))) and (now_ms - ts) > stale_ms
    ]

    for k in keys_to_remove:
        del sessions[k]

    with open(SESSION_STATE, 'w') as f:
        json.dump(sessions, f, indent=2, ensure_ascii=False)

    print(f'  ✅ 清理了 {len(keys_to_remove)} 个过期 Session: {keys_to_remove}')


# ─── 主程序 ──────────────────────────────────────────────────────────────────

def main():
    args = sys.argv[1:]

    if '--setup' in args:
        wizard_path = Path(__file__).parent / 'audit_wizard.py'
        os.execv(sys.executable, [sys.executable, str(wizard_path)])
        return

    cfg = load_config()

    dry_run = '--dry-run' in args
    do_report = '--report' in args or dry_run
    fix_arg = None
    fix_all = False

    for i, arg in enumerate(args):
        if arg == '--fix' and i + 1 < len(args):
            fix_arg = args[i + 1]
    if 'all' in args and '--fix' in args:
        fix_all = True

    list_fixes = '--list-fixes' in args

    issues, enabled_count = collect_all_issues(cfg)

    should_report = do_report or (not fix_arg and not list_fixes)
    if should_report:
        report = format_report(issues, enabled_count, dry_run=dry_run)
        print(report)
        REPORT_FILE.write_text(report)

    if list_fixes:
        print('\n可执行的修复命令:')
        for issue in issues:
            if issue.fix_cmd:
                print(f'  [{issue.idx}] {issue.fix_cmd}')
            elif issue.fix_description:
                print(f'  [{issue.idx}] (手动) {issue.fix_description}')

    if fix_arg or fix_all:
        if fix_all:
            selected = [i.idx for i in issues]
        else:
            selected = [int(x.strip()) for x in re.split(r'[,\s]+', fix_arg) if x.strip().isdigit()]
        execute_fix(issues, selected, cfg, dry_run=dry_run)

    if any(i.severity == 'alert' for i in issues):
        sys.exit(2)
    elif issues:
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == '__main__':
    main()
