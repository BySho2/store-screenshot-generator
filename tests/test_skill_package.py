from __future__ import annotations

import importlib.util
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import yaml
from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "store-listing-screenshots"
VALIDATOR_PATH = SKILL / "scripts" / "validate_outputs.py"


def load_validator():
    spec = importlib.util.spec_from_file_location("validate_outputs", VALIDATOR_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("Could not load output validator")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class SkillPackageTests(unittest.TestCase):
    def test_local_markdown_links_resolve(self) -> None:
        link_pattern = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
        image_pattern = re.compile(r'<img\s+[^>]*src="([^"]+)"')
        for markdown in ROOT.rglob("*.md"):
            if any(part.startswith(".") for part in markdown.relative_to(ROOT).parts):
                continue
            text = markdown.read_text(encoding="utf-8")
            for target in link_pattern.findall(text) + image_pattern.findall(text):
                if target.startswith(("http://", "https://", "#")):
                    continue
                path = target.split("#", 1)[0]
                self.assertTrue((markdown.parent / path).exists(), f"{markdown}: {target}")

    def test_torekanri_example_is_reproducible(self) -> None:
        config_path = ROOT / "examples/torekanri/config.example.yaml"
        config = yaml.safe_load(config_path.read_text(encoding="utf-8"))
        self.assertEqual(len(config["slides"]), 3)
        self.assertEqual({output["name"] for output in config["outputs"]}, {"app-store", "google-play"})
        outputs = {output["name"]: output for output in config["outputs"]}
        self.assertEqual(outputs["app-store"]["device"]["frame"], "generic")
        self.assertEqual(outputs["google-play"]["device"]["frame"], "generic")
        self.assertGreater(
            outputs["app-store"]["device"]["corner_radius_ratio"],
            outputs["google-play"]["device"]["corner_radius_ratio"],
        )
        for slide in config["slides"]:
            self.assertTrue((config_path.parent / slide["screenshot"]).is_file())
        self.assertTrue((config_path.parent / config["theme"]).is_file())

    def test_skill_package_contains_required_files(self) -> None:
        required = [
            "SKILL.md",
            "agents/openai.yaml",
            "requirements.txt",
            "assets/config.template.yaml",
            "assets/project.template.yaml",
            "assets/capture-plan.template.md",
            "assets/themes/premium-navy.yaml",
            "assets/themes/minimal-light.yaml",
            "assets/themes/modern-gradient.yaml",
            "assets/themes/sunny-yellow.yaml",
            "assets/themes/dark-neon.yaml",
            "assets/themes/soft-pastel.yaml",
            "scripts/generate.py",
            "scripts/capture_ios.py",
            "scripts/capture_android.py",
            "scripts/validate_outputs.py",
            "scripts/create_contact_sheet.py",
            "references/screen-selection.md",
            "references/ios-capture.md",
            "references/android-capture.md",
            "references/copy-guidelines.md",
            "references/qa-checklist.md",
            "references/project-workflow.md",
            "references/installation.md",
            "references/installation.ja.md",
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

    def test_codex_and_claude_discovery_paths_resolve_to_canonical_skill(self) -> None:
        for relative in (
            ".agents/skills/store-listing-screenshots",
            ".claude/skills/store-listing-screenshots",
        ):
            link = ROOT / relative
            self.assertTrue(link.is_symlink(), relative)
            self.assertEqual(link.resolve(), SKILL.resolve())

    def test_root_cli_uses_the_canonical_generator(self) -> None:
        wrapper = (ROOT / "generate.py").read_text(encoding="utf-8")
        self.assertIn('"skills"', wrapper)
        self.assertIn('"store-listing-screenshots"', wrapper)
        self.assertEqual(
            (ROOT / "requirements.txt").read_text(encoding="utf-8"),
            (SKILL / "requirements.txt").read_text(encoding="utf-8"),
        )

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

    def test_validator_rejects_stale_extra_images(self) -> None:
        validator = load_validator()
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            output = root / "output" / "ja"
            output.mkdir(parents=True)
            Image.new("RGB", (1080, 1920), "white").save(output / "shot_ja_01.png")
            Image.new("RGB", (1080, 1920), "white").save(output / "stale.png")
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
            with self.assertRaisesRegex(validator.ValidationError, "Unexpected PNG"):
                validator.run(config_path)

    def test_copied_skill_generates_and_validates_without_repository_files(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            copied_skill = root / "installed-skill"
            shutil.copytree(SKILL, copied_skill)
            run_dir = root / "run"
            screenshots = run_dir / "screenshots"
            screenshots.mkdir(parents=True)
            Image.new("RGB", (390, 844), "#F4B400").save(screenshots / "01.png")
            shutil.copy2(copied_skill / "assets/themes/minimal-light.yaml", run_dir / "theme.yaml")
            config = {
                "app": {"name": {"en": "Demo"}},
                "locales": ["en"],
                "outputs": [
                    {
                        "name": "google-play",
                        "preset": "google-play-phone-portrait",
                        "directory": "./generated/google-play",
                        "filename": "shot_{locale}_{index:02d}.png",
                    }
                ],
                "theme": "./theme.yaml",
                "slides": [
                    {
                        "screenshot": "./screenshots/01.png",
                        "text": {
                            "en": {
                                "title": "A Clear Store Message",
                                "body": "Generated from a self-contained installed skill.",
                            }
                        },
                    }
                ],
            }
            config_path = run_dir / "config.yaml"
            config_path.write_text(yaml.safe_dump(config), encoding="utf-8")
            env = os.environ.copy()
            subprocess.run(
                [sys.executable, str(copied_skill / "scripts/generate.py"), "--config", str(config_path)],
                check=True,
                env=env,
                capture_output=True,
                text=True,
            )
            subprocess.run(
                [
                    sys.executable,
                    str(copied_skill / "scripts/validate_outputs.py"),
                    "--config",
                    str(config_path),
                ],
                check=True,
                env=env,
                capture_output=True,
                text=True,
            )
            self.assertTrue((run_dir / "generated/google-play/en/shot_en_01.png").is_file())


if __name__ == "__main__":
    unittest.main()
