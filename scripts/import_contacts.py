#!/usr/bin/env python3

import os
import csv
import re
import subprocess
import sys

# === ENV VARS ===
folder = os.environ["contact_folder"]
ext = os.environ["file_extension"]
import_path = os.environ["import_path"]
workflow_name = os.environ["alfred_workflow_name"]
filename_fields = os.environ.get("filename_fields", "")
filename_separator = os.environ.get("filename_separator", " ")
if not filename_separator.strip():
    filename_separator = " "

# === Check if import file exists ===
if not os.path.exists(import_path):
    subprocess.run([
        "osascript", "-e",
        f'display notification "Import file not found: {import_path}" with title "{workflow_name}"'
    ])
    sys.exit(1)

# === Read rows from CSV ===
with open(import_path, newline="") as csvfile:
    reader = csv.reader(csvfile)
    headers = next(reader)
    rows = list(reader)

# === Make sure output folder exists ===
os.makedirs(folder, exist_ok=True)

# === Save each row as file ===
for row in rows:
    data = {headers[i]: row[i].strip() for i in range(min(len(headers), len(row)))}

    # === Create filename ===
    if filename_fields.strip():
        parts = [data.get(field.strip(), "") for field in filename_fields.split(",")]
        base_name = filename_separator.join(parts).strip()
    else:
        base_name = row[0].strip() if row else "Unnamed"

    # === Normalize filename but keep separator ===
    pattern = rf"[^\w{re.escape(filename_separator)}]+"
    slug = re.sub(pattern, "", base_name).strip()

    filename = f"{slug}{ext}"
    path = os.path.join(folder, filename)

    # === Handle duplicates ===
    counter = 1
    while os.path.exists(path):
        filename = f"{slug}-{counter}{ext}"
        path = os.path.join(folder, filename)
        counter += 1

    # === Write content ===
    with open(path, "w") as f:
        for i, field in enumerate(headers):
            value = row[i].strip() if i < len(row) else ""
            line = f"{field}: {value}"
            if ext == ".md":
                line += "  "
            f.write(line + "\n")

# === Show notification ===
subprocess.run([
    "osascript", "-e",
    f'display notification "Imported {len(rows)} rows from {import_path}" with title "{workflow_name}"'
])

# === Output import path ===
print(import_path)
