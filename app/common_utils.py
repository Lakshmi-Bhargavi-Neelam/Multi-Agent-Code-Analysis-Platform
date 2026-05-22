import json
from typing import Any


def safe_json(data: Any) -> str:
    """
    Safely convert object to pretty JSON string.
    """
    try:
        return json.dumps(data, indent=2, default=str)
    except Exception:
        return str(data)


def append_error(state, error_message: str):
    """
    Append error to workflow state.
    """
    if "errors" not in state:
        state["errors"] = []

    state["errors"].append(error_message)
    return state