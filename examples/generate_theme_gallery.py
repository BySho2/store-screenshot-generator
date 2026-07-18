"""Regenerate the README theme gallery from the shared demo screenshot."""

from __future__ import annotations

import shutil
import sys
import tempfile
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import generate  # noqa: E402


GALLERY_DIR = ROOT / "examples" / "theme-gallery"
THEMES = (
    "modern-gradient",
    "minimal-light",
    "premium-navy",
    "sunny-yellow",
    "dark-neon",
    "soft-pastel",
)


def gallery_config(theme: str, output_dir: Path) -> dict:
    return {
        "app": {"name": {"ja": "Demo App"}},
        "locales": ["ja"],
        "outputs": [
            {
                "name": "app-store",
                "preset": "app-store-iphone-6.9",
                "directory": str(output_dir),
                "filename": f"{theme}.png",
                "device": {
                    "frame": "generic",
                    "corner_radius_ratio": 0.105,
                    "bezel_ratio": 0.022,
                },
            }
        ],
        "theme": str(ROOT / "themes" / f"{theme}.yaml"),
        "fonts": {
            "ja": {
                "title": None,
                "body": None,
            }
        },
        "slides": [
            {
                "screenshot": str(ROOT / "examples" / "screenshots" / "home.png"),
                "text": {
                    "ja": {
                        "title": "毎日のタスクを\nひとつの画面で",
                        "body": "必要な情報をすばやく確認し、次の行動へ進めます。",
                    }
                },
            }
        ],
    }


def main() -> None:
    GALLERY_DIR.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as directory:
        temporary = Path(directory)
        for theme in THEMES:
            config_path = temporary / f"{theme}.yaml"
            output_dir = temporary / theme
            config_path.write_text(
                yaml.safe_dump(gallery_config(theme, output_dir), allow_unicode=True, sort_keys=False),
                encoding="utf-8",
            )
            [generated] = generate.run(config_path, overwrite=True)
            destination = GALLERY_DIR / f"{theme}.png"
            shutil.copy2(generated, destination)
            print(f"Generated {destination.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
