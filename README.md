# Image resize and watermark script

This project contains a small Python CLI that copies photos from a source directory, resizes them so their longer side does not exceed a configured maximum, and adds a centered white watermark with adjustable opacity.

A short helper script is provided to create and use a local virtual environment so the tool is usable on macOS, Linux, and Windows without affecting global Python packages.

Files
- `resize_watermark.py` - main CLI
- `requirements.txt` - Python dependencies (Pillow)
- `run_resize.sh` - POSIX shell script that creates/uses `.venv` and runs the tool
- `run_resize.bat` - Windows batch file equivalent that creates/uses `.venv` and runs the tool

## Quick start (macOS / Linux)

1. Open a terminal and change to the project directory:

```bash
cd /Users/petrpluhar/Documents/Git/resizer
```

2. Run the helper script (it will create a `.venv` folder, install dependencies, then run):

```bash
./run_resize.sh
```

You can pass additional arguments through to the CLI. Example overriding defaults:

```bash
./run_resize.sh --source-dir "/Volumes/NO NAME/Vybrané" --max-side 1000 --watermark-text "Moje značka"
```

## Quick start (Windows)

Open Command Prompt, change to the project directory, then run:

```
cd C:\path\to\resizer
run_resize.bat
```

To pass arguments, append them after the command:

```
run_resize.bat --max-side 1000 --watermark-text "Moje značka"
```

## Direct usage without helper scripts

If preferred, create and activate a virtual environment manually and install requirements:

macOS / Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python resize_watermark.py --source-dir "/Volumes/NO NAME/Vybrané"
```

Windows (Command Prompt):

```
python -m venv .venv
.venv\Scripts\activate
python -m pip install -r requirements.txt
python resize_watermark.py --source-dir "D:\Path\To\Vybrane"
```

## Notes

- Original photos are never modified.
- The script writes resized copies to a sibling `Orezane` folder by default (or the folder specified with `--output-dir`).
- Existing output files are skipped unless `--overwrite` is used.
- Default watermark text: `Nabídka pro redakci` (override with `--watermark-text`).
