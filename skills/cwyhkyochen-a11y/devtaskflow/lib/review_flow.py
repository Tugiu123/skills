import re
from pathlib import Path

from llm import OpenAICompatibleLLM
from project import scan_project_files, get_current_version_dir
from state import StateManager


SYSTEM_PROMPT = """你是一个严格的代码审查员。请对以下代码进行全面审查。

必须按以下结构输出 Markdown：

# 代码审查报告

## 基本信息
| 项目 | 内容 |
|------|------|
| 任务编号 | [TASK_ID] |
| 任务名称 | [TASK_NAME] |
| 审查日期 | [日期] |

## 审查发现

### 🔴 严重问题（必须修复）
1. **[问题类型]** [问题描述]
   - **位置**: [文件路径]:[行号]
   - **影响**: [影响描述]
   - **修复建议**: [具体建议]

### 🟡 警告（建议修复）
1. **[问题类型]** [问题描述]
   - **位置**: [文件路径]:[行号]
   - **建议**: [改进建议]

### 🟢 建议（可选优化）
1. **[问题类型]** [问题描述]
   - **建议**: [优化建议]

## 代码质量评分

| 维度 | 评分 | 说明 |
|------|------|------|
| 功能完整性 | [0-10] | |
| 代码规范 | [0-10] | |
| 安全性 | [0-10] | |
| 性能 | [0-10] | |
| 可维护性 | [0-10] | |
| **总分** | **[0-10]** | |

## 审查结论

[✅ 通过 / ❌ 不通过]

**原因**:
[详细说明]
"""


def parse_review_passed(review_result: str):
    has_critical = '🔴' in review_result or '严重问题' in review_result

    conclusion_match = re.search(r'(?:## 审查结论|审查结论)[\s\S]*?([✅❌].*?)(?:\n\n|\n##|$)', review_result)
    if conclusion_match:
        conclusion = conclusion_match.group(1)
        if '❌' in conclusion or '不通过' in conclusion:
            return False
        if ('✅' in conclusion or '通过' in conclusion) and not has_critical:
            return True

    score_match = re.search(r'\|\s*\*\*总分\*\*\s*\|\s*\*\*(\d+(?:\.\d+)?)\*\*\s*\|', review_result)
    if score_match:
        score = float(score_match.group(1))
        return score >= 7.0 and not has_critical

    if has_critical:
        return False
    return True


def run_review(project_root: Path, config: dict):
    version_dir = get_current_version_dir(project_root, config)
    if not version_dir:
        raise RuntimeError('没有找到当前版本目录')

    state = StateManager(version_dir)
    if state.data.get('status') != 'written':
        raise RuntimeError(f"当前状态不允许 review: {state.data.get('status')}")

    task_id = state.data.get('current_task')
    tasks = state.data.get('tasks', [])
    task = next((t for t in tasks if t['id'] == task_id), None)
    if not task:
        raise RuntimeError('找不到当前任务')

    dev_plan_file = version_dir / 'docs' / 'DEV_PLAN.md'
    if not dev_plan_file.exists():
        raise RuntimeError('找不到 DEV_PLAN.md')
    dev_plan = dev_plan_file.read_text(encoding='utf-8')

    code_files = scan_project_files(project_root, limit=20)
    code = '\n\n'.join([
        f"=== 文件: {f['path']} ===\n```\n{f['content'][:4000]}\n```" for f in code_files[:10]
    ])

    llm = OpenAICompatibleLLM(config)
    user_prompt = f"""请审查以下代码：

## 任务
[{task['id']}] {task['name']}

## 开发计划
{dev_plan[:4000]}

## 代码
{code}
"""
    result = llm.chat(SYSTEM_PROMPT, user_prompt, max_tokens=12288, temperature=0.3)

    review_file = version_dir / 'docs' / f'REVIEW_TASK_{task_id}.md'
    review_file.write_text(result, encoding='utf-8')

    passed = parse_review_passed(result)
    state.data['status'] = 'review_passed' if passed else 'needs_fix'
    state.save()

    return {
        'task_id': task['id'],
        'task_name': task['name'],
        'review_file': str(review_file),
        'passed': passed,
    }
