#!/usr/bin/env python3

import os
import json
import sys

query = sys.argv[1].strip()

# Get display_fields from env var
fields = os.environ["add_fields"]
field_list = [f.strip() for f in fields.split(",") if f.strip()]
subtitle = "Format: " + " | ".join(field_list)

items = []
items.append({
    "title": "Add new contact",
    "subtitle": subtitle,
    "arg": query,
    "variables": {"open_file": "false"},
    "mods": {
        "cmd": {
            "arg": query,
            "subtitle": "⌘ Save & open contact file",
            "variables": {"open_file": "true"}
        }
    }
})
print(json.dumps({ "items": items }))
