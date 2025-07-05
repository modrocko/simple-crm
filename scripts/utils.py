import os
import urllib.parse
import json
import shlex


#######################################
# get the icon based on its specific tag
# cache the icon map
_icon_map = None

import os

def get_icon_for_tag(*strings):
    icons_dir = os.path.join(os.path.dirname(__file__), "..", "icons")

    for string in strings:
        if not isinstance(string, str):
            continue
        for word in string.split():
            tag = word.lstrip("@")
            icon_file = f"{tag}.png"
            icon_path = os.path.join(icons_dir, icon_file)
            if os.path.exists(icon_path):
                return { "path": os.path.abspath(icon_path) }

    return ""




#########################################
# filter logic
def matches_terms(text, raw_query):
    text = text.lower()
    terms = shlex.split(raw_query)  # handles quoted phrases

    include_terms = []
    exclude_terms = []
    current_logic = "AND"

    i = 0
    while i < len(terms):
        term = terms[i]

        if term.upper() == "OR":
            current_logic = "OR"
            i += 1
            continue

        if term.startswith("!") or term.startswith("-"):
            exclude_terms.append(term[1:].lower())
        else:
            include_terms.append(term.lower())

        i += 1

    # Match logic
    if current_logic == "OR":
        include_match = any(term in text for term in include_terms)
    else:
        include_match = all(term in text for term in include_terms)

    exclude_match = any(term in text for term in exclude_terms)

    return include_match and not exclude_match




#########################################
# get query terms
def get_query_terms(query):
    is_or = ":or" in query
    terms = [q for q in query.replace(":or", "").split() if q]
    return is_or, terms




#########################################
# log recently opended items
def add_to_recent(path):
    name = ""

    # === Extract name from file ===
    try:
        with open(path, "r") as f:
            for line in f:
                if line.lower().startswith("name:"):
                    name = line.split(":", 1)[1].strip()
                    break
    except Exception:
        return  # skip if unreadable

    if not name:
        return  # skip if no name

    # === Load recent list ===
    recent_path = os.path.join(os.environ["alfred_workflow_data"], "recent.json")
    try:
        with open(recent_path, "r") as f:
            recent = json.load(f)
    except FileNotFoundError:
        recent = []

    # === Remove duplicates ===
    recent = [r for r in recent if r.get("path") != path]

    # === Add to top ===
    recent.insert(0, { "name": name, "path": path })

    # === Cap the list ===
    cap = int(os.environ["recent"])
    recent = recent[:cap]

    with open(recent_path, "w") as f:
        json.dump(recent, f, indent=2)
