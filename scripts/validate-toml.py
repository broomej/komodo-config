#!/usr/bin/env python3
"""Validate every .toml file in the repo parses cleanly.

Uses tomllib (Python 3.11+ stdlib) — no pip install needed.

Run locally:
    python scripts/validate-toml.py

Run in CI:
    python scripts/validate-toml.py   # exit 0 = all OK, exit 1 = at least one failure
"""
import sys
import tomllib
from pathlib import Path


def main() -> int:
    # Repo root is one level up from this script's directory.
    root = Path(__file__).resolve().parent.parent

    toml_files = sorted(root.rglob("*.toml"))

    # Skip any vendored / cloned external TOML that isn't ours.
    toml_files = [
        f for f in toml_files
        if not any(
            part in f.parts
            for part in {".git", "node_modules", ".venv", "venv", "__pycache__"}
        )
    ]

    if not toml_files:
        print("No .toml files found.")
        return 0

    failures = 0
    for f in toml_files:
        rel = f.relative_to(root)
        try:
            with open(f, "rb") as fh:
                tomllib.load(fh)
            print(f"  OK    {rel}")
        except tomllib.TOMLDecodeError as e:
            print(f"  FAIL  {rel}")
            print(f"        {e}")
            failures += 1
        except OSError as e:
            print(f"  FAIL  {rel}  (unreadable: {e})")
            failures += 1

    if failures:
        print(f"\n{failures} file(s) failed validation.")
    else:
        print(f"\nAll {len(toml_files)} file(s) valid.")

    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
