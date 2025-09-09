#!/usr/bin/env python3

import os
import sys
import subprocess
import utils

# === REQUIRED ENV VARS ===
folder = os.environ["contact_folder"]
ext = os.environ["file_extension"].strip()
title = os.environ["alfred_workflow_name"]

# === INPUT ===
try:
    query = os.environ["query"].strip()
except KeyError:
    print("❌ Missing query")
    sys.exit(1)

# === DISPLAY FIELDS (for consistent matching) ===
display_fields_env = os.environ.get("display_fields", "")
display_fields = [f.strip() for f in display_fields_env.split(",") if f.strip()]

opened = 0

for filename in os.listdir(folder):
    if not filename.endswith(ext):
        continue

    path = os.path.join(folder, filename)
    try:
        with open(path, "r") as f:
            content = f.read()

        # Unified matching logic
        if utils.filter_contact(content, query, display_fields):
            subprocess.run(["open", path])
            utils.add_to_recent(path)
            opened += 1

    except Exception as e:
        print(f"⚠️ Error in {filename}: {e}")

# === Notify ===
msg = f"Opened {opened} contact(s)" if opened else "No matching contacts found"
subprocess.run([
    "osascript", "-e",
    f'display notification "{msg}" with title "{title}"'
])
