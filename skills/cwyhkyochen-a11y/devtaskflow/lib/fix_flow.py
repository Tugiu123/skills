from pathlib import Path

from llm import OpenAICompatibleLLM
from project import scan_project_files, get_current_version_dir
from state import StateManager
from write_flow import parse_file_blocks, apply_file_blocks, SYSTEM_PROMPT as WRITE_SYSTEM_PROMPT


def run_fix(project_root: Path, config: dict):
    version_dir = get_current_version_dir(project_root, config)
    if not version_dir:
        raise RuntimeError('没有找到当前版本目录')

    state = StateManager(version_dir)
    if state.data.get('status') != 'needs_fix':
        raise RuntimeError(f"当前状态不允许 fix: {state.data.get('status')}")

    task_id = state.data.get('current_task')
    tasks = state.data.get('tasks', [])
    task = next((t for t in tasks if t['id'] == task_id), None)
    if not task:
        raise RuntimeError('找不到当前任务')

    review_file = version_dir / 'docs' / f'REVIEW_TASK_{task_id}.md'
    dev_plan_file = version_dir / 'docs' / 'DEV_PLAN.md'
    if not review_file.exists():
        raise RuntimeError('找不到审查报告')
    if not dev_plan_file.exists():
        raise RuntimeError('找不到 DEV_PLAN.md')

    review_feedback = review_file.read_text(encoding='utf-8')
    dev_plan = dev_plan_file.read_text(encoding='utf-8')
    project_files = scan_project_files(project_root, limit=20)
    context = '\n\n'.join([
        f"=== 文件: {f['path']} ===\n{f['content'][:2000]}" for f in project_files[:8]
    ])

    llm = OpenAICompatibleLLM(config)
    user_prompt = f"""请根据以下审查报告修复代码：

## 当前任务
[{task['id']}] {task['name']}

## 开发计划
{dev_plan[:5000]}

## 项目上下文
{context}

## 审查报告
{review_feedback}

请严格使用 FILE 输出格式返回修复后的代码。"""
    result = llm.chat(WRITE_SYSTEM_PROMPT, user_prompt, max_tokens=16384, temperature=0.3)
    file_blocks = parse_file_blocks(result)
    if not file_blocks:
        raise RuntimeError('fix 输出未解析出任何文件块')

    written = apply_file_blocks(project_root, file_blocks)
    state.data['status'] = 'written'
    state.save()

    return {
        'task_id': task['id'],
        'task_name': task['name'],
        'files': written,
        'count': len(written),
    }
