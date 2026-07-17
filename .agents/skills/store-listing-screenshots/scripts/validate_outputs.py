from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

import yaml
from PIL import Image


PRESETS = {
    "app-store-iphone-6.9": (1320, 2868),
    "app-store-iphone-6.5": (1242, 2688),
    "google-play-phone-portrait": (1080, 1920),
}


class ValidationError(ValueError):
    pass


def load_config(path: Path) -> dict[str, Any]:
    if not path.is_file():
        raise ValidationError(f"Config file not found: {path}")
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValidationError(f"Expected a YAML object: {path}")
    return data


def resolve_path(base: Path, raw: str) -> Path:
    value = Path(raw).expanduser()
    return value if value.is_absolute() else (base / value).resolve()


def expected_files(config_path: Path, config: dict[str, Any]) -> list[tuple[Path, tuple[int, int]]]:
    locales = config.get("locales")
    slides = config.get("slides")
    outputs = config.get("outputs")
    if not isinstance(locales, list) or not locales:
        raise ValidationError("'locales' must be a non-empty list")
    if not isinstance(slides, list) or not slides:
        raise ValidationError("'slides' must be a non-empty list")
    if not isinstance(outputs, list) or not outputs:
        raise ValidationError("'outputs' must be a non-empty list")

    result: list[tuple[Path, tuple[int, int]]] = []
    for output in outputs:
        if not isinstance(output, dict):
            raise ValidationError("Each output must be an object")
        preset = str(output.get("preset", ""))
        if preset not in PRESETS:
            raise ValidationError(f"Unknown output preset: {preset}")
        directory = output.get("directory")
        if not directory:
            raise ValidationError("Output directory is missing")
        output_dir = resolve_path(config_path.parent, str(directory))
        filename = str(output.get("filename", "screenshot_{locale}_{index:02d}.png"))
        for locale in locales:
            for index in range(1, len(slides) + 1):
                try:
                    rendered_name = filename.format(locale=locale, index=index)
                except (KeyError, ValueError) as exc:
                    raise ValidationError(f"Invalid filename template: {filename}") from exc
                result.append((output_dir / str(locale) / rendered_name, PRESETS[preset]))
    return result


def validate_image(path: Path, expected_size: tuple[int, int]) -> None:
    if not path.is_file():
        raise ValidationError(f"Expected output is missing: {path}")
    try:
        with Image.open(path) as image:
            image.load()
            if image.format != "PNG":
                raise ValidationError(f"Output is not PNG: {path} ({image.format})")
            if image.size != expected_size:
                raise ValidationError(
                    f"Unexpected dimensions: {path} ({image.size[0]}x{image.size[1]}, "
                    f"expected {expected_size[0]}x{expected_size[1]})"
                )
            if image.mode != "RGB":
                raise ValidationError(f"Output must use RGB mode: {path} ({image.mode})")
    except OSError as exc:
        raise ValidationError(f"Unreadable image: {path}: {exc}") from exc


def run(config_path: Path) -> int:
    config_path = config_path.expanduser().resolve()
    config = load_config(config_path)
    files = expected_files(config_path, config)
    for path, expected_size in files:
        validate_image(path, expected_size)
    print(f"Validated {len(files)} generated PNG files from {config_path}")
    return len(files)


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate generated store listing images.")
    parser.add_argument("--config", required=True, type=Path, help="Path to the generation config YAML")
    args = parser.parse_args()
    try:
        run(args.config)
    except (ValidationError, yaml.YAMLError) as exc:
        print(f"Validation failed: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
