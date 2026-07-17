import tempfile
import unittest
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

import generate


class GeneratorTests(unittest.TestCase):
    def test_parse_hex_color(self):
        self.assertEqual(generate.parse_hex_color("#123456"), (18, 52, 86, 255))
        with self.assertRaises(generate.ConfigError):
            generate.parse_hex_color("blue")

    def test_contain_image_respects_both_bounds(self):
        image = Image.new("RGBA", (2000, 500), "white")
        resized = generate.contain_image(image, 800, 800)
        self.assertLessEqual(resized.width, 800)
        self.assertLessEqual(resized.height, 800)

    def test_apple_and_google_play_presets(self):
        self.assertEqual(generate.PRESETS["app-store-iphone-6.9"], (1320, 2868))
        self.assertEqual(generate.PRESETS["google-play-phone-portrait"], (1080, 1920))

    def test_japanese_text_wraps_without_spaces(self):
        candidates = generate.default_font_candidates("ja")
        path = next((Path(item) for item in candidates if Path(item).is_file()), None)
        if path is None:
            self.skipTest("No Japanese font available")
        image = Image.new("RGB", (500, 500), "white")
        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype(str(path), size=40)
        wrapped = generate.wrap_text(draw, "これはスペースを含まない長い日本語の文章です", font, 200, "ja")
        self.assertIn("\n", wrapped)

    def test_missing_screenshot_is_reported(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            config = {
                "app": {"name": "Test"},
                "locales": ["ja", "en"],
                "outputs": [
                    {
                        "name": "app-store",
                        "preset": "app-store-iphone-6.9",
                        "directory": "./output/app-store",
                    }
                ],
                "theme": "./theme.yaml",
                "slides": [
                    {
                        "screenshot": "./missing.png",
                        "text": {
                            "ja": {"title": "タイトル", "body": "本文"},
                            "en": {"title": "Title", "body": "Body"},
                        },
                    }
                ],
            }
            theme = {
                "background": {"colors": ["#000000", "#111111"]},
                "headline": {"color": "#FFFFFF", "max_size": 100, "min_size": 50},
                "body": {"color": "#FFFFFF", "max_size": 40, "min_size": 20},
                "device": {"max_width_ratio": 0.8, "max_height_ratio": 0.6},
            }
            config_path = root / "config.yaml"
            theme_path = root / "theme.yaml"
            config_path.write_text(__import__("yaml").safe_dump(config, allow_unicode=True), encoding="utf-8")
            theme_path.write_text(__import__("yaml").safe_dump(theme), encoding="utf-8")
            with self.assertRaisesRegex(generate.ConfigError, "Screenshot not found"):
                generate.build_context(config_path, overwrite=False)


if __name__ == "__main__":
    unittest.main()
