"""ASCII banner for the OSIRIS splash screen."""

BANNER = (
    "┌───────────────────────────────────────────────────────────────┐\n"
    "│                                                               │\n"
    "│  ╔══════════╗   ██████╗ ███████╗██╗██████╗ ██╗███████╗   │\n"
    "│  ║  DNA     ║  ██╔═══██╗██╔════╝██║██╔══██╗██║██╔════╝   │\n"
    "│  ║ ::}{{}::  ║  ██║   ██║███████╗██║██████╔╝██║███████╗   │\n"
    "│  ║  lang    ║  ██║   ██║╚════██║██║██╔══██╗██║╚════██║   │\n"
    "│  ╚══════════╝  ╚██████╔╝███████║██║██║  ██║██║███████║   │\n"
    "│   v51.843        ╚═════╝ ╚══════╝╚═╝╚═╝  ╚═╝╚═╝╚══════╝   │\n"
    "│                                                               │\n"
    "│  ⚛  Omega System Integrated Runtime Intelligence System  ⚛   │\n"
    "│     Agile Defense Systems  │  CAGE 9HUP5  │  Gen 5.3         │\n"
    "│                                                               │\n"
    "│  AIDEN·Λ  AURA·Φ  CHEOPS·Δ  CHRONOS·Γ  SCIMITAR·Σ    │\n"
    "│  ╰─North─╯  ╰South─╯  ╰──Spine──╯  ╰─────Shield────╯    │\n"
    "│                                                               │\n"
    "└───────────────────────────────────────────────────────────────┘"
)


def print_banner() -> None:
    """Print the OSIRIS ASCII art banner."""
    print(BANNER)
