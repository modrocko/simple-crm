#!/usr/bin/env python3

import os
import csv
import re
import subprocess

# === ENV VARS ===
folder = os.environ["contact_folder"]
ext = os.environ.get("file_extension", ".md").strip()
import_path = os.path.expanduser(os.environ.get("import_path", ""))
workflow_name = os.environ.get("alfred_workflow_name", "Import")

# === Read rows from CSV ===
with open(import_path, newline="") as csvfile:
    reader = csv.reader(csvfile)
    headers = next(reader)
    rows = list(reader)

# === Make sure output folder exists ===
os.makedirs(folder, exist_ok=True)

# === Save each row as file ===
for row in rows:
    name = row[0].strip() if row else "Unnamed"
    slug = re.sub(r"[^\w]+", "-", name.lower()).strip("-") or "contact"
    filename = f"{slug}.{ext}"
    path = os.path.join(folder, filename)

    counter = 1
    while os.path.exists(path):
        filename = f"{slug}-{counter}.{ext}"
        path = os.path.join(folder, filename)
        counter += 1

    with open(path, "w") as f:
        for i, field in enumerate(headers):
            value = row[i].strip() if i < len(row) else ""
            line = f"{field}: {value}"
            if ext == ".md":
                line += "  "  # Markdown line break
            f.write(line + "\n")

# === Show notification ===
subprocess.run([
    "osascript", "-e",
    f'display notification "Imported {len(rows)} rows from {import_path}" with title "{workflow_name}"'
])

# === Output file path ===
print(import_path)
