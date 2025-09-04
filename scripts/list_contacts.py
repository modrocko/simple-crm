#!/usr/bin/env python3

import os
import json
import sys
import utils
import sort

# === ENV VARS ===
folder = os.environ["contact_folder"]
ext = os.environ["file_extension"].strip()

query = sys.argv[1].strip() if len(sys.argv) > 0 else ""

# allow sorting (for date fields only at this time - for 'reminders')
query, sort_field, descending = sort.extract_sort(query)

rowcount = 0

# === FIELDS TO SHOW ===
# Use default fields unless specified otherwise by 'fields_env' config variable
# This is how to control view for this script, by setting 'fields_env' var. Cool huh?
fields_env_name = os.environ.get("fields_env", "display_fields")
display_fields_env = os.environ[fields_env_name]
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
else:  # folder found
    matched = False
    found_files = False

    # loop all files in the contacts folder, sorted by name
    for filename in sorted(os.listdir(folder), key=str.lower):
        if not filename.endswith(ext):
            continue
        found_files = True
        path = os.path.join(folder, filename)
        try:
            # read the whole contact file
            with open(path, "r") as f:
                content = f.read()

            # grab the Name field & all display fields
            name = get_field("Name", content)
            fields = {field: get_field(field, content) for field in field_names}

            # show only first two tags for 'Lead Status'
            lead = fields["Lead Status"].strip()
            if lead:
                words = lead.split()
                count = int(os.environ["tag_count"])
                fields["Lead Status"] = " ".join(words[:count])

            # build subtitle only from non-empty fields
            subtitle_parts = [fields[f] for f in field_names if fields[f]]
            subtitle = " ∙ ".join(subtitle_parts)


            # get next action date field from configuration
            next_action_date = fields.get(os.environ.get("reminder_query_field", ""), "")

            # run the search
            match = utils.filter_contact(content, query, field_names)

            if match:
                # get the right icon based on lead status field
                icon = utils.get_icon_for_tag(fields["Lead Status"])
                matched = True
                rowcount += 1

                # add row for this contact
                items.append({
                    "title": name,
                    "subtitle": subtitle,
                    "arg": path,
                    "icon": icon,
                    "mods":{
                        "cmd": {
                            "subtitle": "⌘ View contact",
                            "variables": {
                                "action": "view_contact"
                            }
                        },
                        "alt": {
                            # set reminder function if 'next actiondate' is non null
                            "subtitle": "⌥ Set reminder" if next_action_date else "",
                            "arg": name,
                            "variables": {
                                "next_action_date": next_action_date,
                                "action": "set_reminder"
                            }
                        },
                        "ctrl": {
                            # set reminder function if 'next actiondate' is non null
                            "subtitle": "⌃ Clear reminder" if next_action_date else "",
                            "arg": name,
                            "variables": {
                                "action": "clear_reminder"
                            }
                        }
                    }
                })

        except Exception as e:
            # show any file level errors
            items.append({
                "title": f"Error in {filename}",
                "subtitle": str(e),
                "valid": False
            })

    # handle empty states
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
                "variables": {
                    "query": query,
                    "action": "update_contacts"
                }
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
    # no query typed yet, show 1st row prompt
    items.insert(0, {
        "title": f"{rowcount} {noun}",
        "subtitle": "Start typing to filter contacts",
        "icon": { "path": "info.png" },
        "valid": False
    })


# Sort contacts, if specified (while keeping summary row at top)
if sort_field:
    items = sort.sort_items_keep_first(items, key_field=sort_field, descending=descending)

# === Output JSON for Alfred ===
print(json.dumps({ "items": items }))
