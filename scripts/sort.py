# sort.py
#
# Parse "sort:" tokens from the query string
# Sort Alfred Script Filter items by a field
# - If the field looks like a date → sort by date
# - Else → sort as text (case-insensitive)
# - Missing values always sink to the bottom
# - Keep first row helper keeps the summary at top

from datetime import datetime
import os

# ---------- Public API ----------

def extract_sort(query: str):
    """
    Get sorting info from a raw query string.

    Supports:
      "search terms sort:<Field Name>"   → ascending
      "search terms -sort:<Field Name>"  → descending

    Returns:
      query       → terms without the sort token
      sort_field  → field name to sort on
      descending  → True if "-sort:" was used
    """
    sort_field, descending = "", False
    lower = query.lower()

    # find sort token once
    if "sort:" in lower or "-sort:" in lower:
        if "-sort:" in lower:
            head, tail = query.split("-sort:", 1)
            descending = True
        else:
            head, tail = query.split("sort:", 1)
        query = head.strip()
        sort_field = tail.strip()

    return query, sort_field, descending


def sort_rows_by_field(rows, key_field, descending=False):
    """
    Sort by date if value parses as a date, else sort as text
    Missing values always sink to the bottom
    """
    def key_fn(r):
        # read raw value from the contact file path in r["arg"]
        path = r.get("arg", "")
        raw = _read_value_from_file(path, key_field)

        # missing value → bottom
        if not raw:
            return (1, 1, "")  # (missing, is_text, value)

        # try date first
        dt = _parse_date(raw)
        if dt is not None:
            return (0, 0, dt)  # dates come before text among non-missing

        # fallback to text (case-insensitive)
        return (0, 1, raw.strip().lower())

    return sorted(rows, key=key_fn, reverse=descending)


def sort_rows_by_date(rows, key_field, descending=False):
    """
    Backward compatible wrapper
    Calls the generic field sorter
    """
    return sort_rows_by_field(rows, key_field, descending=descending)


def sort_items_keep_first(items, key_field, descending=False):
    """
    Keep first row (summary/info) fixed at top
    Sort the remaining contact rows by field (date or text)
    """
    if not items:
        return items
    summary, rows = items[0], items[1:]
    rows = sort_rows_by_field(rows, key_field=key_field, descending=descending)
    return [summary] + rows


# ---------- Helpers ----------

# accepted date formats
_DATE_FORMATS = (
    "%Y-%m-%d",        # 2025-08-25
    "%Y/%m/%d",        # 2025/08/25
    "%Y.%m.%d",        # 2025.08.25
    "%m/%d/%Y",        # 08/25/2025
    "%m/%d/%y",        # 08/25/25
    "%d %b %Y",        # 25 Aug 2025
    "%b %d %Y",        # Aug 25 2025
    "%b %d, %Y",       # Aug 25, 2025
    "%Y-%m-%d %H:%M",  # 2025-08-25 14:30
    "%Y-%m-%dT%H:%M",  # 2025-08-25T14:30
)

def _parse_date(s: str):
    """Try each date format. Return datetime or None."""
    if not s:
        return None
    s = s.strip()
    for fmt in _DATE_FORMATS:
        try:
            return datetime.strptime(s, fmt)
        except Exception:
            pass
    return None

def _read_value_from_file(path: str, field_name: str) -> str:
    """Read raw field value from a contact file. Return '' if not found."""
    if not path or not os.path.exists(path):
        return ""
    try:
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception:
        return ""
    return _get_field_from_text(field_name, content)

def _get_field_from_text(field: str, content: str):
    """
    Find first line starting with "<field>:"
    Case-insensitive. Return text after the colon.
    """
    if not content:
        return ""
    target = f"{field.lower()}:"
    for line in content.splitlines():
        if line.lower().startswith(target):
            return line.split(":", 1)[1].strip()
    return ""
