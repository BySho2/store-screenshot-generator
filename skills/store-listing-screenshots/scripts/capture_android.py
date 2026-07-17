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
    parser = argparse.ArgumentParser(description="Capture an Android device or emulator screenshot.")
    parser.add_argument("output", type=Path, help="Destination PNG path")
    parser.add_argument("device_serial", nargs="?", help="Optional adb device serial")
    args = parser.parse_args()
    if shutil.which("adb") is None:
        print("adb was not found. Install Android SDK Platform Tools.", file=sys.stderr)
        return 1

    command = ["adb"]
    if args.device_serial:
        command.extend(["-s", args.device_serial])
    command.extend(["exec-out", "screencap", "-p"])
    output = args.output.expanduser().resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    try:
        result = subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output.write_bytes(result.stdout)
        verify_png(output)
    except (OSError, subprocess.CalledProcessError, ValueError) as exc:
        print(f"Android screenshot capture failed: {exc}", file=sys.stderr)
        return 1
    print(f"Captured Android screenshot: {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
