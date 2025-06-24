#!/usr/bin/env python3

import os
import sys
import subprocess
import re
import utils

# === REQUIRED ENV VARS ===
folder = os.environ["contact_folder"]
ext = os.environ["file_extension"].strip()
title = os.environ["alfred_workflow_name"]

# === INPUT ===
try:
    parts = sys.argv[1].split("|")
    if len(parts) != 2:
        raise ValueError
    old = parts[0].strip()
    new = parts[1].strip()
    query = os.environ["query"].strip().lower()
except:
    print("❌ Input must be in format: old|new")
    sys.exit(1)

# === QUERY TERMS ===
is_or, terms = utils.get_query_terms(query)

updated = 0

for filename in os.listdir(folder):
    if not filename.endswith(ext):
        continue

    path = os.path.join(folder, filename)
    try:
        with open(path, "r") as f:
            content = f.read()

        full_text = content.lower()
        match = any(t in full_text for t in terms) if is_or else all(t in full_text for t in terms)

        if match and re.search(re.escape(old), content, re.IGNORECASE):
            content = re.sub(re.escape(old), new, content, flags=re.IGNORECASE)
            with open(path, "w") as f:
                f.write(content)
            updated += 1

    except Exception as e:
        print(f"⚠️ Error in {filename}: {e}")

# === Notify ===
if updated > 0:
    message = f"Updated {updated} file(s)"
else:
    message = f"'{old}' not found in matching files"

subprocess.run([
    "osascript", "-e",
    f'display notification "{message}" with title "{title}"'
])
