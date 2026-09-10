#!/usr/bin/env python3
"""
Image resize + watermark CLI

Recommended usage: run the provided helper script which creates and uses a
local virtual environment (.venv) and installs dependencies there:

  ./run_resize.sh    # macOS / Linux
  run_resize.bat      # Windows (Command Prompt)

Or create a venv manually and run with that Python. The helper scripts will
create .venv in the project directory if missing and run the tool inside it.

The script never modifies originals — it writes resized copies to the output
directory (default sibling folder "Orezane").
"""

import argparse
import sys
from pathlib import Path
from typing import Optional, Union

from PIL import Image, ImageDraw, ImageFont

SUPPORTED_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".bmp",
    ".gif",
    ".tif",
    ".tiff",
    ".webp",
}

DEFAULT_SOURCE_DIR = "/Volumes/NO NAME/Vybrané"
DEFAULT_OUTPUT_DIR_NAME = "Orezane"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Resize images to a max longest side and add a centered watermark."
    )
    parser.add_argument(
        "--source-dir",
        default=DEFAULT_SOURCE_DIR,
        help="Directory with original photos to copy and resize.",
    )
    parser.add_argument(
        "--output-dir",
        default=None,
        help="Optional output directory. Defaults to a sibling directory named Orezane.",
    )
    parser.add_argument(
        "--max-side",
        type=int,
        default=800,
        help="Maximum allowed size of the larger side of the image in pixels.",
    )
    parser.add_argument(
        "--watermark-text",
        default="Nabídka pro redakci",
        help="Center watermark text to draw on each image.",
    )
    parser.add_argument(
        "--font-size",
        type=int,
        default=48,
        help="Font size used for the centered watermark.",
    )
    parser.add_argument(
        "--watermark-opacity-percent",
        type=float,
        default=30.0,
        help="Watermark opacity percentage from 0 to 100.",
    )
    parser.add_argument(
        "--font-path",
        default="",
        help="Optional path to a .ttf or .otf font file for the watermark.",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Overwrite images already present in the output directory.",
    )
    return parser.parse_args()


def resolve_output_dir(source_dir: Path, output_dir: Optional[str]) -> Path:
    if output_dir:
        return Path(output_dir).expanduser().resolve()
    return source_dir.parent / DEFAULT_OUTPUT_DIR_NAME


def find_font(font_path: str, font_size: int) -> Union[ImageFont.FreeTypeFont, ImageFont.ImageFont]:
    if font_path:
        font_file = Path(font_path).expanduser()
        if not font_file.exists():
            raise FileNotFoundError(f"Font file not found: {font_file}")
        return ImageFont.truetype(str(font_file), size=font_size)

    candidates = [
        "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
        "/Library/Fonts/Arial.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf",
    ]
    for candidate in candidates:
        if Path(candidate).exists():
            return ImageFont.truetype(candidate, size=font_size)

    return ImageFont.load_default()


def detect_orientation(image: Image.Image) -> str:
    width, height = image.size
    return "landscape" if width >= height else "portrait"


def resize_to_max_side(image: Image.Image, max_side: int) -> Image.Image:
    width, height = image.size
    longer_side = max(width, height)
    orientation = detect_orientation(image)
    if longer_side <= max_side:
        return image.copy()

    scale = max_side / longer_side
    new_width = max(1, int(round(width * scale)))
    new_height = max(1, int(round(height * scale)))
    if orientation == "landscape":
        return image.resize((new_width, new_height), Image.Resampling.LANCZOS)
    return image.resize((new_width, new_height), Image.Resampling.LANCZOS)


def add_centered_watermark(
    image: Image.Image,
    text: str,
    font: Union[ImageFont.FreeTypeFont, ImageFont.ImageFont],
    opacity_percent: float,
) -> Image.Image:
    if opacity_percent < 0:
        opacity_percent = 0
    if opacity_percent > 100:
        opacity_percent = 100

    opacity = int(round((opacity_percent / 100.0) * 255))

    source = image.convert("RGBA")
    overlay = Image.new("RGBA", source.size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(overlay)

    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    x = (source.width - text_width) / 2 - bbox[0]
    y = (source.height - text_height) / 2 - bbox[1]

    draw.text((x, y), text, font=font, fill=(255, 255, 255, opacity))
    merged = Image.alpha_composite(source, overlay)

    if image.mode in {"RGB", "L", "CMYK"}:
        return merged.convert("RGB")
    return merged


def process_image(path: Path, output_dir: Path, max_side: int, watermark_text: str, font_size: int, opacity_percent: float, font_path: str, overwrite: bool) -> None:
    output_path = output_dir / path.name
    if output_path.exists() and not overwrite:
        print(f"Skipping existing output: {output_path}")
        return

    with Image.open(path) as src:
        image = src.copy()
        resized = resize_to_max_side(image, max_side)
        font = find_font(font_path, font_size)
        watermarked = add_centered_watermark(resized, watermark_text, font, opacity_percent)

        extension_map = {
            ".jpg": "JPEG",
            ".jpeg": "JPEG",
            ".png": "PNG",
            ".bmp": "BMP",
            ".gif": "GIF",
            ".tif": "TIFF",
            ".tiff": "TIFF",
            ".webp": "WEBP",
        }
        file_format = extension_map.get(path.suffix.lower(), "JPEG")
        watermarked.save(output_path, format=file_format)

    print(f"Created: {output_path}")


def main() -> int:
    args = parse_args()

    source_dir = Path(args.source_dir).expanduser()
    if not source_dir.exists():
        print(f"Source directory does not exist: {source_dir}", file=sys.stderr)
        return 2
    if not source_dir.is_dir():
        print(f"Source path is not a directory: {source_dir}", file=sys.stderr)
        return 2

    output_dir = resolve_output_dir(source_dir, args.output_dir)
    if output_dir.resolve() == source_dir.resolve():
        print("Output directory must be different from the source directory.", file=sys.stderr)
        return 2
    output_dir.mkdir(parents=True, exist_ok=True)

    image_count = 0
    for item in sorted(source_dir.iterdir()):
        if item.is_file() and item.suffix.lower() in SUPPORTED_EXTENSIONS:
            process_image(
                item,
                output_dir,
                args.max_side,
                args.watermark_text,
                args.font_size,
                args.watermark_opacity_percent,
                args.font_path,
                args.overwrite,
            )
            image_count += 1

    if image_count == 0:
        print(f"No image files found in {source_dir}")
    else:
        print(f"Completed. Resized copies saved to {output_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
