import json
from pathlib import Path
from datetime import datetime


class StateManager:
    def __init__(self, version_dir: Path):
        self.version_dir = version_dir
        self.state_file = version_dir / '.state.json'
        self.data = self._load()

    def _load(self):
        if self.state_file.exists():
            return json.loads(self.state_file.read_text(encoding='utf-8'))
        return {}

    def init(self, version: str):
        now = datetime.now().isoformat()
        self.data = {
            'version': version,
            'status': 'initialized',
            'current_task': None,
            'architecture_confirmed': False,
            'tasks': [],
            'created_at': now,
            'updated_at': now,
        }
        self.save()

    def save(self):
        self.data['updated_at'] = datetime.now().isoformat()
        self.state_file.write_text(
            json.dumps(self.data, ensure_ascii=False, indent=2),
            encoding='utf-8'
        )

    def update_status(self, status: str):
        self.data['status'] = status
        self.save()

    def set_tasks(self, tasks: list):
        self.data['tasks'] = tasks
        self.save()

    def set_current_task(self, task_id: str | None):
        self.data['current_task'] = task_id
        self.save()
