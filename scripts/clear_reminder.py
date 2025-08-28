#!/usr/bin/env python3
import os, sys, subprocess

# === ENV VARS ===
title = os.environ["alfred_workflow_name"]
folder = os.environ["contact_folder"]
field_name = os.environ["reminder_query_field"].strip()
contact_name = sys.argv[1].strip()

# === Build file path ===
path = os.path.join(folder, f"{contact_name}.md")
if not os.path.exists(path):
    sys.exit(f"❌ Contact file not found: {path}")

# === Clear the field ===
new_lines = []
with open(path, "r", encoding="utf-8") as f:
    for line in f:
        if line.lower().startswith(field_name.lower() + ":"):
            new_lines.append(f"{field_name}: \n")  # clear value
        else:
            new_lines.append(line)

with open(path, "w", encoding="utf-8") as f:
    f.writelines(new_lines)

print(f"✅ Cleared {field_name} for {contact_name}")
subprocess.run(
    ["osascript","-e",f'display notification "Reminder cleared for {contact_name}" with title "{title}"']
)