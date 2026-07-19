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

    def test_rounded_and_generic_frames_are_transparent_at_outer_corners(self):
        image = Image.new("RGBA", (390, 844), "white")
        rounded = generate.render_device(image, {"frame": "rounded", "corner_radius_ratio": 0.08}, Path.cwd())
        generic = generate.render_device(image, {"frame": "generic"}, Path.cwd())
        self.assertEqual(rounded.getpixel((0, 0))[3], 0)
        self.assertEqual(generic.getpixel((0, 0))[3], 0)
        self.assertGreater(generic.width, image.width)

    def test_shadow_can_be_disabled_without_changing_size(self):
        image = Image.new("RGBA", (390, 844), "white")
        rendered = generate.add_shadow(image, {"enabled": False})
        self.assertEqual(rendered.size, image.size)

    def test_external_frame_places_screenshot_behind_asset(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            frame = Image.new("RGBA", (120, 240), (0, 0, 0, 0))
            ImageDraw.Draw(frame).rectangle((0, 0, 119, 239), outline="black", width=10)
            frame.save(root / "frame.png")
            source = Image.new("RGBA", (100, 200), "#2563EB")
            result = generate.render_device(
                source,
                {"frame": "asset", "frame_asset": "frame.png", "screen_rect": [10, 10, 100, 220]},
                root,
            )
            self.assertEqual(result.size, (120, 240))
            self.assertEqual(result.getpixel((60, 120))[:3], (37, 99, 235))
            self.assertEqual(result.getpixel((0, 0))[:3], (0, 0, 0))

    def test_output_device_override_preserves_nested_shadow_defaults(self):
        theme = {
            "device": {
                "frame": "rounded",
                "max_width_ratio": 0.8,
                "max_height_ratio": 0.6,
                "shadow": {"enabled": True, "opacity": 72, "blur_ratio": 0.03},
            }
        }
        merged = generate.merged_device_settings(theme, {"shadow": {"enabled": False}})
        self.assertFalse(merged["shadow"]["enabled"])
        self.assertEqual(merged["shadow"]["opacity"], 72)

    def test_asset_frame_is_validated_before_generation(self):
        device = {
            "frame": "asset",
            "frame_asset": "missing.png",
            "screen_rect": [10, 10, 100, 200],
            "max_width_ratio": 0.8,
            "max_height_ratio": 0.6,
        }
        with self.assertRaisesRegex(generate.ConfigError, "Device frame asset not found"):
            generate.validate_device_settings(device, Path.cwd())

    def test_apple_and_google_play_presets(self):
        self.assertEqual(generate.PRESETS["app-store-iphone-6.9"], (1320, 2868))
        self.assertEqual(generate.PRESETS["app-store-iphone-6.7"], (1290, 2796))
        self.assertEqual(generate.PRESETS["app-store-iphone-6.5"], (1242, 2688))
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
