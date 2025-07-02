#!/usr/bin/env python3

import os
import zipfile
from datetime import datetime
import subprocess

# === ENV VARS ===
contact_folder = os.environ["contact_folder"]
backup_dir = os.environ["backup_folder"]
workflow_name = os.environ["alfred_workflow_name"]

# === Ensure backup folder exists ===
os.makedirs(backup_dir, exist_ok=True)

# === File naming ===
timestamp = datetime.now().strftime("%Y-%m-%d %H.%M")
zip_name = f"{workflow_name} backups {timestamp}.zip"
zip_path = os.path.join(backup_dir, zip_name)

# === Create ZIP ===
file_count = 0
with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
    for fname in os.listdir(contact_folder):
        fpath = os.path.join(contact_folder, fname)
        if os.path.isfile(fpath) and not fname.startswith(".") and not fname.endswith(".zip"):
            zipf.write(fpath, arcname=fname)
            file_count += 1

# === Notification ===
notif_title = f"{workflow_name} Backup Created"
notif_msg = f"{file_count} file(s) backed up to:\n{zip_path}"

subprocess.run([
    "osascript", "-e",
    f'display notification "{notif_msg}" with title "{notif_title}"'
])

# === Output zip path ===
print(zip_path)
