#!/usr/bin/env python3

import os
import sys
import re
import subprocess

# === GET ENV VARS ===
contact_folder = os.environ["contact_folder"]
file_template = os.environ["file_template"]
ext = os.environ["file_extension"]
add_fields = os.environ["add_fields"]
open_file = os.environ["open_file"]

# === PARSE FIELD LISTS ===
if "," in file_template:
    all_fields = [f.strip() for f in file_template.split(",") if f.strip()]
else:
    all_fields = [line.strip() for line in file_template.strip().splitlines() if line.strip()]

add_fields = [f.strip() for f in add_fields.split(",") if f.strip()]

# === GET USER INPUT ===
if len(sys.argv) < 2:
    sys.exit("No input provided")

input_line = sys.argv[1].strip()
input_values = [v.strip() for v in input_line.split("|")]

# === MAP VALUES TO ADD_FIELDS ===
add_data = dict(zip(add_fields, input_values))

# === CREATE FILENAME FROM NAME FIELD ===
name = input_values[0] if input_values else "Unnamed"
slug = re.sub(r"[^\w]+", "-", name.lower()).strip("-")
filename = f"{slug}.{ext.lstrip('.')}"
path = os.path.join(contact_folder, filename)

# === IF FILE EXISTS, ADD -1, -2, ... ===
counter = 1
while os.path.exists(path):
    filename = f"{slug}-{counter}.{ext.lstrip('.')}"
    path = os.path.join(contact_folder, filename)
    counter += 1

# === ENSURE FOLDER EXISTS ===
os.makedirs(contact_folder, exist_ok=True)

# === WRITE FIELDS TO FILE ===
with open(path, "w") as f:
    for field in all_fields:
        value = add_data.get(field, "")
        if ext == ".md":
            value += "  "  # add 2 spaces for Markdown line break
        f.write(f"{field}: {value}\n")

# === NOTIFY USER ===
subprocess.run([
    "osascript", "-e",
    f'display notification "Contact saved" with title "CRM Contact Created" subtitle "{name}"'
])

# === OPEN FILE if requested ===
if open_file == "true":
    subprocess.run(["open", path])

# === RETURN FILE PATH TO ALFRED ===
print(path)
