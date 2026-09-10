#!/usr/bin/env bash
set -euo pipefail

# This script creates and uses a local virtual environment (.venv) so the tool
# works consistently across systems without polluting global Python packages.

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="$SCRIPT_DIR/.venv"
SOURCE_DIR="/Volumes/NO NAME/Vybrané"
MAX_SIDE=800
FONT_SIZE=48
WATERMARK_TEXT="Nabídka pro redakci"
WATERMARK_OPACITY=30

# Override defaults by passing arguments, for example:
# ./run_resize.sh --source-dir "/Volumes/NO NAME/Vybrané" --max-side 1200 --font-size 56

# Create venv if missing
if [ ! -d "$VENV_DIR" ]; then
  echo "Creating virtual environment at $VENV_DIR"
  python3 -m venv "$VENV_DIR"
fi

# Use the venv's python to install dependencies and run the script
PYTHON="$VENV_DIR/bin/python"
export PATH="$VENV_DIR/bin:$PATH"

"$PYTHON" -m pip install --upgrade pip
"$PYTHON" -m pip install -r "$SCRIPT_DIR/requirements.txt"

"$PYTHON" "$SCRIPT_DIR/resize_watermark.py" \
  --source-dir "$SOURCE_DIR" \
  --max-side "$MAX_SIDE" \
  --font-size "$FONT_SIZE" \
  --watermark-text "$WATERMARK_TEXT" \
  --watermark-opacity-percent "$WATERMARK_OPACITY" \
  "$@"
