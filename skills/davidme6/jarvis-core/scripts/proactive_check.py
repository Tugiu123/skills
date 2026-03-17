#!/usr/bin/env python3
"""
Jarvis Core - Proactive Check Script
主动检查系统状态、项目进展、待办事项
"""

import json
import os
from datetime import datetime, timedelta
from pathlib import Path

WORKSPACE = Path(os.environ.get('OPENCLAW_WORKSPACE', Path.home() / '.openclawworkspace'))
MEMORY_DIR = WORKSPACE / 'memory'
MEMORY_FILE = WORKSPACE / 'MEMORY.md'
USER_FILE = WORKSPACE / 'USER.md'
SOUL_FILE = WORKSPACE / 'SOUL.md'

def check_workspace_changes():
    """检查 workspace 变化"""
    import subprocess
    try:
        result = subprocess.run(
            ['git', 'status', '--porcelain'],
            cwd=WORKSPACE,
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.stdout.strip():
            return {
                'has_changes': True,
                'changes': result.stdout.strip().split('\n')
            }
        return {'has_changes': False}
    except:
        return {'has_changes': False, 'error': 'git not available'}

def check_recent_memory():
    """检查最近记忆文件"""
    today = datetime.now().strftime('%Y-%m-%d')
    today_file = MEMORY_DIR / f'{today}.md'
    
    yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
    yesterday_file = MEMORY_DIR / f'{yesterday}.md'
    
    result = {
        'today_exists': today_file.exists(),
        'yesterday_exists': yesterday_file.exists()
    }
    
    if today_file.exists():
        result['today_content'] = today_file.read_text()[:500]
    
    return result

def check_pending_tasks():
    """检查待办事项"""
    tasks = []
    
    # 检查 HEARTBEAT.md 中的任务
    heartbeat_file = WORKSPACE / 'HEARTBEAT.md'
    if heartbeat_file.exists():
        content = heartbeat_file.read_text()
        # 简单提取任务项
        for line in content.split('\n'):
            if line.strip().startswith('- [ ]') or line.strip().startswith('□'):
                tasks.append(line.strip())
    
    return {'tasks': tasks}

def generate_suggestions():
    """生成主动建议"""
    suggestions = []
    
    # 检查时间，给出时段建议
    hour = datetime.now().hour
    
    if 7 <= hour <= 9:
        suggestions.append("早上好！今天有什么重要安排吗？我可以帮你检查日历和邮件。")
    elif 12 <= hour <= 13:
        suggestions.append("午餐时间！记得休息一下。下午有什么需要准备的吗？")
    elif 17 <= hour <= 18:
        suggestions.append("快下班了，今天的工作需要我总结或记录吗？")
    elif 22 <= hour or hour <= 6:
        suggestions.append("这么晚还在工作？注意休息。需要我帮你整理明天的待办吗？")
    
    # 检查是否有未完成的电商项目
    # （根据用户最近的对话）
    suggestions.append("关于美国电商项目，需要我深入分析某个具体方向吗？比如：竞品分析、选品调研、或视频脚本？")
    
    return suggestions

def main():
    """主函数"""
    result = {
        'timestamp': datetime.now().isoformat(),
        'workspace': check_workspace_changes(),
        'memory': check_recent_memory(),
        'tasks': check_pending_tasks(),
        'suggestions': generate_suggestions()
    }
    
    # 输出 JSON 供 OpenClaw 使用
    print(json.dumps(result, indent=2, ensure_ascii=False))
    
    # 同时输出人类可读版本
    print("\n" + "="*50)
    print("🤖 JARVIS PROACTIVE CHECK")
    print("="*50)
    
    if result['workspace']['has_changes']:
        print(f"\n📝 Workspace 有未提交的变化")
        for change in result['workspace']['changes'][:5]:
            print(f"   {change}")
    
    if result['tasks']['tasks']:
        print(f"\n📋 待办事项:")
        for task in result['tasks']['tasks']:
            print(f"   {task}")
    
    print(f"\n💡 建议:")
    for suggestion in result['suggestions']:
        print(f"   • {suggestion}")
    
    print("\n" + "="*50)

if __name__ == '__main__':
    main()
