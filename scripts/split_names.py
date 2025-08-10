import os
import pandas as pd
import subprocess
import sys

title = os.environ["alfred_workflow_name"]

# ====== SETTINGS ======
INPUT_FILE = os.environ["export_path"]
OUTPUT_FILE = os.environ["export_path"] + "_split_names.csv"
NAME_COLUMN = "Name"
FIRSTNAME_COLUMN = "First Name"
LASTNAME_COLUMN = "Last Name"
SPLIT_LIMIT = 1  # How many splits (1 = split into 2 parts)
# ======================

# Check if input file exists
if not os.path.isfile(INPUT_FILE):
    subprocess.run([
        "osascript", "-e",
        f'display notification "Input file not found: {INPUT_FILE}" with title "{title}"'
    ])
    sys.exit(1)

# Load CSV
df = pd.read_csv(INPUT_FILE)

# Split name column
split_names = df[NAME_COLUMN].str.split(' ', n=SPLIT_LIMIT, expand=True)

# Drop original name column
df = df.drop(columns=[NAME_COLUMN])

# Insert new columns at start
df.insert(0, FIRSTNAME_COLUMN, split_names[0])
df.insert(1, LASTNAME_COLUMN, split_names[1])

# Save CSV
df.to_csv(OUTPUT_FILE, index=False)

# Show success notification
subprocess.run([
    "osascript", "-e",
    f'display notification "File saved as {OUTPUT_FILE}" with title "{title}"'
])
