import json
import re
from typing import Any, Dict, List


def extract_json(text: str) -> Dict[str, Any]:
    text = text.strip()

    # Remove code fences if present
    text = re.sub(r"^```(?:json)?\s*|\s*```$", "", text.strip(), flags=re.IGNORECASE)

    # Try direct parse
    try:
        return json.loads(text)
    except Exception:
        pass

    # Find first JSON object
    match = re.search(r"\{.*\}", text, flags=re.DOTALL)
    if match:
        candidate = match.group(0).strip()

        # Remove trailing commas
        candidate = re.sub(r",\s*([}\]])", r"\1", candidate)

        try:
            return json.loads(candidate)
        except Exception:
            pass

    raise ValueError("Model did not return valid JSON. Try regenerating.")


def ensure_menu_rows(menu: Any) -> List[Dict[str, Any]]:
    """
    Makes sure the menu is a list of dict rows so Streamlit table rendering never crashes.
    """
    if not isinstance(menu, list):
        return []

    out = []
    for row in menu:
        if isinstance(row, dict):
            out.append(row)

    return out