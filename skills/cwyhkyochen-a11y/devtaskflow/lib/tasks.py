import re


def parse_tasks_from_plan(dev_plan: str):
    tasks = []
    table_pattern = r'\|\s*(T\d+)\s*\|\s*([^|]+)\|\s*(P\d+)\s*\|\s*([^|]*)\|\s*([^|]*)\|\s*([^|]*)\|'
    for match in re.finditer(table_pattern, dev_plan):
        tasks.append({
            'id': match.group(1),
            'name': match.group(2).strip(),
            'priority': match.group(3),
            'dependencies': match.group(4).strip() if match.group(4) else None,
            'estimate': match.group(5).strip() if match.group(5) else None,
            'output_files': match.group(6).strip() if match.group(6) else None,
            'status': 'pending',
        })
    return tasks
