# App Store Screenshot Generator

[日本語](README.ja.md)

Generate customizable, localized App Store screenshots from real app captures.

The initial release supports:

- Japanese and English
- App Store iPhone 6.5-inch portrait output (`1242 x 2688`)
- YAML-based content and design configuration
- Automatic text fitting, including Japanese text without spaces
- PNG, JPEG, and WebP source images
- RGB PNG output without alpha channels
- Safe overwrite behavior

## Quick Start

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

python examples/create_demo_screenshots.py
cp config.example.yaml config.yaml
python generate.py --config config.yaml
```

Generated files are written to `output/ja` and `output/en`.

To replace existing outputs intentionally:

```bash
python generate.py --config config.yaml --overwrite
```

## Use Your Own App

1. Put your captures in a private local folder.
2. Copy `config.example.yaml` to `config.yaml`.
3. Replace each slide's screenshot path and localized text.
4. Select or customize a theme.
5. Run the generator and visually inspect every output.

`config.yaml`, `output/`, and your private app captures should not be committed unless you have the right to publish them.

## Themes

Included themes:

- `themes/premium-navy.yaml`
- `themes/minimal-light.yaml`

See [Custom Themes](docs/custom-themes.md).

## How It Works

See [How It Works](docs/how-it-works.md) for the generation pipeline and input requirements.

## Validation

```bash
python -m unittest discover -s tests -v
```

The generator validates missing screenshots, unsupported locales and formats, missing copy, unavailable fonts, invalid colors, output presets, and accidental overwrites.

## Store Requirements

Store specifications can change. Verify generated files against the current official requirements before upload:

- [Apple screenshot specifications](https://developer.apple.com/help/app-store-connect/reference/app-information/screenshot-specifications/)
- [Google Play preview asset requirements](https://support.google.com/googleplay/android-developer/answer/9866151)

This initial release does not claim Google Play output support.

## License

[MIT](LICENSE)
