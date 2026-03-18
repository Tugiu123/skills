from pathlib import Path
import shutil

from project import get_current_version_dir
from state import StateManager


def run_deploy(project_root: Path, config: dict):
    version_dir = get_current_version_dir(project_root, config)
    if not version_dir:
        raise RuntimeError('没有找到当前版本目录')

    state = StateManager(version_dir)
    allowed = {'review_passed', 'all_done', 'deployed'}
    if state.data.get('status') not in allowed:
        raise RuntimeError(f"当前状态不允许 deploy: {state.data.get('status')}")

    state.data['status'] = 'deployed'
    state.save()

    return {
        'version': version_dir.name,
        'mode': config.get('adapters', {}).get('deploy', 'manual'),
        'message': '当前为基础版 deploy：仅完成状态推进，真实部署将由 deploy adapter 接管。',
    }


def run_seal(project_root: Path, config: dict):
    version_dir = get_current_version_dir(project_root, config)
    if not version_dir:
        raise RuntimeError('没有找到当前版本目录')

    state = StateManager(version_dir)
    if state.data.get('status') not in {'deployed', 'review_passed', 'all_done'}:
        raise RuntimeError(f"当前状态不允许 seal: {state.data.get('status')}")

    src_dir = version_dir / 'src'
    src_dir.mkdir(parents=True, exist_ok=True)

    exclude = {'versions', '.dtflow', '.git', 'node_modules', '__pycache__'}
    copied = 0
    for item in project_root.iterdir():
        if item.name in exclude:
            continue
        dest = src_dir / item.name
        if item.is_dir():
            shutil.copytree(item, dest, dirs_exist_ok=True)
            copied += 1
        elif item.is_file():
            shutil.copy2(item, dest)
            copied += 1

    (src_dir / '.version').write_text(version_dir.name, encoding='utf-8')
    state.data['status'] = 'sealed'
    state.save()

    return {
        'version': version_dir.name,
        'src_dir': str(src_dir),
        'items_copied': copied,
    }
