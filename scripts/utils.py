import os
import urllib.parse
import json
import shlex


#######################################
# get the icon based on its specific tag
# cache the icon map
_icon_map = None

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



####################################################
# added this section to keep above code and logic in tact | Fri, Jul 25 2025


def filter_contact(content: str, query: str, display_fields: list[str]) -> bool:
    # Build name and full_text like list_contacts did
    fields = {}
    for line in content.splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            fields[k.strip()] = v.strip()

    name = fields.get("Name", "")
    subtitle_parts = [fields.get(f, "—") for f in display_fields]
    full_text = f"{name} {' '.join(subtitle_parts)}"

    # Decide match
    if is_structured_query(query):
        return matches_structured(content, name, query)
    else:
        return matches_terms(full_text, query)




def is_structured_query(query: str) -> bool:
    """Returns True if query contains has:, !has:, or field:value logic."""
    q = (query or "").lower()
    return any(op in q for op in ("has:", "!has:")) or ":" in q


def matches_has(content: str, name: str, raw_query: str) -> bool:
    import shlex

    # Build normalized field dictionary
    fields = {}
    for line in content.splitlines():
        if ":" not in line:
            continue
        k, v = line.split(":", 1)
        key = k.strip()
        val = v.strip()
        fields[key] = val
        fields[key.lower()] = val
        fields[key.lower().replace(" ", "_")] = val
    fields["name"] = name

    def _truthy(value):
        if value is None:
            return False
        if isinstance(value, str):
            return value.strip() != ""
        if isinstance(value, (list, tuple, set)):
            return any(bool(x) for x in value)
        return bool(value)

    tokens = shlex.split(raw_query or "")
    i = 0
    while i < len(tokens):
        tok = tokens[i].lower()
        # Merge following tokens if "has:" or "!has:" is incomplete
        if tok.startswith("has:") or tok.startswith("!has:"):
            prefix = "has:" if tok.startswith("has:") else "!has:"
            field_name = tok[len(prefix):].strip()
            j = i + 1
            while j < len(tokens) and not any(tokens[j].lower().startswith(x) for x in ("has:", "!has:")):
                field_name += " " + tokens[j]
                j += 1
            field_name = field_name.strip().replace(" ", "_")
            if prefix == "has:":
                if not _truthy(fields.get(field_name)):
                    return False
            else:
                if _truthy(fields.get(field_name)):
                    return False
            i = j
        else:
            i += 1
    return True



def matches_structured(content: str, name: str, raw_query: str) -> bool:
    import shlex

    # Build normalized field dictionary
    fields = {}
    for line in content.splitlines():
        if ":" not in line:
            continue
        k, v = line.split(":", 1)
        key = k.strip()
        val = v.strip()
        fields[key] = val
        fields[key.lower()] = val
        fields[key.lower().replace(" ", "_")] = val
    fields["name"] = name

    def _truthy(value):
        if value is None:
            return False
        if isinstance(value, str):
            return value.strip() != ""
        if isinstance(value, (list, tuple, set)):
            return any(bool(x) for x in value)
        return bool(value)

    tokens = shlex.split(raw_query or "")

    # --- FIX: rebuild tokens so "field: value" & "field:value" both work ---
    rebuilt = []
    i = 0
    carry = []
    while i < len(tokens):
        t = tokens[i]

        # handle has:/!has: first (allow multi-word fields)
        tl = t.lower()
        if tl.startswith("has:") or tl.startswith("!has:"):
            prefix = "has:" if tl.startswith("has:") else "!has:"
            field_name = t[len(prefix):]
            j = i + 1
            while j < len(tokens) and ":" not in tokens[j] and not tokens[j].lower().startswith(("has:", "!has:")):
                field_name += " " + tokens[j]
                j += 1
            rebuilt.append(prefix + field_name)
            i = j
            carry = []
            continue

        # if token has a colon somewhere
        if ":" in t:
            left, right = t.split(":", 1)
            field_bits = carry + [left]
            carry = []

            # if value part is empty (i.e. token ended with ':'), pull from following tokens
            if right.strip() == "":
                j = i + 1
                vals = []
                while j < len(tokens) and ":" not in tokens[j] and not tokens[j].lower().startswith(("has:", "!has:")):
                    vals.append(tokens[j])
                    j += 1
                rebuilt.append(f'{" ".join(field_bits)}:{ " ".join(vals) }'.strip())
                i = j
            else:
                rebuilt.append(f'{" ".join(field_bits)}:{right}'.strip())
                i += 1
            continue

        # otherwise, accumulate as possible field-name parts
        carry.append(t)
        i += 1

    if carry:
        rebuilt.extend(carry)

    tokens = rebuilt
    # ---------------------------------------------------------

    i = 0
    while i < len(tokens):
        tok = tokens[i]

        # --- HAS / !HAS ---
        if tok.lower().startswith("has:") or tok.lower().startswith("!has:"):
            prefix = "has:" if tok.lower().startswith("has:") else "!has:"
            field_name = tok[len(prefix):].strip().replace(" ", "_").lower()
            if prefix == "has:":
                if not _truthy(fields.get(field_name)):
                    return False
            else:
                if _truthy(fields.get(field_name)):
                    return False
            i += 1
            continue

        # --- FIELD MATCH (field:value) ---
        if ":" in tok:
            field, val = tok.split(":", 1)
            field_key = field.strip().replace(" ", "_").lower()
            field_val = str(fields.get(field_key, "")).lower()
            val = val.strip('"').lower()

            # Exact match if query contains quotes
            exact = f'{field}:"{val}"'.lower() in raw_query.lower()
            if exact:
                if field_val != val:
                    return False
            else:
                if val not in field_val:
                    return False
            i += 1
            continue

        i += 1

    return True



# run this line to test the quesries below: python3 -c "import utils; utils.test_queries()"

def test_queries():
    """Quick test for matches_structured queries."""
    sample_content = """Name: Jane Doe
Email: jane.doe@gmail.com
Next Action: Complete payment
Company: Acme Corp
"""
    sample_name = "Jane Doe"

    test_cases = [
        'next action:complete',
        'next action: complete',
        '"next action": complete',
        'name:"Jane Doe"',
        'email:gmail.com',
        'company:Acme',
        'company:"Acme Corp"',
        'has:company',
        '!has:phone',
    ]

    print("=== Testing matches_structured ===")
    for q in test_cases:
        result = matches_structured(sample_content, sample_name, q)
        print(f"{q:<30} -> {result}")
