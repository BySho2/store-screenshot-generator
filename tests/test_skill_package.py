from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path

import yaml
from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / ".agents" / "skills" / "store-listing-screenshots"
VALIDATOR_PATH = SKILL / "scripts" / "validate_outputs.py"


def load_validator():
    spec = importlib.util.spec_from_file_location("validate_outputs", VALIDATOR_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("Could not load output validator")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class SkillPackageTests(unittest.TestCase):
    def test_skill_package_contains_required_files(self) -> None:
        required = [
            "SKILL.md",
            "agents/openai.yaml",
            "scripts/capture_ios.sh",
            "scripts/capture_android.sh",
            "scripts/validate_outputs.py",
            "references/screen-selection.md",
            "references/ios-capture.md",
            "references/android-capture.md",
            "references/copy-guidelines.md",
            "references/qa-checklist.md",
        ]
        for relative in required:
            self.assertTrue((SKILL / relative).is_file(), relative)

    def test_skill_metadata(self) -> None:
        text = (SKILL / "SKILL.md").read_text(encoding="utf-8")
        _, frontmatter, _ = text.split("---", 2)
        metadata = yaml.safe_load(frontmatter)
        self.assertEqual(metadata["name"], "store-listing-screenshots")
        self.assertIn("App Store", metadata["description"])
        self.assertIn("Google Play", metadata["description"])

    def test_validator_accepts_expected_images(self) -> None:
        validator = load_validator()
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            output = root / "output" / "ja"
            output.mkdir(parents=True)
            Image.new("RGB", (1080, 1920), "white").save(output / "shot_ja_01.png")
            config = {
                "locales": ["ja"],
                "slides": [{"screenshot": "source.png"}],
                "outputs": [
                    {
                        "name": "google-play",
                        "preset": "google-play-phone-portrait",
                        "directory": "./output",
                        "filename": "shot_{locale}_{index:02d}.png",
                    }
                ],
            }
            config_path = root / "config.yaml"
            config_path.write_text(yaml.safe_dump(config), encoding="utf-8")
            self.assertEqual(validator.run(config_path), 1)


if __name__ == "__main__":
    unittest.main()
