#!/usr/bin/env python3

import os
import sys
import subprocess
import utils

# Skip if action is meant for save_search
if os.environ.get("action") == "save_search":
    sys.exit(0)

# Open the file if input exists
path = sys.argv[1] if len(sys.argv) > 0 else ""
if path and os.path.exists(path):
    utils.add_to_recent(path)
    subprocess.run(["open", path])