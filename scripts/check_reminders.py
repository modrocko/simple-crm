#!/usr/bin/env python3

import os
import datetime
import subprocess

# === ENV VARS ===
folder = os.environ["contact_folder"]
ext = os.environ["file_extension"].strip()
date_format = os.environ["reminder_date_format"]
workflow_name = os.environ["alfred_workflow_name"]

# === TODAY ===
today = datetime.date.today().strftime(date_format)
print(f"Today's date: {today}\n")

names = []

for filename in os.listdir(folder):
    if not filename.endswith(ext):
        continue

    path = os.path.join(folder, filename)
    try:
        with open(path, "r") as f:
            lines = f.readlines()

        for line in lines:
            if "@reminder:" in line.lower():
                parts = line.split("@reminder:", 1)
                if len(parts) < 2:
                    continue
                reminder_raw = parts[1].strip().title()
                print(f"{filename} → Found: {reminder_raw}")
                if reminder_raw == today:
                    # Get first field name
                    for l in lines:
                        if ":" in l:
                            name = l.split(":", 1)[1].strip()
                            names.append(name)
                            print(f"→ MATCHED: {name} ({path})")
                            break
                else:
                    print("→ No match\n")
    except Exception as e:
        print(f"{filename} → Error: {e}")

if names:
    print("\nFinal matched names:")
    for name in names:
        print(name)

    body = "\n" + "\n".join(names)
    subprocess.run([
        "osascript", "-e",
        f'display notification "Reminder to contact:{body}" with title "{workflow_name}"'
    ])
else:
    print("\nNo reminders found for today.")
