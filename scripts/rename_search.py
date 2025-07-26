#!/usr/bin/env python3

import os
import sys
import json
import subprocess

# === REQUIRED ENV VARS ===
title = os.environ["alfred_workflow_name"]
workflow_dir = os.environ["alfred_workflow_data"]
save_path = os.path.join(workflow_dir, "searches.json")

# === INPUT ===
try:
    parts = sys.argv[1].split("|")
    if len(parts) != 2:
        raise ValueError
    old = parts[0].strip()
    new_name = parts[1].strip()
except:
    print("❌ Input must be in format: old|new")
    sys.exit(1)

# === LOAD EXISTING SEARCHES ===
try:
    with open(save_path, "r") as f:
        searches = json.load(f)
except FileNotFoundError:
    searches = []

if not isinstance(searches, list):
    searches = []

# === RENAME LOGIC ===
updated = 0

def set_name(entry, name):
    entry["name"] = name

# 1) if old is an int, treat it as index
if old.isdigit():
    idx = int(old)
    if 0 <= idx < len(searches):
        set_name(searches[idx], new_name)
        updated += 1
else:
    # 2) otherwise, match by query or name
    for entry in searches:
        if entry.get("query") == old or entry.get("name") == old:
            set_name(entry, new_name)
            updated += 1
            break

# === SAVE CHANGES ===
if updated > 0:
    with open(save_path, "w") as f:
        json.dump(searches, f, indent=2)

# === NOTIFY USER ===
if updated > 0:
    message = f"Renamed to: {new_name}"
else:
    message = f"No match found for '{old}'"

subprocess.run([
    "osascript", "-e",
    f'display notification "{message}" with title "{title}"'
])
