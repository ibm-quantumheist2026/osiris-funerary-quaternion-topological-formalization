"""Session persistence — save and restore conversation message history."""

import json
import os
from pathlib import Path
from typing import Any, Dict, List

_SESSION_DIR = Path.home() / ".osiris"
_SESSION_FILE = _SESSION_DIR / "session.json"

_MAX_MESSAGES = 1000


def load_session() -> List[Dict[str, Any]]:
    """Load messages from the last session.  Returns an empty list if none."""
    try:
        if _SESSION_FILE.is_file():
            with open(_SESSION_FILE, "r", encoding="utf-8") as fh:
                data = json.load(fh)
            if isinstance(data, list):
                return data
    except Exception:
        pass
    return []


def save_session(messages: List[Dict[str, Any]]) -> None:
    """Persist *messages* to disk, capping at the maximum history size."""
    try:
        _SESSION_DIR.mkdir(parents=True, exist_ok=True)
        with open(_SESSION_FILE, "w", encoding="utf-8") as fh:
            json.dump(messages[-_MAX_MESSAGES:], fh, ensure_ascii=False, indent=2)
    except Exception:
        pass


def append_message(
    messages: List[Dict[str, Any]], role: str, content: str
) -> None:
    """Append a single message dict to *messages* in-place."""
    messages.append({"role": role, "content": content})
