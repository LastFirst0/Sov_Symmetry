#!/usr/bin/env python3
"""
scripts/sovereign_pet.py
=========================
Launch the E8 Tamagotchi virtual pet.

Usage:
    python3 scripts/sovereign_pet.py
    python3 scripts/sovereign_pet.py --name LUMI
    python3 scripts/sovereign_pet.py --reset
    python3 scripts/sovereign_pet.py --status   (no animation, just print vitals)
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

# Ensure project root on path
_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from sov_heart.tamagotchi.e8_pet import E8Pet, DEFAULT_SAVE_PATH
from sov_heart.tamagotchi.pet_cli import PetCLI
from sov_heart.tamagotchi.pet_renderer import _GOLD, _GREEN, _RED, _WHITE, _RESET, _DIM


def main() -> None:
    parser = argparse.ArgumentParser(
        description="E8 Tamagotchi — a living geometric organism in your terminal.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Controls (in-game):
  [f]  Feed   — type text/data to feed your pet
  [p]  Play   — trigger a Weyl reflection interaction
  [s]  Status — print verbose vitals snapshot
  [q]  Quit   — save and exit
        """,
    )
    parser.add_argument("--name",   type=str,  help="Pet name (used on first creation)")
    parser.add_argument("--reset",  action="store_true", help="Delete saved state and start fresh")
    parser.add_argument("--status", action="store_true", help="Print vitals only (no animation)")
    args = parser.parse_args()

    save_path = DEFAULT_SAVE_PATH

    # Handle reset
    if args.reset:
        if save_path.exists():
            save_path.unlink()
            print(f"{_RED}Pet state reset.{_RESET}")
        else:
            print(f"{_DIM}No saved state found.{_RESET}")

    # Load or create
    pet = E8Pet.load_or_create(path=save_path, name=args.name)

    # Status-only mode
    if args.status:
        v = pet.vitals()
        print(f"\n{_GOLD}✦ {v['name'].upper()} — vitals ✦{_RESET}\n")
        for key, val in v.items():
            if isinstance(val, float):
                print(f"  {_DIM}{key:<14}{_RESET} {_WHITE}{val:.4f}{_RESET}")
            else:
                print(f"  {_DIM}{key:<14}{_RESET} {_WHITE}{val}{_RESET}")
        print()
        return

    # Interactive loop
    cli = PetCLI(pet, save_path=save_path)
    cli.run()


if __name__ == "__main__":
    main()
