#!/usr/bin/env python3

import os
import json
import re
import sys

# === ENV VARS ===
folder = os.environ["contact_folder"]
ext = os.environ.get("file_extension", ".md").strip()
query = sys.argv[1].strip().lower() if len(sys.argv) > 0 else ""

# === DETECT OR MODE ===
is_or = ":or" in query
query_terms = [q for q in query.replace(":or", "").split() if q]

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

    for filename in os.listdir(folder):
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

                full_text = f"{name} {' '.join(subtitle_parts)}".lower()

                match = (
                    any(term in full_text for term in query_terms)
                    if is_or else
                    all(term in full_text for term in query_terms)
                )

                if match:
                    matched = True
                    items.append({
                        "title": name or filename,
                        "subtitle": subtitle,
                        "arg": path
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

# === Output JSON for Alfred ===
print(json.dumps({ "items": items }))
