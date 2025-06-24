import os
import urllib.parse
import json



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



#######################################
def parse_query(raw_query):
    """Split the query & detect :or mode"""
    is_or = ":or" in raw_query
    terms = [q for q in raw_query.replace(":or", "").split() if q]
    return is_or, terms


#######################################
def matches_terms(text, terms, is_or):
    """Return True if text matches all or any terms"""
    text = text.lower()
    if is_or:
        return any(term in text for term in terms)
    return all(term in text for term in terms)

#######################################
def get_query_terms(query):
    is_or = ":or" in query
    terms = [q for q in query.replace(":or", "").split() if q]
    return is_or, terms
