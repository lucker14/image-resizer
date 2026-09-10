# Image resize and watermark script

This project contains a small Python CLI that copies photos from a source directory, resizes them so their longer side does not exceed a configured maximum, and adds a centered white watermark with adjustable opacity.

## Usage

```bash
python3 resize_watermark.py \
  --source-dir "/Volumes/NO NAME/Vybrané" \
  --max-side 800 \
  --font-size 48 \
  --watermark-opacity-percent 30 \
  --watermark-text "Nabídka pro redakci"
```

A sibling directory named `Orezane` is created automatically unless `--output-dir` is provided.

## Notes

- Original photos are never modified.
- The script writes resized copies to the output directory.
- The output directory is created automatically if missing.
- Existing output files are skipped unless `--overwrite` is used.

## Install dependencies

```bash
python3 -m pip install -r requirements.txt
```
# image-resizer
