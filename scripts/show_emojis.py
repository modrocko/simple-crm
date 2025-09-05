#!/usr/bin/env python3

import os
import sys
import json

# === GET QUERY ===
query = sys.argv[1].lower() if len(sys.argv) > 1 else ""

# === READ EMOJIS FROM ENV VAR (one "emoji label" per line, separated by space) ===
raw = os.environ["emoji_list"]

pairs = []
for line in raw.splitlines():
    line = line.strip()
    if not line:
        continue
    parts = line.split(None, 1)  # split on first whitespace
    emoji = parts[0]
    name = parts[1].strip() if len(parts) > 1 else ""
    pairs.append((emoji, name))

# === FILTER ===
matches = []
for emoji, name in pairs:
    text = f"{emoji} {name}".lower()
    if query in text:
        matches.append((emoji, name))

# === SORT ALPHABETICALLY BY NAME ===
#matches.sort(key=lambda t: t[1])

# === BUILD RESULTS ===
items = []

# Top row with count
items.append({
    "title": f"{len(matches)} matching emojis",
    "subtitle": "Type to filter",
    "valid": False,
    "icon": {"path": "info.png"}
})

for emoji, name in matches:
    items.append({
        "title": f"{emoji}  {name}",
        "subtitle": "↵ Copy emoji (& paste into frontmost app)",
        "arg": emoji,  # send emoji to clipboard
        "text": {
            "copy": emoji
        }
    })

print(json.dumps({"items": items}))
