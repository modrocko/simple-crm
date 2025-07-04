import os
import urllib.parse
import json
import shlex


#######################################
# get the icon based on its specific tag
# cache the icon map
_icon_map = None

def get_icon_for_tag(*strings):
    global _icon_map
    if _icon_map is None:
        try:
            _icon_map = json.loads(os.environ["tag_icons"])
        except Exception:
            _icon_map = {}

    for string in strings:
        if not isinstance(string, str):
            continue
        for word in string.split():
            for keyword, filename in _icon_map.items():
                if keyword == word:
                    icon_path = os.path.join(os.path.dirname(__file__), "..", "icons", filename)
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
