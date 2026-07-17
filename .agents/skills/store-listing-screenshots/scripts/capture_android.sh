#!/bin/sh
set -eu

if [ "$#" -lt 1 ] || [ "$#" -gt 2 ]; then
  echo "Usage: $0 <output.png> [device-serial]" >&2
  exit 2
fi

if ! command -v adb >/dev/null 2>&1; then
  echo "adb was not found. Install Android SDK Platform Tools." >&2
  exit 1
fi

output_path=$1
device_serial=${2:-}
output_dir=$(dirname "$output_path")
mkdir -p "$output_dir"

if [ -n "$device_serial" ]; then
  adb -s "$device_serial" exec-out screencap -p > "$output_path"
else
  adb exec-out screencap -p > "$output_path"
fi

if [ ! -s "$output_path" ]; then
  echo "Screenshot was not created: $output_path" >&2
  exit 1
fi

echo "Captured Android screenshot: $output_path"
