import shutil
from pathlib import Path


def init_project_structure(project_root: Path, templates_dir: Path):
    dtflow_dir = project_root / '.dtflow'
    versions_dir = project_root / 'versions'
    docs_dir = project_root / 'docs'

    dtflow_dir.mkdir(parents=True, exist_ok=True)
    versions_dir.mkdir(parents=True, exist_ok=True)
    docs_dir.mkdir(parents=True, exist_ok=True)

    config_src = templates_dir / 'config.json'
    env_src = templates_dir / 'env.example'

    config_dst = dtflow_dir / 'config.json'
    env_dst = project_root / '.env.dtflow.example'

    if not config_dst.exists():
        shutil.copy2(config_src, config_dst)
    if not env_dst.exists():
        shutil.copy2(env_src, env_dst)

    return {
        'dtflow_dir': str(dtflow_dir),
        'versions_dir': str(versions_dir),
        'docs_dir': str(docs_dir),
        'config': str(config_dst),
        'env_example': str(env_dst),
    }
