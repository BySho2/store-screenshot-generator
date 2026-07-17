# App Store Screenshot Generator

[English](README.md)

アプリの実画面から、デザインと文章をカスタマイズしたApp Store掲載用スクリーンショットを生成するツールです。

初期公開版の対応範囲：

- 日本語・英語
- App Store iPhone 6.5インチ縦向き（`1242 x 2688`）
- YAMLによる文章・画像・テーマ設定
- 日本語を含む文字サイズと改行の自動調整
- PNG、JPEG、WebP入力
- アルファなしRGB PNG出力
- 意図しない上書きの防止

## すぐに試す

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

python examples/create_demo_screenshots.py
cp config.example.yaml config.yaml
python generate.py --config config.yaml
```

生成結果は`output/ja`と`output/en`へ保存されます。

既存の出力を意図的に置き換える場合だけ、`--overwrite`を付けます。

```bash
python generate.py --config config.yaml --overwrite
```

## 自分のアプリで使う

1. 公開してよいアプリ画面を撮影する
2. `config.example.yaml`を`config.yaml`へコピーする
3. スクショのパスと日本語・英語の文章を変更する
4. テーマを選ぶ、または自分のブランド色へ変更する
5. 生成後、全画像の文字切れと内容を目視確認する

`config.yaml`、生成結果、実アプリの素材は、公開権限が確認できない限りコミットしないでください。

## 生成の仕組み

[How It Works](docs/how-it-works.md)で、入力からPNG出力までの処理を説明しています。

## デザイン変更

次のテーマが付属します。

- `themes/premium-navy.yaml`
- `themes/minimal-light.yaml`

独自テーマは[Custom Themes](docs/custom-themes.md)を参考にYAMLだけで作成できます。

## テスト

```bash
python -m unittest discover -s tests -v
```

入力画像、言語、文章、フォント、色、出力プリセット、上書きなどを生成前に検証します。

## ストア仕様

ストア仕様は変更される可能性があります。アップロード前に必ず公式仕様を確認してください。

- [Apple公式スクリーンショット仕様](https://developer.apple.com/help/app-store-connect/reference/app-information/screenshot-specifications/)
- [Google Play公式プレビュー素材要件](https://support.google.com/googleplay/android-developer/answer/9866151)

初期公開版はGoogle Play対応をうたいません。

## ライセンス

[MIT License](LICENSE)
