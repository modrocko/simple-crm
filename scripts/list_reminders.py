#!/usr/bin/env python3

import os
import json
import sys
import utils

# === ENV VARS ===
folder = os.environ["contact_folder"]
ext = os.environ["file_extension"].strip()
query = sys.argv[1].strip().lower() if len(sys.argv) > 0 else ""
rowcount = 0

# === Parse query using utils ===
is_or, query_terms = utils.parse_query(query)

# === Local get_field — used only here ===
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
    for filename in os.listdir(folder):
        if not filename.endswith(ext):
            continue

        path = os.path.join(folder, filename)
        try:
            with open(path, "r") as f:
                content = f.read()

            reminder = get_field("Reminder", content)
            if not reminder:
                continue

            name = get_field("Name", content)
            icon = utils.get_icon_for_tag(content)
            row_text = f"{name} Reminder: {reminder}".lower()

            if query and not utils.matches_terms(row_text, query_terms, is_or):
                continue

            rowcount += 1
            items.append({
                "title": name,
                "subtitle": f"Reminder: {reminder}",
                "arg": path,
                "icon": icon
            })

        except Exception as e:
            items.append({
                "title": f"Error in {filename}",
                "subtitle": str(e),
                "valid": False
            })

if rowcount == 0:
    items.append({
        "title": "No reminders found",
        "subtitle": "No contacts have a 'Reminder:' value",
        "valid": False
    })

# === Output JSON ===
print(json.dumps({ "items": items }))
