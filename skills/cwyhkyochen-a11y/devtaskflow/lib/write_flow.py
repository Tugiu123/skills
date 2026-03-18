import re
from pathlib import Path

from llm import OpenAICompatibleLLM
from project import scan_project_files, get_current_version_dir
from state import StateManager


SYSTEM_PROMPT = """你是一个专业的高级软件工程师。请基于开发计划，编写高质量的代码。

对于每个需要创建的文件，必须按以下格式输出：

### FILE: [相对路径]
**操作类型**: [create | overwrite | append]
**描述**: [该文件的用途说明]

```[语言]
[完整的文件代码内容]
```

---

规则：
1. 每个文件必须以 `### FILE: 路径` 开头
2. 操作类型必须明确
3. 路径使用相对路径
4. 不要省略任何任务要求的文件
"""


def parse_file_blocks(code_result: str):
    files = []
    file_sections = re.split(r'\n---\s*\n|\n(?=### FILE:)', code_result)
    for section in file_sections:
        section = section.strip()
        if not section:
            continue
        file_match = re.search(r'###\s*FILE:\s*(.+?)(?:\n|$)', section)
        if not file_match:
            continue
        filepath = file_match.group(1).strip()
        op_match = re.search(r'\*\*操作类型\*\*:\s*(\w+)', section)
        operation = op_match.group(1).lower() if op_match else 'create'
        desc_match = re.search(r'\*\*描述\*\*:\s*(.+?)(?:\n|$)', section)
        description = desc_match.group(1).strip() if desc_match else ''
        code_match = re.search(r'```[\w]*\n([\s\S]*?)```', section)
        if not code_match:
            continue
        content = code_match.group(1).strip()
        if not content:
            continue
        files.append({
            'path': filepath,
            'operation': operation,
            'description': description,
            'content': content,
        })
    return files


def apply_file_blocks(project_root: Path, file_blocks: list):
    written = []
    for block in file_blocks:
        full_path = project_root / block['path']
        full_path.parent.mkdir(parents=True, exist_ok=True)
        operation = block['operation']
        if operation == 'append':
            existing = full_path.read_text(encoding='utf-8') if full_path.exists() else ''
            full_path.write_text(existing + ('\n' if existing else '') + block['content'], encoding='utf-8')
            action = 'append'
        elif operation == 'overwrite':
            full_path.write_text(block['content'], encoding='utf-8')
            action = 'overwrite'
        else:
            if full_path.exists():
                full_path.write_text(block['content'], encoding='utf-8')
                action = 'overwrite'
            else:
                full_path.write_text(block['content'], encoding='utf-8')
                action = 'create'
        written.append({'path': block['path'], 'action': action})
    return written


def run_write(project_root: Path, config: dict, task_id: str | None = None):
    version_dir = get_current_version_dir(project_root, config)
    if not version_dir:
        raise RuntimeError('没有找到当前版本目录')

    state = StateManager(version_dir)
    if state.data.get('status') not in {'confirmed', 'review_passed', 'needs_fix'}:
        raise RuntimeError(f"当前状态不允许 write: {state.data.get('status')}")

    tasks = state.data.get('tasks', [])
    task_id = task_id or state.data.get('current_task')
    task = next((t for t in tasks if t['id'] == task_id), None)
    if not task:
        raise RuntimeError(f'找不到任务: {task_id}')

    dev_plan_file = version_dir / 'docs' / 'DEV_PLAN.md'
    if not dev_plan_file.exists():
        raise RuntimeError('找不到 DEV_PLAN.md，请先执行 analyze')

    dev_plan = dev_plan_file.read_text(encoding='utf-8')
    project_files = scan_project_files(project_root)
    context = '\n\n'.join([
        f"=== 文件: {f['path']} ===\n{f['content'][:2000]}" for f in project_files[:8]
    ])

    llm = OpenAICompatibleLLM(config)
    user_prompt = f"""当前任务：[{task['id']}] {task['name']}

输出文件：{task.get('output_files')}
依赖：{task.get('dependencies')}

## 开发计划
{dev_plan[:6000]}

## 项目上下文
{context}

请生成完整代码，并严格使用 FILE 输出格式。"""
    result = llm.chat(SYSTEM_PROMPT, user_prompt, max_tokens=16384, temperature=0.4)
    file_blocks = parse_file_blocks(result)
    if not file_blocks:
        raise RuntimeError('LLM 输出未解析出任何文件块')

    written = apply_file_blocks(project_root, file_blocks)
    state.data['status'] = 'written'
    state.save()

    return {
        'task_id': task['id'],
        'task_name': task['name'],
        'files': written,
        'count': len(written),
    }
