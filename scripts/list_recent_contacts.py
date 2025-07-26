#!/usr/bin/env python3

import os
import json
import sys
import utils

# === ENV VARS ===
query = sys.argv[1].strip().lower() if len(sys.argv) > 0 else ""
rowcount = 0
items = []

# === Load recent list ===
recent_path = os.path.join(os.environ["alfred_workflow_data"], "recent.json")
try:
    with open(recent_path, "r") as f:
        recent_list = json.load(f)
except Exception:
    recent_list = []

# === Updated list to keep only valid entries ===
valid_entries = []

for entry in recent_list:
    name = entry.get("name", "")
    path = entry.get("path", "")

    if not os.path.exists(path):
        continue  # skip this entry (will be removed from recent)

    valid_entries.append(entry)

    if query and query not in name.lower():
        continue

    # === Read tags from file ===
    tags = ""
    try:
        with open(path, "r") as f:
            for line in f:
                if line.lower().startswith("lead status:"):
                    tags = line.split(":", 1)[1].strip()
                    break
    except Exception:
        pass

    icon = utils.get_icon_for_tag(tags)

    items.append({
        "title": name,
        "subtitle": "↵ Open contact file ∙ ⌘ Clear contact from recents",
        "arg": path,
        "icon": icon,
        "mods": {
            "cmd": {
                "subtitle": "⌘ Clear this recent contact",
                "arg": f"clear::{path}"
            }
        }
    })
    rowcount += 1

# === Save cleaned recent list ===
with open(recent_path, "w") as f:
    json.dump(valid_entries, f, indent=2)

# === Summary row ===
noun = "contact" if rowcount == 1 else "contacts"
summary_item = {
    "title": f"{rowcount} recent {noun}",
    "icon": { "path": "info.png" },
    "arg": "clear_recents"
}

if rowcount > 0:
    summary_item["subtitle"] = "↵ Clear recents"

items.insert(0, summary_item)

# === Output JSON ===
print(json.dumps({ "items": items }))
