"""Compatibility entry point for the bundled Agent Skill generator."""

from __future__ import annotations

import runpy
from pathlib import Path


_IMPLEMENTATION = (
    Path(__file__).resolve().parent
    / "skills"
    / "store-listing-screenshots"
    / "scripts"
    / "generate.py"
)
_NAMESPACE = runpy.run_path(str(_IMPLEMENTATION))
globals().update({name: value for name, value in _NAMESPACE.items() if not name.startswith("__")})


if __name__ == "__main__":
    raise SystemExit(main())
