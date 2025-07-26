#!/usr/bin/env python3

import os
import json
import sys
import utils

# === ENV VARS ===
folder = os.environ["contact_folder"]
ext = os.environ["file_extension"].strip()
query = sys.argv[1].strip() if len(sys.argv) > 0 else ""
rowcount = 0

# === FIELDS TO SHOW ===
display_fields_env = os.environ.get("display_fields", "")
field_names = [field.strip() for field in display_fields_env.split(",")]

# === Extract field from file content ===
def get_field(field, content):
    for line in content.splitlines():
        if line.lower().startswith(f"{field.lower()}:"):
            return line.split(":", 1)[1].strip()
    return ""

items = []

# === If folder not found ===
if not os.path.exists(folder):
    items.append({
        "title": "Folder not found",
        "subtitle": folder,
        "valid": False
    })
else:
    matched = False
    found_files = False

    for filename in sorted(os.listdir(folder), key=str.lower):
        if not filename.endswith(ext):
            continue
        found_files = True
        path = os.path.join(folder, filename)
        try:
            with open(path, "r") as f:
                content = f.read()

            name = get_field("Name", content)
            fields = {field: get_field(field, content) for field in field_names}
            subtitle_parts = [fields[f] if fields[f] else "—" for f in field_names]
            subtitle = " ∙ ".join(subtitle_parts)

            match = utils.filter_contact(content, query, field_names)

            if match:
                icon = utils.get_icon_for_tag(fields.get("Tags", ""))
                matched = True
                rowcount += 1
                items.append({
                    "title": name,
                    "subtitle": subtitle,
                    "arg": path,
                    "icon": icon
                })

        except Exception as e:
            items.append({
                "title": f"Error in {filename}",
                "subtitle": str(e),
                "valid": False
            })

    if not found_files:
        items.append({
            "title": "No contacts available",
            "subtitle": f"No *{ext} files found in folder",
            "valid": False
        })
    elif not matched:
        items.append({
            "title": "No matches found",
            "subtitle": f"Query: {query}",
            "valid": False
        })

# === Summary row at the top ===
noun = "contact" if rowcount == 1 else "contacts"
if query:
    items.insert(0, {
        "title": f"{rowcount} {noun}",
        "subtitle": "↵ Save search ∙ ⌘ Update contacts ∙ ⌥ Open contacts ∙ ⌃ Export contacts",
        "arg": query,
        "icon": { "path": "info.png" },
        "variables": { "action": "save_search" },
        "mods": {
            "cmd": {
                "subtitle": "⌘ Update contacts in this list",
                "variables": { "query": query }
            },
            "alt": {
                "subtitle": "⌥ Open contacts in this list",
                "arg": query,
                "variables": { "query": query }
            },
            "ctrl": {
                "subtitle": "⌃ Exports contacts from this list",
                "arg": query
            }
        }
    })
else:
    items.insert(0, {
        "title": f"{rowcount} {noun}",
        "icon": { "path": "info.png" },
        "valid": False
    })

# === Output JSON for Alfred ===
print(json.dumps({ "items": items }))
