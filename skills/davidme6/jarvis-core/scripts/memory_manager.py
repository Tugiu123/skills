#!/usr/bin/env python3
"""
Jarvis Core - Memory Manager
记忆管理系统：记录、检索、蒸馏记忆
"""

import json
import os
from datetime import datetime
from pathlib import Path

WORKSPACE = Path(os.environ.get('OPENCLAW_WORKSPACE', Path.home() / '.openclawworkspace'))
MEMORY_DIR = WORKSPACE / 'memory'
MEMORY_FILE = WORKSPACE / 'MEMORY.md'

def ensure_memory_dir():
    """确保记忆目录存在"""
    MEMORY_DIR.mkdir(parents=True, exist_ok=True)

def get_today_file():
    """获取今日记忆文件路径"""
    today = datetime.now().strftime('%Y-%m-%d')
    return MEMORY_DIR / f'{today}.md'

def log_event(event_type, content, metadata=None):
    """记录事件到今日记忆"""
    ensure_memory_dir()
    today_file = get_today_file()
    
    timestamp = datetime.now().strftime('%H:%M')
    
    entry = f"\n## [{timestamp}] {event_type}\n\n{content}\n"
    
    if metadata:
        entry += f"\n```json\n{json.dumps(metadata, indent=2, ensure_ascii=False)}\n```\n"
    
    with open(today_file, 'a', encoding='utf-8') as f:
        f.write(entry)
    
    return today_file

def log_decision(topic, decision, reasoning, alternatives=None):
    """记录决策"""
    content = f"**决策：** {decision}\n\n**理由：** {reasoning}"
    
    if alternatives:
        content += f"\n\n**考虑过的替代方案：**\n"
        for alt in alternatives:
            content += f"- {alt}\n"
    
    return log_event('🎯 决策', content, {
        'topic': topic,
        'decision': decision,
        'reasoning': reasoning
    })

def log_learning(what, insight, source=None):
    """记录学习"""
    content = f"**学到了：** {what}\n\n**洞察：** {insight}"
    
    if source:
        content += f"\n\n**来源：** {source}"
    
    return log_event('📚 学习', content, {
        'what': what,
        'insight': insight,
        'source': source
    })

def log_mistake(mistake, lesson, fix=None):
    """记录错误和教训"""
    content = f"**错误：** {mistake}\n\n**教训：** {lesson}"
    
    if fix:
        content += f"\n\n**修正方法：** {fix}"
    
    return log_event('⚠️ 错误/教训', content, {
        'mistake': mistake,
        'lesson': lesson,
        'fix': fix
    })

def log_task_completed(task, result=None, time_spent=None):
    """记录任务完成"""
    content = f"**任务：** {task}"
    
    if result:
        content += f"\n\n**结果：** {result}"
    
    if time_spent:
        content += f"\n\n**耗时：** {time_spent}"
    
    return log_event('✅ 任务完成', content)

def get_memory_summary(days=7):
    """获取最近 N 天的记忆摘要"""
    from datetime import timedelta
    
    summary = []
    
    for i in range(days):
        date = (datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d')
        file_path = MEMORY_DIR / f'{date}.md'
        
        if file_path.exists():
            content = file_path.read_text(encoding='utf-8')
            summary.append({
                'date': date,
                'content': content[:1000]  # 限制长度
            })
    
    return summary

def distill_to_longterm(key_points):
    """提炼到长期记忆 MEMORY.md"""
    if not MEMORY_FILE.exists():
        MEMORY_FILE.write_text('# MEMORY.md - 长期记忆\n\n', encoding='utf-8')
    
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M')
    
    entry = f"\n## {timestamp}\n\n"
    
    for point in key_points:
        entry += f"- {point}\n"
    
    with open(MEMORY_FILE, 'a', encoding='utf-8') as f:
        f.write(entry)
    
    return MEMORY_FILE

def search_memory(query):
    """搜索记忆"""
    results = []
    
    # 搜索今日记忆
    today_file = get_today_file()
    if today_file.exists():
        content = today_file.read_text(encoding='utf-8')
        if query.lower() in content.lower():
            results.append({
                'file': str(today_file),
                'match': 'today'
            })
    
    # 搜索长期记忆
    if MEMORY_FILE.exists():
        content = MEMORY_FILE.read_text(encoding='utf-8')
        if query.lower() in content.lower():
            results.append({
                'file': str(MEMORY_FILE),
                'match': 'longterm'
            })
    
    return results

def main():
    """命令行入口"""
    import sys
    
    if len(sys.argv) < 2:
        print("用法：jarvis-memory <command> [args]")
        print("命令:")
        print("  log <type> <content>  - 记录事件")
        print("  search <query>        - 搜索记忆")
        print("  summary [days]        - 查看摘要")
        print("  distill               - 提炼到长期记忆")
        return
    
    command = sys.argv[1]
    
    if command == 'log':
        if len(sys.argv) < 4:
            print("用法：jarvis-memory log <type> <content>")
            return
        event_type = sys.argv[2]
        content = ' '.join(sys.argv[3:])
        file_path = log_event(event_type, content)
        print(f"✅ 已记录到 {file_path}")
    
    elif command == 'search':
        if len(sys.argv) < 3:
            print("用法：jarvis-memory search <query>")
            return
        query = ' '.join(sys.argv[2:])
        results = search_memory(query)
        if results:
            print(f"找到 {len(results)} 个匹配:")
            for r in results:
                print(f"  - {r['file']} ({r['match']})")
        else:
            print("未找到匹配")
    
    elif command == 'summary':
        days = int(sys.argv[2]) if len(sys.argv) > 2 else 7
        summary = get_memory_summary(days)
        for day in summary:
            print(f"\n📅 {day['date']}")
            print(day['content'][:500])
    
    elif command == 'distill':
        print("请输入要提炼的要点（每行一个，空行结束）:")
        points = []
        while True:
            line = input()
            if not line.strip():
                break
            points.append(line.strip())
        
        if points:
            file_path = distill_to_longterm(points)
            print(f"✅ 已提炼到 {file_path}")
    
    else:
        print(f"未知命令：{command}")

if __name__ == '__main__':
    main()
