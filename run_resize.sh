#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
SOURCE_DIR="/Volumes/NO NAME/Vybrané"
MAX_SIDE=800
FONT_SIZE=48
WATERMARK_TEXT="Nabídka pro redakci"
WATERMARK_OPACITY=30

# Override defaults by passing arguments, for example:
# ./run_resize.sh --source-dir "/Volumes/NO NAME/Vybrané" --max-side 1200 --font-size 56

python3 -m pip install --user -r "$SCRIPT_DIR/requirements.txt"

python3 "$SCRIPT_DIR/resize_watermark.py" \
  --source-dir "$SOURCE_DIR" \
  --max-side "$MAX_SIDE" \
  --font-size "$FONT_SIZE" \
  --watermark-text "$WATERMARK_TEXT" \
  --watermark-opacity-percent "$WATERMARK_OPACITY" \
  "$@"
