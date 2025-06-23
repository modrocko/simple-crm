#!/usr/bin/env python3

import os
import csv
import subprocess

# === ENV VARS ===
folder = os.environ["contact_folder"]
ext = os.environ.get("file_extension", ".md").strip()
export_fields = [f.strip() for f in os.environ.get("export_fields", "").split(",") if f.strip()]
workflow_name = os.environ["alfred_workflow_name"]
export_path = os.environ["export_path"]
export_path = os.path.expanduser(export_path)

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
        lines = f.readlines()
        row = []
        for field in export_fields:
            value = get_field(field, lines)
            row.append(value)
        rows.append(row)

# === Write CSV ===
os.makedirs(os.path.dirname(export_path), exist_ok=True)
with open(export_path, "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(export_fields)
    writer.writerows(rows)

# === Show notification with full path ===
subprocess.run([
    "osascript", "-e",
    f'display notification "Exported {len(rows)} rows to {export_path}" with title "{workflow_name}"'
])

# === Output path for Alfred ===
print(export_path)
