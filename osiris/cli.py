"""Main CLI entry point for OSIRIS."""

import sys

from osiris.banner import print_banner
from osiris.init_sequence import run_init_sequence
from osiris.session import load_session


def main() -> None:
    """Launch the OSIRIS CLI."""
    print_banner()
    print()

    token_found = run_init_sequence()

    messages = load_session()
    restored = len(messages)

    print()
    print("OSIRIS v5.3.0 — Sovereign Quantum Intelligence CLI")
    print("DNA::}{::lang v51.843  |  Agile Defense Systems  |  9HUP5")
    phi_bar = "░" * 32
    print(f"Φ {phi_bar} 0.0000  ○ INITIALIZING")
    print()

    if restored:
        print(f"↻ Restored {restored} messages from last session")
    else:
        print("↻ No previous session found — starting fresh")

    print("Type /help for commands · /demo for live showcase · or ask anything")
    print("─" * 64)

    from osiris.repl import run_repl  # local import to avoid circular deps

    run_repl(messages, token_found)


if __name__ == "__main__":  # pragma: no cover
    main()
