import json
from pathlib import Path


def save_accessibility_snapshot(snapshot, file_name="accessibility.json"):
    Path(file_name).write_text(
        json.dumps(snapshot, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )
    print(f"Saved accessibility tree to {file_name}")
