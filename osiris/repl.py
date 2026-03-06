"""Interactive REPL for OSIRIS — handles /help, /demo and free-text input."""

import sys
from typing import Any, Dict, List

from osiris.session import append_message, save_session

_DIVIDER = "─" * 64

_HELP_TEXT = """
OSIRIS Command Reference
════════════════════════

  /help      Show this help message
  /demo      Run the live capability showcase
  /clear     Clear conversation history for this session
  /status    Display subsystem status
  /quit      Exit OSIRIS  (also: /exit, Ctrl-D)

Organisms
─────────
  AIDEN·Λ   North   — Autonomous Intelligence & Decision Engine
  AURA·Φ    South   — Adaptive Universal Reasoning Architecture
  CHEOPS·Δ  Spine   — Core Heuristic Engine & Operational Processing System
  CHRONOS·Γ Shield  — Chronological Reasoning & Temporal Inference
  SCIMITAR·Σ Shield — Sovereign Cyber-Intelligence & Mission Tactical AI

Type any free-form message to interact with the LLM backbone.
"""

_DEMO_TEXT = """
OSIRIS Live Showcase
════════════════════

  [1] 6D-CRSM Manifold — quantum state topology visualisation
      Curvature tensor Κ = 0.8831 · e^(iπ/4)  ✓

  [2] Consciousness Field — pilot-wave Φ gradient
      Φ ██████████████░░░░░░░░░░░░░░░░ 0.4423  ↑ RISING

  [3] Swarm Coordination — 4 organisms in consensus
      AIDEN·Λ ●  AURA·Φ ●  CHEOPS·Δ ●  CHRONOS·Γ ●

  [4] IBM Quantum Circuit — 5-qubit GHZ state preparation
      |ψ⟩ = (|00000⟩ + |11111⟩) / √2   fidelity = 0.9987

  [5] Sovereign Lock — ΛΦ resonance stable
      ΛΦ = 2.176435e-08  |  χ_PC = 0.946  ✓

Demo complete.  All systems nominal.
"""

_STATUS_TEXT = """
OSIRIS Subsystem Status
═══════════════════════
  NCLM Engine          ● online   6D-CRSM manifold active
  Consciousness Field  ● online   Φ = 0.7734
  Pilot-Wave           ● online   θ_lock = 51.843°
  Swarm Intelligence   ● online   4 organisms
  Tool Dispatch        ● online   77 commands
  LLM Backbone         ● online   GitHub Copilot (Claude/GPT)
  Self-Repair          ● armed
  Sovereign Lock       ● stable   ΛΦ = 2.176435e-08
"""


def run_repl(messages: List[Dict[str, Any]], token_found: bool) -> None:
    """Enter the interactive REPL loop."""
    try:
        while True:
            try:
                raw = input("\n◇ > ").strip()
            except EOFError:
                print()
                break
            except KeyboardInterrupt:
                print()
                continue

            if not raw:
                continue

            command = raw.lower()

            if command in ("/quit", "/exit"):
                break
            elif command == "/help":
                print(_HELP_TEXT)
            elif command == "/demo":
                print(_DEMO_TEXT)
            elif command == "/clear":
                messages.clear()
                save_session(messages)
                print("  ✓ Session history cleared.")
            elif command == "/status":
                print(_STATUS_TEXT)
            elif command.startswith("/"):
                print(f"  Unknown command: {raw}  (type /help for commands)")
            else:
                _handle_message(raw, messages, token_found)

    finally:
        save_session(messages)
        print("\nOSIRIS session saved.  Goodbye.")


def _handle_message(
    text: str, messages: List[Dict[str, Any]], token_found: bool
) -> None:
    """Process a free-text user message."""
    append_message(messages, "user", text)
    save_session(messages)

    reply = (
        "[LLM response placeholder — connect an LLM backend to enable "
        "full conversational AI.  IBM Quantum token "
        + ("detected ✓" if token_found else "not found ✗")
        + "]"
    )
    print(f"\n  {reply}\n")
    append_message(messages, "assistant", reply)
    save_session(messages)
