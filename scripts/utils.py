import os
import urllib.parse
import json


###################################
#add items to the recent list/file
def add_to_recent(entry, tag):

    entry = dict(entry)  # make a copy
    entry["tag"] = tag

    recent_path = os.path.join(os.environ["alfred_workflow_data"], "recent.json")

    try:
        with open(recent_path) as f:
            recent = json.load(f)
    except FileNotFoundError:
        recent = []

    # remove duplicate if exists
    recent = [r for r in recent if r.get("uid") != entry.get("uid")]

    # insert to top
    recent.insert(0, entry)

    cap = int(os.environ.get("recent"))
    recent = recent[:cap]

    with open(recent_path, "w") as f:
        json.dump(recent, f, indent=2)




#######################################
# get the icon based on its specific tag
# cache the icon map
_icon_map = None

def get_icon_for_tag(*strings):
    global _icon_map
    if _icon_map is None:
        # load tag_icons from env var
        try:
            _icon_map = json.loads(os.environ["tag_icons"])
        except Exception:
            _icon_map = {}

    for string in strings:
        if not isinstance(string, str):
            continue
        for keyword, filename in _icon_map.items():
            if keyword in string:
                icon_path = os.path.join(os.path.dirname(__file__), "..", "icons", filename)
                return { "path": os.path.abspath(icon_path) }

    return ""



