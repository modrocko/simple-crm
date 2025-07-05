#!/usr/bin/env python3

import os
import json
import sys
import subprocess

# === Get the correct argument ===
arg = sys.argv[1].strip() if len(sys.argv) > 1 else ""

if arg != "clear_recents":
    sys.exit(0)

# === Clear the recents file ===
recent_path = os.path.join(os.environ["alfred_workflow_data"], "recent.json")

try:
    with open(recent_path, "w") as f:
        json.dump([], f)
except Exception:
    pass

# === Show notification ===
title = os.environ["alfred_workflow_name"]
subprocess.run([
    "osascript", "-e",
    f'display notification "Recent contacts cleared" with title "{title}"'
])