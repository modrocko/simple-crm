#!/usr/bin/env python3

import os
import sys
import json

workflow_dir = os.environ["alfred_workflow_data"]
save_path = os.path.join(workflow_dir, "searches.json")

query = sys.argv[1].strip().lower() if len(sys.argv) > 1 else ""
items = []

# Load saved searches
if os.path.exists(save_path):
    with open(save_path, "r") as f:
        saved = json.load(f)
else:
    saved = []

# Filter & build results
for entry in saved:
    text = entry.get("name")
    if not text:
        continue

    terms = query.lower().split()
    if any(term not in text.lower() for term in terms):
        continue

    items.append({
        "title": text,
        "subtitle": "↵ Run search • ⌘ Remove search • ⌥ Rename search" ,
        "arg": entry["query"],
        "mods": {
            "cmd": {
                "subtitle": "⌘ Remove this saved search",
                "arg": text
            },
            "option": {
                "subtitle": "⌥ Rename this saved search",
                "arg": text
            }
        }
    })

# Fallback message
if not items:
    items.append({
        "title": "No saved searches",
        "subtitle": "But there will be soon, I'm sure",
        "valid": False,
        "icon": { "path": "info.png" }
    })

print(json.dumps({ "items": items }))
