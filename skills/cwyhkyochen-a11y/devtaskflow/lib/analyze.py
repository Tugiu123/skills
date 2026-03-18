from pathlib import Path

from llm import OpenAICompatibleLLM
from tasks import parse_tasks_from_plan
from project import scan_project_files, get_current_version_dir
from state import StateManager


SYSTEM_PROMPT = """你是一个资深全栈架构师。请基于需求文档，生成详细的开发执行方案。

【输出格式要求】
必须按以下结构输出 Markdown：

# 项目开发方案

## 1. 需求理解
- 业务目标
- 核心业务流程
- 关键技术特性

## 2. 技术架构
- 整体架构图（ASCII）
- 技术选型表格
- 目录结构设计

## 3. 数据库设计
- 完整的 SQL 建表语句
- 索引设计
- 外键约束

## 4. API 接口设计
- 每个接口的 Method/Path
- Request/Response 格式
- 错误码定义

## 5. 任务清单（关键！必须可被解析）

### 阶段一：基础设施（P0）
| 任务ID | 任务名称 | 优先级 | 依赖 | 预估工时 | 输出文件 |
|--------|---------|--------|------|---------|----------|
| T001 | 项目初始化 | P0 | 无 | 2h | package.json, .gitignore |

## 6. 风险评估
- 技术风险表格
- 缓解措施
"""


def run_analyze(project_root: Path, config: dict):
    version_dir = get_current_version_dir(project_root, config)
    if not version_dir:
        raise RuntimeError('没有找到当前版本目录，请先准备版本目录')

    req_file = version_dir / 'docs' / 'REQUIREMENTS.md'
    if not req_file.exists():
        raise RuntimeError(f'找不到需求文档: {req_file}')

    requirements = req_file.read_text(encoding='utf-8')
    project_files = scan_project_files(project_root)
    context = '\n\n'.join([
        f"=== 文件: {f['path']} ===\n{f['content'][:2000]}" for f in project_files[:10]
    ])

    llm = OpenAICompatibleLLM(config)
    user_prompt = f"""请根据以下需求和项目上下文，输出完整开发方案：

## 需求文档

{requirements}

## 项目上下文

{context}
"""
    result = llm.chat(SYSTEM_PROMPT, user_prompt, max_tokens=16384, temperature=0.6)

    plan_file = version_dir / 'docs' / 'DEV_PLAN.md'
    plan_file.write_text(result, encoding='utf-8')

    tasks = parse_tasks_from_plan(result)
    state = StateManager(version_dir)
    if not state.data:
        state.init(version_dir.name)
    state.data['tasks'] = tasks
    state.data['status'] = 'pending_confirm'
    state.save()

    return {
        'plan_file': str(plan_file),
        'tasks': tasks,
        'task_count': len(tasks),
    }
