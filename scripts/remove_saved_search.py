#!/usr/bin/env python3

import os
import sys
import json
import subprocess

query = sys.argv[1].strip()
workflow_dir = os.environ["alfred_workflow_data"]
workflow_name = os.environ.get("alfred_workflow_name", "Saved Search")
save_path = os.path.join(workflow_dir, "searches.json")

if not query or not os.path.exists(save_path):
    sys.exit(0)

# Load and filter
with open(save_path, "r") as f:
    saved = json.load(f)

new_list = [s for s in saved if s.get("query") != query]

# Write back
with open(save_path, "w") as f:
    json.dump(new_list, f, indent=2)

# Notify
subprocess.run([
    "osascript", "-e",
    f'display notification "Removed: {query}" with title "{workflow_name}"'
])
