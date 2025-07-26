#!/usr/bin/env python3

import os
import csv
import subprocess
import sys
import utils

# === ARGS ===
query = sys.argv[1].strip() if len(sys.argv) > 1 else ""

# === ENV VARS ===
folder = os.environ["contact_folder"]
ext = os.environ.get("file_extension", ".md").strip()
export_fields = [f.strip() for f in os.environ.get("export_fields", "").split(",") if f.strip()]
display_fields_env = os.environ.get("display_fields", "")
display_fields = [f.strip() for f in display_fields_env.split(",") if f.strip()]
workflow_name = os.environ["alfred_workflow_name"]
export_path = os.path.expanduser(os.environ["export_path"])

# === Line-by-line field lookup ===
def get_field(field, lines):
    for line in lines:
        if line.lower().startswith(field.lower() + ":"):
            return line.split(":", 1)[1].strip()
    return ""

# === Gather data ===
rows = []

for filename in os.listdir(folder):
    if not filename.endswith(ext):
        continue

    path = os.path.join(folder, filename)
    with open(path, "r") as f:
        content = f.read()

    # <-- SAME matcher as list_contacts
    if not utils.filter_contact(content, query, display_fields):
        continue

    lines = content.splitlines()
    row = [get_field(field, lines) for field in export_fields]
    rows.append(row)

# === Write CSV ===
os.makedirs(os.path.dirname(export_path), exist_ok=True)
with open(export_path, "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(export_fields)
    writer.writerows(rows)

# === Notify ===
subprocess.run([
    "osascript", "-e",
    f'display notification "Exported {len(rows)} rows to {export_path}" with title "{workflow_name}"'
])

print(export_path)
