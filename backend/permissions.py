from typing import List, Tuple, Dict
from database import db
import fnmatch

def method_to_action(method: str) -> str:
    return {
        "GET": "read",
        "POST": "write",
        "PUT": "write",
        "PATCH": "write",
        "DELETE": "delete"
    }.get(method.upper(), "")

def normalize_path(path: str) -> str:
    """
    Convert incoming API path to resource identifier used in DB.
    We remove a leading slash and keep nested segments as-is.
    """
    return path.lstrip("/")

def _specificity_key(pattern: str) -> Tuple[int, int]:
    """
    Higher = more specific.
    1) Count of 'concrete' segments (no wildcard)
    2) Length of pattern (longer is more specific)
    """
    segments = [s for s in pattern.split("/") if s != ""]
    concrete_segments = sum(1 for s in segments if "*" not in s)
    return (concrete_segments, len(pattern))

def _match_rules(user_id: str, action: str, resource: str) -> List[Dict]:
    """
    Fetch and filter rules by action/resource match.
    Supports '*' action and wildcard resource patterns.
    """
    with db() as conn:
        cur = conn.cursor()
        cur.execute("""
            SELECT action, resource, effect
            FROM user_permissions
            WHERE user_id = ?
        """, (user_id,))
        rows = cur.fetchall()

    matches = []
    for a, r, e in rows:
        if a != "*" and a != action:
            continue
        # Use fnmatch against the normalized resource
        if fnmatch.fnmatch(resource, r):
            matches.append({"action": a, "resource": r, "effect": e})

    return matches

def decide(user_id: str, action: str, resource: str) -> Tuple[str, List[Dict]]:
    """
    Authorization decision with precedence:
      - Default DENY
      - Filter matches
      - Choose the highest specificity group (most concrete)
      - If any DENY in the highest group => DENY
      - Else ALLOW
    """
    matches = _match_rules(user_id, action, resource)
    if not matches:
        return "DENY", []

    # Group by specificity; pick the highest group
    # Specificity defined by (# concrete segments, pattern length)
    scored = [(m, _specificity_key(m["resource"])) for m in matches]
    max_key = max(score for _, score in scored)
    best = [m for (m, score) in scored if score == max_key]

    # Deny beats allow within best group
    if any(m["effect"].lower() == "deny" for m in best):
        return "DENY", best

    return "ALLOW", best
