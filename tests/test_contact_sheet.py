from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "skills/store-listing-screenshots/scripts/create_contact_sheet.py"


def load_module():
    spec = importlib.util.spec_from_file_location("create_contact_sheet", SCRIPT)
    if spec is None or spec.loader is None:
        raise RuntimeError("Could not load contact-sheet script")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class ContactSheetTests(unittest.TestCase):
    def test_creates_rgb_contact_sheet_from_nested_pngs(self) -> None:
        module = load_module()
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "generated"
            (source / "ja").mkdir(parents=True)
            for index, color in enumerate(("#2563EB", "#7C3AED", "#EC4899"), start=1):
                Image.new("RGB", (108, 192), color).save(source / "ja" / f"shot_{index}.png")
            output = root / "qa" / "contact-sheet.png"

            images = module.collect_images(source, output)
            module.create_contact_sheet(images, output, columns=2, title="Visual QA")

            self.assertTrue(output.is_file())
            with Image.open(output) as image:
                self.assertEqual(image.mode, "RGB")
                self.assertGreater(image.width, 108)
                self.assertGreater(image.height, 192)

    def test_rejects_empty_input_directory(self) -> None:
        module = load_module()
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            with self.assertRaisesRegex(ValueError, "No PNG images"):
                module.collect_images(root, root / "contact-sheet.png")


if __name__ == "__main__":
    unittest.main()
