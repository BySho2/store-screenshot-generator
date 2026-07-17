# Store Screenshot Generator

[日本語](README.ja.md)

Generate App Store and Google Play listing images from screenshots of your app.

The generator combines each app screenshot with localized headlines, supporting copy, and a customizable background. Content and visual settings live in YAML files, so you can reuse the same generator without editing the Python source for every app.

## Supported Output

- Japanese and English
- App Store: iPhone 6.9-inch portrait (`1320 x 2868`)
- Google Play: phone portrait (`1080 x 1920`)
- Apple and Google Play outputs generated in one run
- YAML configuration for copy, source screenshots, and visual themes
- Automatic Japanese and English line wrapping and text sizing
- PNG, JPEG, and WebP source images
- RGB PNG output without alpha channels
- Protection against accidental overwrites

## Generate the Sample

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

python examples/create_demo_screenshots.py
cp config.example.yaml config.yaml
python generate.py --config config.yaml
```

Japanese and English images are generated for both stores:

```text
output/
├── app-store/
│   ├── ja/
│   └── en/
└── google-play/
    ├── ja/
    └── en/
```

Use `--overwrite` only when you intend to replace existing generated images.

```bash
python generate.py --config config.yaml --overwrite
```

## Use It with Your App

1. Capture the app screens you want to use in your store listing.
2. Copy `config.example.yaml` to `config.yaml`.
3. Set each screenshot path and its Japanese and English copy in `config.yaml`.
4. Choose a theme and adjust it to match your app's brand when needed.
5. Run the generator.
6. Review every generated image for clipping, accuracy, and display order.

Your real app screenshots and `config.yaml` may contain private or unreleased information. Keep them in your own environment instead of committing them to this public repository.

## Customize the Design

Two themes are included:

- `themes/premium-navy.yaml`
- `themes/minimal-light.yaml`

You can change background colors, typography, accent colors, screenshot size, shadows, and other visual settings in YAML. See [Custom Themes](docs/custom-themes.md).

## How Images Are Generated

See [How It Works](docs/how-it-works.md) for the complete pipeline from an app screenshot to store listing images.

## Tests

```bash
python -m unittest discover -s tests -v
```

Before rendering, the generator validates source images, localized copy, fonts, colors, output presets, and existing files.

## Store Image Requirements

Store requirements can change. Check the latest official specifications before uploading generated images.

- [Apple screenshot specifications](https://developer.apple.com/help/app-store-connect/reference/app-information/screenshot-specifications/)
- [Google Play preview asset requirements](https://support.google.com/googleplay/android-developer/answer/9866151)

## License

[MIT](LICENSE)
