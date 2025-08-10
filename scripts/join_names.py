import os
import pandas as pd
import subprocess
import sys

title = os.environ["alfred_workflow_name"]

# ====== SETTINGS ======
INPUT_FILE = os.environ["import_path"]
OUTPUT_FILE = os.path.splitext(INPUT_FILE)[0] + "_joined_names.csv"
NAME_COLUMN = "Name"
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

# Get names of first two columns
col1, col2 = df.columns[:2]

# Join first two columns into "Name"
df[NAME_COLUMN] = df[col1].astype(str) + " " + df[col2].astype(str)

# Drop the first two columns
df = df.drop(columns=[col1, col2])

# Move "Name" to the start
name_col = df.pop(NAME_COLUMN)
df.insert(0, NAME_COLUMN, name_col)

# Save CSV
df.to_csv(OUTPUT_FILE, index=False)

# Show success notification
subprocess.run([
    "osascript", "-e",
    f'display notification "File saved as {OUTPUT_FILE}" with title "{title}"'
])
