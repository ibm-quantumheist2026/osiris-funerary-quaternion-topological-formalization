"""IBM Quantum token auto-discovery utilities."""

import configparser
import os
from pathlib import Path
from typing import Optional


# Environment variables to probe, in priority order
_ENV_VARS = [
    "IBM_QUANTUM_TOKEN",
    "QISKIT_IBM_TOKEN",
    "IBMQ_TOKEN",
]

# Config file paths to probe
_CONFIG_PATHS = [
    Path.home() / ".qiskit" / "qiskitrc",
    Path.home() / ".ibm" / "quantum" / "qiskitrc",
    Path.home() / ".osiris" / "config",
]


def discover_ibm_quantum_token() -> Optional[str]:
    """Return the IBM Quantum API token if one can be found, else None.

    Checks environment variables first, then well-known config files.
    """
    for var in _ENV_VARS:
        value = os.environ.get(var)
        if value:
            return value

    for config_path in _CONFIG_PATHS:
        token = _read_token_from_config(config_path)
        if token:
            return token

    return None


def _read_token_from_config(path: Path) -> Optional[str]:
    """Parse a qiskitrc-style INI file and return the token value."""
    if not path.is_file():
        return None
    try:
        parser = configparser.ConfigParser()
        parser.read(str(path))
        for section in parser.sections():
            for key in ("token", "api_token", "ibm_quantum_token"):
                if parser.has_option(section, key):
                    value = parser.get(section, key).strip()
                    if value:
                        return value
    except Exception:
        pass
    return None


def redact_token(token: str) -> str:
    """Return a partially redacted representation of a token string.

    Tokens longer than 8 characters show the first 8 characters followed by
    '...'.  Shorter tokens are fully masked as '***' to avoid leaking short
    secrets.
    """
    if len(token) > 8:
        return token[:8] + "..."
    return "***"
