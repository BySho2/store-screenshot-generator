#!/usr/bin/env python3
from __future__ import annotations

import argparse
import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps


BACKGROUND = "#F3F4F6"
CARD = "#FFFFFF"
TEXT = "#111827"
PADDING = 48
GAP = 28
LABEL_HEIGHT = 44
THUMBNAIL_HEIGHT = 720


def collect_images(input_dir: Path, output: Path) -> list[Path]:
    if not input_dir.is_dir():
        raise ValueError(f"Input directory not found: {input_dir}")
    output = output.resolve()
    images = sorted(
        path for path in input_dir.rglob("*.png") if path.resolve() != output
    )
    if not images:
        raise ValueError(f"No PNG images found under: {input_dir}")
    return images


def make_thumbnail(path: Path) -> Image.Image:
    with Image.open(path) as source:
        image = ImageOps.exif_transpose(source).convert("RGB")
        width = max(1, round(image.width * THUMBNAIL_HEIGHT / image.height))
        return image.resize((width, THUMBNAIL_HEIGHT), Image.Resampling.LANCZOS)


def create_contact_sheet(
    image_paths: list[Path], output: Path, columns: int = 3, title: str = ""
) -> Path:
    if columns < 1:
        raise ValueError("Columns must be at least 1")

    thumbnails = [(path, make_thumbnail(path)) for path in image_paths]
    cell_width = max(image.width for _, image in thumbnails) + GAP * 2
    cell_height = THUMBNAIL_HEIGHT + LABEL_HEIGHT + GAP * 2
    title_height = 64 if title else 0
    rows = math.ceil(len(thumbnails) / columns)
    width = PADDING * 2 + cell_width * columns + GAP * (columns - 1)
    height = PADDING * 2 + title_height + cell_height * rows + GAP * (rows - 1)

    sheet = Image.new("RGB", (width, height), BACKGROUND)
    draw = ImageDraw.Draw(sheet)
    font = ImageFont.load_default()
    if title:
        draw.text((PADDING, PADDING), title, fill=TEXT, font=font)

    top = PADDING + title_height
    for index, (path, image) in enumerate(thumbnails):
        row, column = divmod(index, columns)
        left = PADDING + column * (cell_width + GAP)
        cell_top = top + row * (cell_height + GAP)
        draw.rounded_rectangle(
            (left, cell_top, left + cell_width, cell_top + cell_height),
            radius=18,
            fill=CARD,
        )
        image_left = left + (cell_width - image.width) // 2
        sheet.paste(image, (image_left, cell_top + GAP))
        label = path.name
        label_box = draw.textbbox((0, 0), label, font=font)
        label_width = label_box[2] - label_box[0]
        draw.text(
            (left + (cell_width - label_width) // 2, cell_top + GAP + THUMBNAIL_HEIGHT + 14),
            label,
            fill=TEXT,
            font=font,
        )

    output.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(output, format="PNG")
    return output


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create a visual QA contact sheet from PNG files.")
    parser.add_argument("--input-dir", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--columns", type=int, default=3)
    parser.add_argument("--title", default="")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        images = collect_images(args.input_dir, args.output)
        result = create_contact_sheet(images, args.output, args.columns, args.title)
    except (OSError, ValueError) as error:
        raise SystemExit(str(error)) from error
    print(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
