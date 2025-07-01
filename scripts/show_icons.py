#!/usr/bin/env python3

import os
import json
import sys

query = sys.argv[1].lower() if len(sys.argv) > 1 else ""
tag_icons_env = os.environ.get("tag_icons", "{}")

try:
    tag_icons = json.loads(tag_icons_env)
except json.JSONDecodeError:
    print(json.dumps({"items": [{"title": "❌ tag_icons is invalid JSON"}]}))
    sys.exit(1)

items = []
for tag, icon in tag_icons.items():
    if query in tag.lower():
        items.append({
            "title": tag,
            "subtitle": icon,
            "arg": tag,
            "icon": { "path": os.path.join("icons", icon) }
        })

print(json.dumps({"items": items}))
