#!/usr/bin/env python3

import os
import sys
import json
import subprocess

# === CHECK FOR ACTION TYPE ===
if os.environ.get("action") != "save_search":
    sys.exit(0)

# === GET SEARCH QUERY ===
query = sys.argv[1].strip() if len(sys.argv) > 1 else ""
if not query:
    sys.exit(0)

# === PATHS & SETTINGS ===
workflow_dir = os.environ["alfred_workflow_data"]
workflow_name = os.environ["alfred_workflow_name"]
save_path = os.path.join(workflow_dir, "searches.json")
max_count = int(os.environ["saved_search_count"])

# === LOAD EXISTING SAVES ===
try:
    with open(save_path, "r") as f:
        saved = json.load(f)
        if not isinstance(saved, list):
            saved = []
except:
    saved = []

# === CHECK FOR DUPLICATES ===
queries = [s["query"] for s in saved]
if query in queries:
    subprocess.run([
        "osascript", "-e",
        f'display notification "Already saved: {query}" with title "{workflow_name}"'
    ])
    sys.exit(0)

# === SAVE NEW QUERY TO TOP ===
saved.insert(0, { "name": query, "query": query })


# === TRIM & SAVE BACK ===
# === ENSURE FOLDER EXISTS & SAVE ===
os.makedirs(workflow_dir, exist_ok=True)
with open(save_path, "w") as f:
    json.dump(saved[:max_count], f, indent=2)

# === NOTIFY USER ===
subprocess.run([
    "osascript", "-e",
    f'display notification "Saved: {query}" with title "{workflow_name}"'
])
