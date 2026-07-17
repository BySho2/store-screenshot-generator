from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

from PIL import Image


def verify_png(path: Path) -> None:
    if not path.is_file() or path.stat().st_size == 0:
        raise ValueError(f"Screenshot was not created: {path}")
    with Image.open(path) as image:
        image.load()
        if image.format != "PNG":
            raise ValueError(f"Captured file is not PNG: {path} ({image.format})")


def main() -> int:
    parser = argparse.ArgumentParser(description="Capture an iOS Simulator screenshot.")
    parser.add_argument("output", type=Path, help="Destination PNG path")
    parser.add_argument("device", nargs="?", default="booted", help="Simulator UDID or 'booted'")
    args = parser.parse_args()
    if shutil.which("xcrun") is None:
        print("xcrun was not found. Install Xcode and its command-line tools.", file=sys.stderr)
        return 1

    output = args.output.expanduser().resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    try:
        subprocess.run(["xcrun", "simctl", "io", args.device, "screenshot", str(output)], check=True)
        verify_png(output)
    except (OSError, subprocess.CalledProcessError, ValueError) as exc:
        print(f"iOS screenshot capture failed: {exc}", file=sys.stderr)
        return 1
    print(f"Captured iOS Simulator screenshot: {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
