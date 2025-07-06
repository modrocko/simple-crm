#!/usr/bin/env python3

import os
import sys
import json

# === GET QUERY ===
query = sys.argv[1].lower() if len(sys.argv) > 1 else ""

# === LOAD ICONS DIRECTORY ===
workflow_dir = os.path.dirname(__file__)
icons_dir = os.path.join(workflow_dir, "..", "icons")

try:
    icon_files = os.listdir(icons_dir)
except FileNotFoundError:
    print(json.dumps({"items": [{"title": "❌ icons folder not found"}]}))
    sys.exit(1)

# === GET TAGS FROM FILENAMES ===
tags = []
for filename in icon_files:
    if not filename.lower().endswith(".png"):
        continue
    tag = os.path.splitext(filename)[0]
    if query in tag.lower():
        tags.append((tag, filename))

# === SORT TAGS ALPHABETICALLY ===
tags.sort()

# === BUILD RESULTS ===
items = []
for tag, filename in tags:
    items.append({
        "title": f"@{tag}",
        "subtitle": filename,
        "arg": f"@{tag}",
        "icon": { "path": os.path.join("icons", filename) }
    })

print(json.dumps({ "items": items }))
