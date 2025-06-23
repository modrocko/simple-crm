#!/usr/bin/env python3

import os
import json
import sys

query = sys.argv[1].strip()

# Get display fields from env var
fields = os.environ["add_fields"]
field_list = [f.strip() for f in fields.split(",") if f.strip()]

# Count how many fields user has filled
active_index = query.count("|")

# Capitalize the current field
parts = []
for i, field in enumerate(field_list):
    if i == active_index:
        parts.append(field.upper())
    else:
        parts.append(field)

subtitle = " | ".join(parts)

items = [{
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
}]

print(json.dumps({ "items": items }))
