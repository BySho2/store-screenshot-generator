#!/bin/sh
set -eu

if [ "$#" -lt 1 ] || [ "$#" -gt 2 ]; then
  echo "Usage: $0 <output.png> [device-udid-or-booted]" >&2
  exit 2
fi

if ! command -v xcrun >/dev/null 2>&1; then
  echo "xcrun was not found. Install Xcode and its command-line tools." >&2
  exit 1
fi

output_path=$1
device_id=${2:-booted}
output_dir=$(dirname "$output_path")
mkdir -p "$output_dir"

xcrun simctl io "$device_id" screenshot "$output_path"

if [ ! -s "$output_path" ]; then
  echo "Screenshot was not created: $output_path" >&2
  exit 1
fi

echo "Captured iOS Simulator screenshot: $output_path"
