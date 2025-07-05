#!/usr/bin/env python3

import os
import json
import sys
import subprocess

# === Get input ===
raw = sys.argv[1] if len(sys.argv) > 0 else ""
if not raw.startswith("clear::"):
    sys.exit(0)

# === Extract path ===
target_path = raw.split("clear::", 1)[1]

# === Load recent list ===
recent_path = os.path.join(os.environ["alfred_workflow_data"], "recent.json")
try:
    with open(recent_path, "r") as f:
        recent = json.load(f)
except Exception:
    recent = []

# === Filter & find name ===
updated = []
removed_name = None

for r in recent:
    if r.get("path") == target_path:
        removed_name = r.get("name") or os.path.basename(target_path)
        continue
    updated.append(r)

# === Save updated list ===
with open(recent_path, "w") as f:
    json.dump(updated, f, indent=2)

# === Notify user ===
if removed_name:
    title = os.environ.get("alfred_workflow_name", "Recent Items")
    subprocess.run([
        "osascript", "-e",
        f'display notification "Removed {removed_name} from recents list" with title "{title}"'
    ])
